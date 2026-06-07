import cv2
import numpy as np

yesOptions = ['yes', 'y']
simplified_contours = []
allp0 = []
allp1 = []
allp2 = []
desmosList = []  
 
IMG_PATH = input("image path: ").strip('"\'# ')
img = cv2.imread(IMG_PATH)

if img is None:
    print("Error: Could not load image.")
    exit()

useResize = input("is resize needed? (Type yes if needed, else just enter any key):  ").lower() in yesOptions
resizedImg = cv2.resize(img, None, fx=0.5, fy=0.5) if useResize else img

gray = cv2.cvtColor(resizedImg, cv2.COLOR_BGR2GRAY)
useBlur = input("is blur needed? (Type yes if needed, else just enter any key): ").lower() in yesOptions

targetImg = (cv2.bilateralFilter(gray, d=4, sigmaColor=140, sigmaSpace=150) if useBlur else gray)

if useBlur:
    cv2.imshow("Blur (Enter any key to close)", targetImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

canny = cv2.Canny(targetImg, 50, 150)

cv2.imshow("Canny (Enter any key to close)", canny)
cv2.waitKey()
cv2.destroyAllWindows()

contours, hierarchy = cv2.findContours(image=canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    epsilon = 0.001 * cv2.arcLength(cnt, True)
    approx =  cv2.approxPolyDP(cnt, epsilon, True)
    simplified_contours.append(approx)
    
img_copy = resizedImg.copy()
cv2.drawContours(img_copy, simplified_contours, -1, (0, 255, 0), 3)

cv2.imshow('None approximation (Enter any key to close)', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()

for i in simplified_contours:
    print(i.shape)
    new_arr = i.squeeze(axis=1)
    if len(new_arr) < 3:
        continue
    else:
        p1 = new_arr
        p0 = (np.roll(new_arr, shift=1, axis=0) + new_arr) / 2
        p2 = (new_arr + np.roll(new_arr, shift=-1, axis=0)) / 2

        allp0.append(p0)
        allp1.append(p1)
        allp2.append(p2)
        
height = img.shape[0]
combined_p0 = np.vstack(allp0)
combined_p1 = np.vstack(allp1)
combined_p2 = np.vstack(allp2)

x0 = combined_p0[:, 0]
y0 = combined_p0[:, 1]

x1 = combined_p1[:, 0]
y1 = combined_p1[:, 1]

x2 = combined_p2[:, 0]
y2 = combined_p2[:, 1]

desmos_y0 = height - y0
desmos_y1 = height - y1
desmos_y2 = height - y2

desmosList = [
    f"((1-t)^2*{x_0}+2(1-t)t*{x_1}+t^2*{x_2},(1-t)^2*{y_0}+2(1-t)t*{y_1}+t^2*{y_2})"
    for x_0, y_0, x_1, y_1, x_2, y_2 in zip(x0, desmos_y0, x1, desmos_y1, x2, desmos_y2)
]

with open("desmos_equations_list", 'w') as desmos:
    desmos.write("\n".join(desmosList))
print(f"Generated {len(desmosList)} equations")
print("Saved to desmos_equations_list")
input("Press Enter to exit...")