#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, pyramid_level;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (pyramid_level = 1; pyramid_level <= height; pyramid_level++)
    {
        int column;
        for (column = height - pyramid_level; column > 0; --column)
        {
            putchar(' ');
        }

        for (column = 0; column < pyramid_level; column++)
        {
            putchar('#');
        }

        printf("  ");

        for (column = 0; column < pyramid_level; column++)
        {
            putchar('#');
        }
        putchar('\n');
    }
}