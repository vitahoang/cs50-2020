/* includes */
#include <cs50.h>
#include <stdio.h>
#include <string.h>

/* typedefs */
typedef struct 
{
    float sents, words, chars;
    long len;
}textstruct;

/* function prototypes */
textstruct textCounter(string text);
float readLevel(textstruct c);

/* main.c */
int main(void)
{
    string text;
    do
    {
        text = get_string("Text: ");
    } while (strlen(text) < 1);

    textstruct tc;
    tc = textCounter(text);
    float grade = readLevel(tc);
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.f\n", grade);
    }
}

/* function declarations */
textstruct textCounter(string text)
{
    textstruct ts;
    ts.sents = 0;
    ts.words = 1;
    ts.chars = 0;
    ts.len = strlen(text);
    for (int i = 0; i <= ts.len; i++)
    {
        switch (text[i])
        {
        case '.':
        case '?':
        case '!':
            ts.sents++;
        }
        if (text[i] == ' ')
        {
            ts.words++;
        }
        switch ((int)text[i])
        {
        case 65 ... 90:
        case 97 ... 122:
            ts.chars++;
        }
    }
    return ts;
};

float readLevel(textstruct ts)
{
    float L, S, index;
    L = ts.chars / ts.words * 100;
    S = ts.sents / ts.words * 100;
    index = 0.0588 * L - 0.296 * S - 15.8;
    return index;
}
