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

# Load the original color image
image = cv2.imread(r'C:\Users\djain\Downloads\a.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

with_nmsup = True # apply non-maximal suppression
fudgefactor = 1.3 # with this threshold you can play a little bit
sigma = 21 # for Gaussian Kernel
kernel = 2*math.ceil(2*sigma)+1 # Kernel size

gray_image = gray_image/255.0
blur = cv2.GaussianBlur(gray_image, (kernel, kernel), sigma)
gray_image = cv2.subtract(gray_image, blur)

# Compute sobel response 
sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
mag = np.hypot(sobelx, sobely)
ang = np.arctan2(sobely, sobelx)

# Threshold
threshold = 4 * fudgefactor * np.mean(mag)
mag[mag < threshold] = 0

# Apply non-maximal suppression
if with_nmsup:
    mag = orientated_non_max_suppression(mag, ang)

# Create mask for edges
mag[mag > 0] = 255
mag = mag.astype(np.uint8)

# Find contours based on edges
contours, _ = cv2.findContours(mag, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw rectangles around contours on the original color image
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Display the color image with rectangles
cv2.imshow('Detected Edges', image)
cv2.waitKey(0)

# Save the image with rectangles
k = cv2.waitKey(0) & 0xFF
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite(r'C:\Users\djain\Downloads\detected_crack.png', image)
    cv2.destroyAllWindows()

cv2.destroyAllWindows()

```

## Original Picture
![d](https://github.com/user-attachments/assets/ccb18431-b364-46bc-b1b5-7a46f6214c5e)
![image](https://github.com/user-attachments/assets/821ff51e-d8b2-4e8f-bea3-82154f0045bc)


## Cracks Detected
![detected_crack](https://github.com/user-attachments/assets/3d4ef729-3cd0-46f2-9de7-b5fec2cec4c2)
![detected_crack](https://github.com/user-attachments/assets/f743196b-fe66-4a10-9f44-d9c6a7f76f4c)
