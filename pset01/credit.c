#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Forward Declarations
int ValidateCardLong(int digit_long);
int *Long2Array(long card_no, int digit_long);
int LuhnSum(int *card_no, int c);

// Check if the digits long of the card is valid
int ValidateCardLong(int digit_long)
{
    if (digit_long < 13 || digit_long > 16 || digit_long == 14)
    {
        printf("INVALID\n");
        exit(0);
    }
    return 1;
}

// Convert format of the card number from a long to an array
int *Long2Array(long card_no, int digit_long)
{
    int static card_array[18];
    while (card_no != 0)
    {
        card_array[digit_long - 1] = card_no % 10;
        card_no /= 10;
        digit_long--;
    }
    return card_array;
}

// An algorithm invented by Hans Peter Luhn of IBM to checksum the credit card number
int LuhnSum(int *card_no, int digit_long)
{
    int sum = 0;
    for (int i = digit_long - 2; i >= 0; i -= 2)
    {
        if (card_no[i] * 2 >= 10)
        {
            int x = card_no[i] * 2;
            while (x != 0)
            {
                sum += x % 10;
                x /= 10;
            }
        }
        else
        {
            sum += card_no[i] * 2;
        }
    }
    for (int i = digit_long - 1; i >= 0; i -= 2)
    {
        sum += card_no[i];
    }
    return sum;
}

int main(void)
{
    long card_no = get_long("Number: ");
    int digit_long = floor(log10(card_no)) + 1;

    ValidateCardLong(digit_long);
    int *card_array = Long2Array(card_no, digit_long);

    int sum = LuhnSum(card_array, digit_long);
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        exit(0);
    }

    if (
        digit_long == 15 &&
        card_array[0] == 3 &&
        (card_array[1] == 4 || card_array[1] == 7))
    {
        printf("AMEX\n");
    }
    else if ((digit_long == 13 || digit_long == 16) && card_array[0] == 4)
    {
        printf("VISA\n");
    }
    else if (
        digit_long == 16 &&
        card_array[0] == 5 &&
        (card_array[1] == 1 ||
         card_array[1] == 2 ||
         card_array[1] == 3 ||
         card_array[1] == 4 ||
         card_array[1] == 5))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}