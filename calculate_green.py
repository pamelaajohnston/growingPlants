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
    return fileList

def makeFreshDir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)

if __name__ == "__main__":
    source_dir = "../data" # The directory where you store your images
    dest_dir = "../evaluation" # The directory where any images will go


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

    for imageName in imageNames:
        imageBaseName = os.path.splitext(os.path.basename(imageName))[0]
        print(imageBaseName)
        img_mat = cv2.imread(imageName)
        img = np.asarray(img_mat)
        iheight, iwidth = img.shape[:2]
        print(img.shape)


        for i in range(0, 3):
            c = img[:, :, i]
            print("Channel {} Maximum {} Minimum {} Mean {}".format(i, np.amax(c), np.amin(c), np.mean(c)))

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
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for i in range(0, 3):
            c = hsv[:, :, i]
            print("Channel {} Maximum {} Minimum {} Mean {}".format(i, np.amax(c), np.amin(c), np.mean(c)))
        # Threshold of blue in HSV space
        #lower_green = np.array([60, 35, 140])
        #upper_green = np.array([180, 255, 255])
        # Threshold of green in HSV space
        lower_green = np.array([21, 97, 43])
        upper_green = np.array([40, 255, 255])
        #lower_green = np.array([(79*255/100), (26*255/100), (32*255/100)])
        #upper_green = np.array([(153*255/100), (100*255/100), (100*255/100)])

        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower_green, upper_green)
        print(mask)

        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-green regions
        result = cv2.bitwise_and(img, img, mask = mask)

        cv2.imshow('frame', img)
        cv2.imshow('mask', mask)
        cv2.imshow('result', result)

        cv2.waitKey(0)
