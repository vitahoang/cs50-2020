/* includes */
#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/* defines */
#define KEYLENGTH 26

/* typedefs */
typedef struct pairthekey
{
    char key, value;
} pair;

/* global variable declarations */
string plaintext, ciphertext, public_key;
string private_key = "abcdefghijklmnopqrstuvwxyz";
pair keypair[(KEYLENGTH * 2)];

/* function prototypes */
void encrypt(string key);
void *combine(string);

/* main.c */
int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(argv[1]) < 26 || strlen(argv[1]) > 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Parse the input to string variable
    public_key = argv[1];

    printf("Public key: %s\n", public_key);
    for (int i = 0; i < strlen(public_key); i++)
    {
        printf("Public key letter %i: %c\n", i + 1, public_key[i]);
    }
    puts("-----------");

    // combine to the key pair
    combine(public_key);
    for (int i = 0; i < KEYLENGTH * 2; i++)
    {
        printf("Key: %c - Value: %c\n", keypair[i].key, keypair[i].value);
    }
    puts("-----------");

    // Get plaintext
    plaintext = get_string("plaintext: ");
    ciphertext = (string)malloc(sizeof(plaintext));
    for (int i = 0; i < strlen(ciphertext); i++)
    {
        printf("ciphertext no.%i: %c\n", i, ciphertext[i]);
    }

    encrypt(plaintext);
    printf("ciphertext: %s\n", ciphertext);

    puts("-----------");
    for (int i = 0; i < strlen(ciphertext); i++)
    {
        printf("ciphertext no.%i: %c\n", i, ciphertext[i]);
    }
}

/* function declarations */
void *combine(string key)
{
    // pair * ptkey;
    // ptkey = keypair;
    for (int i = 0; i < KEYLENGTH; i++)
    {
        for (int j = 0; j < KEYLENGTH * 2; j++)
        {
            if (key[i] == keypair[j].key)
            {
                exit(1);
            }
        }

        switch (key[i])
        {
            // key character is uppercase
            case 65 ... 90:
                keypair[i].key = key[i];
                keypair[i].value = private_key[i] - 32;
                keypair[i + 26].key = key[i] + 32;
                keypair[i + 26].value = private_key[i];
                break;
            // key character is lowercase
            case 97 ... 122:
                keypair[i + 26].key = key[i];
                keypair[i + 26].value = private_key[i];
                keypair[i].key = key[i] - 32;
                keypair[i].value = private_key[i] - 32;
                break;
            default:
                exit(1);
        }
    }
    return 0;
}

void encrypt(string a)
{
    for (int i = 0; i < strlen(a); i++)
        switch (a[i])
        {
            case 65 ... 90:
                for (int j = 0; j < 26; j++)
                {
                    if (a[i] == keypair[j].value)
                    {
                        ciphertext[i] = keypair[j].key;
                        break;
                    }
                }
                break;
            case 97 ... 122:
                for (int j = 26; j < 52; j++)
                {
                    if (a[i] == keypair[j].value)
                    {
                        ciphertext[i] = keypair[j].key;
                        break;
                    }
                }
                break;
            default:
                ciphertext[i] = a[i];
        }
}