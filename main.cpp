#include <iostream>
#include <string>
#include <stdexcept>
#include "encrypt.hpp"
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/imgcodecs.hpp>

// Todo:
//  Work on the security of the encryption algorithm
//  Have offset to data in image defined by the key. Fill the rest of the image with junk data.

void write_secret_to_image(cv::Mat image, std::string image_dest, std::string secret)
{
    // Encodes secret string into the alpha channels of target image s.t char = 255-intensity.val[3].
    // Saves encoded image as encoded_image.png

    uint stringIndex = 0;
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);

            if (stringIndex == secret.length())
            {
                // Insert a null terminator. Assumes no characters have ascii value of 255.
                intensity.val[3] = 0;
                cv::imwrite(image_dest, image);
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
    // Extracts secret string from the alpha channels of target image s.t char = 255-intensity.val[3].
    // Returns secret string from function.

    std::string secret = "";
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);

            if (intensity.val[3] == 0)
            {
                // When null terminator reached - exit function.
                return secret;
            }
            secret += static_cast<char>(255 - intensity.val[3]); // Minus value from alpha - defaults is 255.
        }
    }
    return secret;
}

void display_image(cv::Mat &img)
{
    // Shows small version of image on the screen in a cv2 window. Debugging purposes.
    cv::Mat copyImage;
    cv::resize(img, copyImage, cv::Size{800, 400});
    cv::imshow("Title", copyImage);
    cv::waitKey(0);
}

void encode_secret(std::string img_path, std::string img_dest, std::string secret, std::string password)
{
    // Encodes secret into image - saves image as encoded_image.png
    // Reads the image as r,g,b and converts to r,g,b,a - sets alpha value to 255
    cv::Mat image = cv::imread(img_path,
                               cv::IMREAD_COLOR);
    cv::cvtColor(image, image, cv::COLOR_RGB2RGBA);

    // Encrypt secret with viginere algorithm for added security
    std::string encrypted_secret = viginere_encrypt(secret, password);
    write_secret_to_image(image, img_dest, encrypted_secret);
}

std::string decode_secret(std::string img_path, std::string password)
{

    // Returns the secret string encoded in the image located at image path.
    // IMREAD_UNCHANGED preserves alpha channel value
    cv::Mat image = cv::imread(img_path,
                               cv::IMREAD_UNCHANGED);

    std::string encrypted_secret = read_secret_from_image(image);
    return viginere_decrypt(encrypted_secret, password);
}

bool ends_with(std::string str, std::string suffix)
{
    return str.size() >= suffix.size() && str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
}

bool is_png(std::string file_path)
{
    return ends_with(file_path, ".png");
}

int main(int argc, char *argv[])
{

    if (argc == 5)
    {
        std::string img_path = argv[1];
        std::string img_dest = argv[2];

        assert(is_png(img_path) && is_png(img_dest));

        std::string secret = argv[3];
        std::string password = argv[4];
        encode_secret(img_path, img_dest, secret, password);
    }

    else if (argc == 3)
    {
        std::string img_path = argv[1];
        std::string password = argv[2];
        std::cout << decode_secret(img_path, password) << std::endl;
        return 0;
    }

    else
    {
        std::cout << "Cli arguments invalid. Should either be to encrypt(img_path,img_dest,secret,password) or decrypt([img_path,secret])" << std::endl;
        return -1;
    }
}