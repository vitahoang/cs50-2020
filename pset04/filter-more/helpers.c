#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float gray_scale;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            gray_scale = (image[i][j].rgbtBlue +
                          image[i][j].rgbtGreen +
                          image[i][j].rgbtRed) /
                         3.0;
            image[i][j].rgbtBlue = round(gray_scale);
            image[i][j].rgbtGreen = round(gray_scale); 
            image[i][j].rgbtRed = round(gray_scale);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
