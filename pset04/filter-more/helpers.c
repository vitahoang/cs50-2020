#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int gray_scale;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            gray_scale = round((image[i][j].rgbtBlue +
                                image[i][j].rgbtGreen +
                                image[i][j].rgbtRed) /
                               3.0);
            image[i][j].rgbtBlue = gray_scale;
            image[i][j].rgbtGreen = gray_scale;
            image[i][j].rgbtRed = gray_scale;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*reflection)
    [width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, w = width - 1; j < width; j++, w--)
        {
            reflection[i][w] = image[i][j];
        }
    }
    memcpy(image, reflection, height * width * sizeof(RGBTRIPLE));
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*blur_image)
    [width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avgRed, avgGreen, avgBlue;
            avgRed = avgGreen = avgBlue = 0;
            float count = 0.0;

            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // offset if pixel is at top edge
                    if (i + k < 0 || i + k > height - 1)
                    {

                        continue;
                    }

                    // offset if pixel is at left edge
                    if (j + l < 0 || j + l > width - 1)
                    {
                        continue;
                    }

                    avgRed += image[i + k][j + l].rgbtRed;
                    avgGreen += image[i + k][j + l].rgbtGreen;
                    avgBlue += image[i + k][j + l].rgbtBlue;
                    count += 1;
                }
            }
            blur_image[i][j].rgbtRed = round(avgRed / count);
            blur_image[i][j].rgbtGreen = round(avgGreen / count);
            blur_image[i][j].rgbtBlue = round(avgBlue / count);
        }
    }
    memcpy(image, blur_image, height * width * sizeof(RGBTRIPLE));
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*edge_image)
    [width] = calloc(height, width * sizeof(RGBTRIPLE));
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double GxRed, GxGreen, GxBlue, GyRed, GyGreen, GyBlue;
            GxRed = GxGreen = GxBlue = GyRed = GyGreen = GyBlue = 0.0;
            // offset the pointer to the top right of the convolution kernel 3x3
            for (int k = -1; k < 2; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    // offset if pixel is at top edge
                    if (i + k < 0 || i + k > height - 1)
                    {
                        continue;
                    }

                    // offset if pixel is at left edge
                    if (j + l < 0 || j + l > width - 1)
                    {
                        continue;
                    }

                    GxRed += image[i + k][j + l].rgbtRed * Gx[k + 1][l + 1];
                    GxGreen += image[i + k][j + l].rgbtGreen * Gx[k + 1][l + 1];
                    GxBlue += image[i + k][j + l].rgbtBlue * Gx[k + 1][l + 1];
                    GyRed += image[i + k][j + l].rgbtRed * Gy[k + 1][l + 1];
                    GyGreen += image[i + k][j + l].rgbtGreen * Gy[k + 1][l + 1];
                    GyBlue += image[i + k][j + l].rgbtBlue * Gy[k + 1][l + 1];
                }
            }
            int red = round(sqrt(GxRed * GxRed + GyRed * GyRed));
            int green = round(sqrt(GxGreen * GxGreen + GyGreen * GyGreen));
            int blue = round(sqrt(GxBlue * GxBlue + GyBlue * GyBlue));

            edge_image[i][j].rgbtRed = (red > 255) ? 255 : red;
            edge_image[i][j].rgbtGreen = (green > 255) ? 255 : green;
            edge_image[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
        }
    }
    memcpy(image, edge_image, height * width * sizeof(RGBTRIPLE));
    return;
}
