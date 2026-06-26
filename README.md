# Raster Image to Equation Converter
A programme where it converts the uploaded image into a set of parametric mathematical equations where it could be plotted onto Desmos.
Release link: https://github.com/cziwu12/Raster-Image-to-Equation-Converter/releases/tag/v1.0

<img width="1361" height="497" alt="Screenshot 2026-06-05 013845" src="https://github.com/user-attachments/assets/898e641d-34d4-4793-b77b-d72f04372192" />

## Features

- Converts raster images into parametric Desmos equations
- Uses OpenCV edge detection and contour extraction
- Optional image blurring and resizing
- Exports equations directly to a text file for Desmos
- Includes sample images for testing

## Quick Start

1. Download the latest release.
2. Run Raster Image to Equation Converter.exe.
3. Paste the image path along with resize and blur options when prompted.
4. Copy the generated equations into Desmos.

## Running From Source
1. Clone the repo or download it as a ZIP file.
```bash
git clone https://github.com/cziwu12/Raster-image-to-equation-convert-for-Desmos.git
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage 
Copy the path of the image you want to convert and paste it into the "image path:" prompt. JPEG and PNG files work best, although most non-transparent image formats should work. Several example images are included in the repository.

After that you'll be asked if you want to resize or blur your image, type ```yes``` (or ```y```) to comfirm or any key to deny. The reason for this is to reduce the amount of equations generated which improves desmos performance (in addition to reduce noise for blur). I would generally recommend blurring the image but you may chose not to if you want the graph to be as accurate as your image.

Once you done both of those, there'll be some windows showing the result of the edge detection algorithm and the contours, you can close by entering any key. If you chose to resize your image the contours overlaid onto the image will be on the top left (the same thing for the graph) so you can ignore that.

<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/3f2b85b4-72e7-4eae-8d25-7a1bdbec821e" />

Sometimes the window might overextend to the bottom of the task bar which you can also ignore.

<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/e3a07f3a-4d18-4730-ac1c-34d79d7f816d" />

After those windows, the equations will be exported to a file named ```desmos_equations_list```. Open that file, copy everything inside it and paste it into desmos. It might take a while to load but once the equations are loaded, zoom out until you see the graph. Usually, the graph (or some parts of it) should show up at x,y = 200. If it doesn't show up, wait a while as the graph might take a while to load. 

## How it works
It uses OpenCV, a popular computer vision library, for the edge detection. The program first grayscales the image (and blurs it if you chose the option) to allow for easier detection while reducing noise. It then goes through a function called cv2.Canny() which highlights and locates the boundaries of an image. Then it goes through cv2.findContours which uses the output from cv2.Canny to identify the contours and simplifies it using cv2.approxPolyDP. 

After this it then identifies the parameters for the equation. The equation I’m using is the quadratic Bezier:

$(1-t)^2{x_0}+2(1-t)t{x_1}+t^2{x_2}$

where $0 <= t <= 1$, $P0$ is the starting point, $P2$ the end point and $P1$ the control point where it determines the curvature. 

To find these curves I looped each individual contour and set P1 as the entire contour, P0 as the midpoint between the entire contour plus the entire contour moved forward by one index then dividing the result by 2 and P2 as the midpoint between the entire contour plus the entire contour moved backward by one index then divided by 2. The reason for this is because if I identify P0, P1 and P2 as individual points on a contour, it would curve too much.

 Using this method allows for smoother curves and the process would be faster (since I’m using vectorization). The program does this process for every contour before exporting this into a file where you can copy/paste this into desmos. 

## Limitations
This program isn’t perfect yet (it’s v1) so there are some limitations to it. Firstly the program generates a thousands of equations which will affect desmos ability to plot it. 

The current limit for this is ~10 thousand equations which might sound a lot but images contains thousands of edges so I would recommend blurring the image (technically this is limited by the amount of memory so technically you can go above 10K but it will take a while to load).  

Also I’m currently still using the quadratic bezier curve for every edge which means that some parts  (like straight lines) will look wonky.
