/* includes */
#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* defines */
#define KEYLENGTH 26

/* typedefs */
typedef struct KeyPair
{
    char cypher, plain;
} pair;

/* global variable declarations */
string plain_text, cipher_text, input_key;
string lowercase_key = "abcdefghijklmnopqrstuvwxyz";
pair keypair[(KEYLENGTH * 2)];

/* function prototypes */
void encrypt(string input_key);
void *combineKey(string);

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

    // Combime uppercase and lowercase characters of input_key to create a 
    // keypair
    combineKey(input_key);

    // Get plain_text
    plain_text = get_string("plain_text: ");

    // Generate encrypted text 
    cipher_text = (string)malloc(sizeof(plain_text));
    encrypt(plain_text);
    printf("ciphertext: %s\n", cipher_text);
}

/* function declarations */
void *combineKey(string input_key)
{
    for (int i = 0; i < KEYLENGTH; i++)
    {
        // Check if any dubplicated character in the input_key
        for (int j = 0; j < KEYLENGTH * 2; j++)
        {
            if (input_key[i] == keypair[j].cypher)
            {
                exit(1);
            }
        }

        switch (input_key[i])
        {
        // input_key character is uppercase
        case 65 ... 90:
            keypair[i].cypher = input_key[i];
            keypair[i].plain = lowercase_key[i] - 32;
            keypair[i + 26].cypher = input_key[i] + 32;
            keypair[i + 26].plain = lowercase_key[i];
            break;
        // input_key character is lowercase
        case 97 ... 122:
            keypair[i + 26].cypher = input_key[i];
            keypair[i + 26].plain = lowercase_key[i];
            keypair[i].cypher = input_key[i] - 32;
            keypair[i].plain = lowercase_key[i] - 32;
            break;
        default:
            exit(1);
        }
    }
    return 0;
}

void encrypt(string text)
{
    for (int i = 0; i < strlen(text); i++)
        switch (text[i])
        {
        case 65 ... 90:
            for (int j = 0; j < 26; j++)
            {
                if (text[i] == keypair[j].plain)
                {
                    cipher_text[i] = keypair[j].cypher;
                    break;
                }
            }
            break;
        case 97 ... 122:
            for (int j = 26; j < 52; j++)
            {
                if (text[i] == keypair[j].plain)
                {
                    cipher_text[i] = keypair[j].cypher;
                    break;
                }
            }
            break;
        default:
            cipher_text[i] = text[i];
        }
}