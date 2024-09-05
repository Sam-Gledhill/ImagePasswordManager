#!/usr/bin/bash
g++ main.cpp encrypt.cpp -o ipwm -I /usr/local/include/opencv4 -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_imgcodecs;./ipwm
