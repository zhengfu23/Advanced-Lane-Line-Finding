import cv2
import numpy as np

def abs_sobel_thresh(img, orient='x', sobel_kernel=3, thresh=(0,255)):
    xorder = 1
    yorder = 0
    if orient=='y':
        xorder = 0
        yorder = 1
    sobel = cv2.Sobel(img, cv2.CV_64F, xorder, yorder, ksize=sobel_kernel)
    abs_sobel = np.absolute(sobel)
    grad_binary = np.zeros_like(abs_sobel)
    grad_binary[(abs_sobel>thresh[0]) & (abs_sobel<thresh[1])] = 1
    return grad_binary

def mag_thresh(img, sobel_kernel=3, thresh=(0,255)):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    mag_sobel = np.sqrt(np.square(sobelx) + np.square(sobely))
    mag_binary = np.zeros_like(mag_sobel)
    mag_binary[(mag_sobel>thresh[0]) & (mag_sobel<thresh[1])] = 1
    return mag_binary

def dir_thresh(img, sobel_kernel=3, thresh=(0,255)):
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    dir_sobel = np.arctan2(abs_sobely, abs_sobelx)
    dir_binary = np.zeros_like(dir_sobel)
    dir_binary[(dir_sobel>thresh[0]) & (dir_sobel<thresh[1])] = 1
    return dir_binary

image = cv2.imread('test_images/signs_vehicles_xygrad.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ksize = 3

gradx = abs_sobel_thresh(gray, orient='x', sobel_kernel=ksize, thresh=(0, 255))
grady = abs_sobel_thresh(gray, orient='y', sobel_kernel=ksize, thresh=(0, 255))
mag_binary = mag_thresh(gray, sobel_kernel=ksize, thresh=(0, 255))
dir_binary = dir_thresh(gray, sobel_kernel=ksize, thresh=(0, np.pi/2))

combined = np.zeros_like(dir_binary)
combined[((gradx == 1) & (grady == 1)) | ((mag_binary == 1) & (dir_binary == 1))] = 1

cv2.imshow('output', combined)
cv2.waitKey()
