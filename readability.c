#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

typedef struct textStruct {
    float sents, words, chars;
    long len;
}StructCount;

StructCount textCounter (string text)
{
    StructCount c;
    c.sents = 0; c.words = 1; c.chars = 0;
    c.len = strlen(text);
    for (int i=0; i <= c.len; i++)
    {
        switch (text[i])
        {
            case '.':
            case '?':
            case '!':
                c.sents++;
        } 
        if (text[i] == ' ')
        {
            c.words++;
        }
        switch ((int) text[i])
        {
            case 65 ... 90:
            case 97 ... 122:
                c.chars++;
        }
    }
    return c;
};

float readLevel (StructCount c)
{
    float L,S,index;
    L = c.chars/c.words*100;
    S = c.sents/c.words*100;
    index = 0.0588 * L - 0.296 * S - 15.8;
    return index;
}

int main(void)
{
    string text;
    do 
    {
        text = get_string("Give me your text: ");
    }while(strlen(text)<1);

    StructCount tc;
    tc = textCounter(text);
    float grade = readLevel(tc);
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    } else
    {
        printf("Grade %.f\n", grade);
    }
}