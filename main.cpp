#include <iostream>
#include <fstream>
#include <string>
#include <opencv4/opencv2/opencv.hpp>
#include <opencv4/opencv2/imgcodecs.hpp>

// Use opencv to do image handling

//TODO: Features
//Store and retrieve data from  
//Work out how to read and write rgb image data from pngs etc: opencv


std::string read_file(std::string filename)
{
    std::string s = "";
    std::ifstream in(filename, std::ios::binary);
    char c;
    while (in)
    {
        in.get(c);
        if (in)
        {
            s += int(c);
        }
    }
    in.close();
    return s;
}

void write_file(std::string filename, std::string data)
{
    std::ofstream out(filename);
    out << data;
    out.close();
}

void write_secret_to_image(cv::Mat image, std::string secret)
{
    uint stringIndex = 0;

    uchar pixValue;
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);

            if (stringIndex == secret.length() - 1)
            {
                intensity.val[3] = 0; // have an alpha value of 0 be a null terminator
            }
            intensity.val[3] -= (int)secret[stringIndex]; // Minus value from alpha - defaults is 255.
            stringIndex++;
        }
    }
}

std::string read_secret_from_image(cv::Mat image)
{
    std::string secret = "";
    uchar pixValue;
    for (int i = 0; i < image.cols; i++)
    {
        for (int j = 0; j < image.rows; j++)
        {
            cv::Vec4b &intensity = image.at<cv::Vec4b>(j, i);

            if (intensity.val[3] == 0)
            {
                return secret;
            }
            secret += (uchar)(255 - intensity.val[3]); // Minus value from alpha - defaults is 255.
        }
    }
    return secret;
}

int main(int argc, char *argv[])
{
    // if (argc != 3)
    // {
    //     return 0;
    // }
    // std::string main_file = read_file(argv[1]);
    // std::string secret_file = read_file(argv[2]);
    // size_t secret_position = 10000;
    // main_file.replace(secret_position, 3, "Hello World!");
    // std::string embedded_filename = "output.png";
    // write_file(embedded_filename, main_file);

    cv::Mat image = cv::imread("pr5ded8pqr0b1.png",
                               cv::IMREAD_UNCHANGED);

    // cv::cvtColor(image, image, cv::COLOR_RGB2RGBA);

    // cv::Size resized{800, 400};
    // cv::resize(image, image, resized);
    // cv::imshow("Window", image);

    // write_secret_to_image(image, "Hello world!");

    std::cout << read_secret_from_image(image) << std::endl;

    cv::imwrite("output.png", image);

    // cv::waitKey(0);

    return 0;
}