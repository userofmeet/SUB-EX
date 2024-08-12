# Crack Detection with OpenCV

This script detects cracks in an image using OpenCV by applying non-maximal suppression and Sobel filters. The detected cracks are outlined with rectangles, and the user has the option to save the processed image by pressing 's'.

## Python Code

```python
import cv2
import math
import numpy as np
import scipy.ndimage

def orientated_non_max_suppression(mag, ang):
    ang_quant = np.round(ang / (np.pi/4)) % 4
    winE = np.array([[0, 0, 0],[1, 1, 1], [0, 0, 0]])
    winSE = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    winS = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    winSW = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    magE = non_max_suppression(mag, winE)
    magSE = non_max_suppression(mag, winSE)
    magS = non_max_suppression(mag, winS)
    magSW = non_max_suppression(mag, winSW)

    mag[ang_quant == 0] = magE[ang_quant == 0]
    mag[ang_quant == 1] = magSE[ang_quant == 1]
    mag[ang_quant == 2] = magS[ang_quant == 2]
    mag[ang_quant == 3] = magSW[ang_quant == 3]
    return mag

def non_max_suppression(data, win):
    data_max = scipy.ndimage.filters.maximum_filter(data, footprint=win, mode='constant')
    data_max[data != data_max] = 0
    return data_max

# start calulcation
gray_image = cv2.imread(r'C:\Users\djain\Downloads\a.png', 0)

with_nmsup = True #apply non-maximal suppression
fudgefactor = 1.3 #with this threshold you can play a little bit
sigma = 21 #for Gaussian Kernel
kernel = 2*math.ceil(2*sigma)+1 #Kernel size

gray_image = gray_image/255.0
blur = cv2.GaussianBlur(gray_image, (kernel, kernel), sigma)
gray_image = cv2.subtract(gray_image, blur)

# compute sobel response
sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
mag = np.hypot(sobelx, sobely)
ang = np.arctan2(sobely, sobelx)

# threshold
threshold = 4 * fudgefactor * np.mean(mag)
mag[mag < threshold] = 0

#either get edges directly
if with_nmsup is False:
    mag = cv2.normalize(mag, 0, 255, cv2.NORM_MINMAX)
    kernel = np.ones((5,5),np.uint8)
    result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('im', result)
    cv2.waitKey()

#or apply a non-maximal suppression
else:

    # non-maximal suppression
    mag = orientated_non_max_suppression(mag, ang)
    # create mask
    mag[mag > 0] = 255
    mag = mag.astype(np.uint8)

    kernel = np.ones((5,5),np.uint8)
    result = cv2.morphologyEx(mag, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('im', result)
    cv2.waitKey()
```


## Original Picture
![image](https://github.com/user-attachments/assets/0bef8b6d-0459-42e4-aa27-55f1d4110ed6)

![image](https://github.com/user-attachments/assets/f100ff69-e87a-45a4-895d-8367abfe50af)



## Detected Crack 
![detected_crack](https://github.com/user-attachments/assets/5b5797af-8c40-4dd9-818f-82a13c35a495)

![detected_crack](https://github.com/user-attachments/assets/f5a88555-26d4-42bb-b4c6-70f41cf3804f)
