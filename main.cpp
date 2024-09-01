#include <iostream>
#include <string>
#include <stdexcept>
#include "encrypt.hpp"
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/imgcodecs.hpp>

//Todo:
// Encrypt secret string
// Do lossless compression?

void write_secret_to_image(cv::Mat image, std::string secret)
{
    //Encodes secret string into the alpha channels of target image s.t char = 255-intensity.val[3].
    //Saves encoded image as encoded_image.png

    uint stringIndex = 0;
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);
            
            if (stringIndex == secret.length())
            {
                //Insert a null terminator. Assumes no characters have ascii value of 255.
                intensity.val[3] = 0; 
                cv::imwrite("encoded_image.png",image);
                return;
            }
            intensity.val[3] -= static_cast<int>(secret[stringIndex]); // Minus value from alpha - defaults is 255.
            stringIndex++;
        }
    }

    throw std::length_error("Target image not large enough to store secret string");

}

std::string read_secret_from_image(cv::Mat image)
{
    //Extracts secret string from the alpha channels of target image s.t char = 255-intensity.val[3].
    //Returns secret string from function.


    std::string secret = "";
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);

            if (intensity.val[3] == 0)
            {
                //When null terminator reached - exit function.
                return secret;
            }
            secret += static_cast<char>(255 - intensity.val[3]); // Minus value from alpha - defaults is 255.
        }
    }
    return secret;
}

void display_image(cv::Mat &img){
    //Shows small version of image on the screen in a cv2 window. Debugging purposes.
    cv::Mat copyImage;
    cv::resize(img,copyImage,cv::Size{800,400});
    cv::imshow("Title",copyImage);
    cv::waitKey(0);
}

void encode_secret(std::string img_path, std::string secret){
    // Encodes secret into image - saves image as encoded_image.png
    //Reads the image as r,g,b and converts to r,g,b,a - sets alpha value to 255
    cv::Mat image = cv::imread(img_path,
                               cv::IMREAD_COLOR);
    cv::cvtColor(image, image, cv::COLOR_RGB2RGBA);

    write_secret_to_image(image, secret);
}

std::string decode_secret(std::string img_path){

    //Returns the secret string encoded in the image located at image path.
    //IMREAD_UNCHANGED preserves alpha channel value
    cv::Mat image = cv::imread(img_path,
                               cv::IMREAD_UNCHANGED);

    return read_secret_from_image(image);
}

int main(int argc, char *argv[])
{

    std::string secret = "Hello world!";

    encode_secret("gy65o4mk3oe01.png",secret);

    std::cout << decode_secret("encoded_image.png") << std::endl;

    return 0;
}