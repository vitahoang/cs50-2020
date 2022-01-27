/* includes */
#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* defines */
#define KEYLENGTH 26

/* typedefs */
typedef struct 
{
    char cypher, plain;
} pair;

/* global variable declarations */
string plain_text, cipher_text, input_key;
string lowercase_key = "abcdefghijklmnopqrstuvwxyz";
pair keypair[(KEYLENGTH * 2)];

/* function prototypes */
void encrypt(string input_key);

/* main.c */
int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check if the input_key contains exactly 26 characters
    if (strlen(argv[1]) < 26 || strlen(argv[1]) > 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    
    input_key = argv[1];
    // Check if any dubplicated character in the input_key
    for (int i = 0; i < KEYLENGTH; i++)
    {
        for (int j = i + 1; j < KEYLENGTH; j++)
        {
            if (input_key[i] == input_key[j])
            {
                exit(1);
            }
        }
    }

    // Get plain_text
    plain_text = get_string("plain_text: ");

    // Generate encrypted text 
    cipher_text = (string)malloc(sizeof(plain_text));
    encrypt(plain_text);
    printf("ciphertext: %s\n", cipher_text);
}

/* function declarations */
void encrypt(string text)
{
    for (int i = 0; i < strlen(text); i++)
        switch (text[i])
        {
            case 65 ... 90:
                cipher_text[i] = input_key[(int)text[i] - 65];
                break;
            case 97 ... 122:
                cipher_text[i] = input_key[(int)text[i] - 97];
                break;
            default:
                exit(1); 
        }
}