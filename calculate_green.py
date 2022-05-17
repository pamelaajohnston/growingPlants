import cv2
import numpy as np
import pandas as pd
import argparse
import os
import shutil


def createFileList(myDir, formats=['.tif', '.png', '.tiff', ',jpeg', '.jpg']):
    fileList = []
    for root, dirs, files in os.walk(myDir, topdown=False):
        for name in files:
            for format in formats:
                if name.endswith(format):
                    fullName = os.path.join(root, name)
                    fileList.append(fullName)
    fileList = sorted(fileList)
    return fileList

def makeFreshDir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)

if __name__ == "__main__":
    source_dir = "../data" # The directory where you store your images
    dest_dir = "../evaluation" # The directory where any images will go
    do_green_analysis = False
    do_crop = True
    save_masks = False


    # arguments
    parser = argparse.ArgumentParser(description="Takes a folder of images of plants and quantitatively evaluates the leaves in them")
    parser.add_argument("-s", "--source", help="the source directory where all the source images already live")
    parser.add_argument("-d", "--dest",   help="the (optional) destination directory (will make it if it doesn't exist, wipe it if it does), stores intermediate images if specified")


    args = parser.parse_args()

    if args.source:
        source_dir = args.source
    if args.dest:
        dest_dir = args.dest

    print("Getting pictures from {}".format(source_dir))
    print("Deleting and remaking directory {}".format(dest_dir))
    makeFreshDir(dest_dir)

    imageNames = createFileList(source_dir)
    print(imageNames)
    #imageNames = imageNames[:30] #smaller dataset size for testing

    result_list = []
    for imageName in imageNames:
        imageBaseName = os.path.splitext(os.path.basename(imageName))[0]
        #print(imageBaseName)
        img_mat = cv2.imread(imageName)

        img = np.asarray(img_mat)
        if do_crop:
            # Let's add a centre crop to help get rid of the background
            h, w = img.shape[:2]
            t = 100
            b = h - 100
            l = 200
            r = w - 200

            img_crop = img[t:b, l:r, :].copy()
            #print(img_crop.shape)
        else:
            img_crop = img
        hsv = cv2.cvtColor(img_crop, cv2.COLOR_BGR2HSV)
        #print(img.shape)


        if do_green_analysis: # this is the part where we work out the best green values
            for i in range(0, 3):
                c = img[:, :, i]
                print("RGB[{}]: Maximum {} Minimum {} Mean {}".format(i, np.amax(c), np.amin(c), np.mean(c)))

            blue = img.copy()
            blue[:,:,1] = 0
            blue[:,:,2] = 0
            #cv2.imshow('blue', blue)

            green = img.copy()
            green[:,:,0] = 0
            green[:,:,2] = 0
            #cv2.imshow('green', green)

            red = img.copy()
            red[:,:,0] = 0
            red[:,:,1] = 0
            #cv2.imshow('red', red)


            # From https://www.geeksforgeeks.org/filter-color-with-opencv/
            # and https://www.rapidtables.com/web/color/RGB_Color.html to pick color
            for i in range(0, 3):
                c = hsv[:, :, i]
                print("HSV[{}]: Maximum {} Minimum {} Mean {}".format(i, np.amax(c), np.amin(c), np.mean(c)))
        # Threshold of green in HSV space (take it from a sample of the plants)
        lower_green = np.array([21, 97, 43])
        upper_green = np.array([64, 255, 255])

        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower_green, upper_green)
        total_green = np.sum(mask)
        mytuple = [imageBaseName, total_green]
        print("File {} has {} greens".format(imageBaseName, total_green))
        result_list.append(mytuple)

        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-green regions
        result = cv2.bitwise_and(img_crop, img_crop, mask = mask)

        # save the mask
        if save_masks:
            save_file_name = os.path.join(dest_dir, "{}.png".format(imageBaseName))
            cv2.imwrite(save_file_name, result)
    #lastly, plot the graph
    results_df = pd.DataFrame(result_list, columns=['file', 'green pels'])
    lines = results_df.plot.line(x='file', y='green pels', rot=90)
    fig = lines.get_figure()
    fig.savefig("graph.png")
