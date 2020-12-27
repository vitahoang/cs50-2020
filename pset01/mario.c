#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, lineno;

    do
    {
        height = get_int("How hight do you want Mario to jump through?\n");
    } while (height < 1 || height > 8);

    for (lineno = 1; lineno <= height; lineno++)
    {
        int column;
        for (column = height - lineno; column > 0; --column)
        {
            putchar(' ');
        }

        for (column = 0; column < lineno; column++)
        {
            putchar('#');
        }

        printf("  ");

        for (column = 0; column < lineno; column++)
        {
            putchar('#');
        }
        putchar('\n');
    }
}
