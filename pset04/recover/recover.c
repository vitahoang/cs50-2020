#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define FAT 512
typedef unsigned char BYTE;

int main(int argc, char *argv[])
{
    // program must accept only one argument
    if (argc > 2)
    {
        printf("Usage: ./recover [image disk]\n");
        return 1;
    }

    // open forentic file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        fclose(input);
        printf("Could not open %s.\n", argv[1]);
        return 2;
    }

    // create a buffer
    BYTE buffer[FAT];
    int fcount = -1;
    char pic_name[8];
    FILE *output;

    while (fread(buffer, FAT, 1, input))
    {
        // check if the buffer started with the 04 signed digits of jpeg
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xe0) == 0xe0)
        {
            // if it's not the first picture, we need to close the connection 
            // to create a new image.
            if (fcount > -1)
            {
                fclose(output);
            }
            fcount++;
            sprintf(pic_name, "%03i.jpg", fcount);
            output = fopen(pic_name, "w");
            if (output == NULL)
            {
                fclose(input);
                printf("Could not create %s.\n", pic_name);
                return 3;
            }
        }
        if (fcount > -1)
        {
            fwrite(buffer, FAT, 1, output);
        }
    }
    fclose(input);
    fclose(output);
    return 0;
}