#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int *Long2Array(long n, int c)
{
    static int array[30];
    while (n != 0)
    {
        array[c - 1] = n % 10;
        n /= 10;
        c--;
    }
    return array;
}

int CheckLuhn(int *a, int c)
{
    int sum = 0;
    for (int loop = (c - 1); loop >= 0; loop -= 2)
    {
        sum = sum + a[loop];
    }
    for (int loop = (c - 2); loop >= 0; loop -= 2)
    {
        if (a[loop] > 4)
        {
            int x = a[loop] * 2;
            while (x != 0)
            {
                sum = sum + x % 10;
                x /= 10;
            }
        }
        else
        {
            sum = sum + (a[loop] * 2);
        }
    }
    return sum;
}

int main(void)
{
    long card_n = get_long("Please give me your credit card number: ");
    int card_l = floor(log10(card_n)) + 1;
    if (card_l < 13 || card_l > 16 || card_l == 14)
    {
        printf("INVALID\n");
        exit(0);
    }
    else
    {
        int *card_array = Long2Array(card_n, card_l);
        int check_n = CheckLuhn(card_array, card_l);
        if (check_n % 10 == 0)
        {
            if (card_l == 15 && card_array[0] == 3)
            {
                if (card_array[1] == 4 || card_array[1] == 7)
                {
                    printf("AMEX\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else if (card_l == 13)
            {
                if (card_array[0] == 4)
                {
                    printf("VISA\n");
                }
                else
                {
                    printf("INVALID\n");
                }
            }
            else
            {
                if (card_array[0] == 4)
                {
                    printf("VISA\n");
                }
                else if (card_array[0] == 5)
                {
                    if (card_array[1] > 0 && card_array[1] < 6)
                    {
                        printf("MASTERCARD\n");
                    }
                    else
                    {
                        printf("INVALID\n");
                    }
                }
                else
                {
                    printf("INVALID\n");
                }
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
}
