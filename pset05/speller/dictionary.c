// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <string.h>

#include "dictionary.h"

// TODO: Choose number of buckets in hash table
const unsigned int TABLESIZE = 1000;

// Hash table

node *table[TABLESIZE];
bool if_loaded = false; // True if the table load successfully
int w_count = 0;        // Total number of words in the table

void tableInit()
{
    for (int i = 0; i < TABLESIZE; i++)
    {
        table[i] = NULL;
    }
}

// Hashes word to a number
// Use djb2 hash function (http://www.cse.yorku.ca/~oz/hash.html)
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c);
    }
    return hash % TABLESIZE;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];
    char c;
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Cannot open the file '%s'", dictionary);
        return false;
    }

    node *w = malloc(sizeof(node));
    int id;
    int c_count = 0;

    // Loads each word to the buffer
    while (fread(&c, sizeof(char), 1, dict))
    {
        if (c_count > LENGTH - 1 && c != '\n')
        {
            while (fread(&c, sizeof(char), 1, dict) && isalpha(c))
                ;
            memset(word, '\0', LENGTH + 1);
            c_count = 0;
            continue;
        }
        // Adds word to the table
        if (c == '\n')
        {
            // if (c_count == 1)
            // {
            //     memset(word, '\0', LENGTH + 1);
            //     c_count = 0;
            //     continue;
            // }

            word[c_count] = '\0';
            // Copy string word from the buffer to the node
            strcpy(w->word, word);
            printf("dict: %s\n", w->word);
            w->next = NULL;

            // Adds a new node to the hash table
            id = hash(word);
            if (!tableInsert(table, id, w))
            {
                printf("Fail: Can not insert '%s' to the table\n", word);
                free(w);
                fclose(dict);
                return false;
            }

            // Resets the word
            memset(word, '\0', LENGTH + 1);
            c_count = 0;
            w = malloc(sizeof(node));
            continue;
        }
        word[c_count] = tolower(c);
        c_count++;
    }

    // catch the last word
    if (c_count < LENGTH + 1 && c_count > 0)
    {
        word[c_count] = '\0';
        strcpy(w->word, word);
        w->next = NULL;
        printf("dict: %s\n", word);
        id = hash(word);
        if (!tableInsert(table, id, w))
        {
            printf("Fail: Can not insert '%s' to the table\n", word);
            free(w);
            fclose(dict);
            return false;
        }
        fclose(dict);
        if_loaded = true;
        return true;
    }
    free(w);
    fclose(dict);
    if_loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (!if_loaded)
    {
        return 0;
    }
    return w_count;
}

// Returns true if word is in dictionary, else false
bool check(char *word)
{
    // the word is not in the dictionary if its location is NULL
    int id = hash(word);
    if (table[id] == NULL)
    {
        return false;
    }

    // compare the word if its location is not NULL
    char *l_word = strToLower(word);
    if (strcmp(table[id]->word, l_word) == 0)
    {
        return true;
    }
    // check if there is other words exist in the bucket
    else if (table[id]->next == NULL)
    {
        return false;
    }
    // if there is, search the bucket
    else if (table[id]->next != NULL)
    {
        return bucketCheck(table[id]->next, l_word);
    }
    else
    {
        return false;
    }
}

// Inserts a new node to the has table
bool tableInsert(node *t[], int id, node *w)
{
    if (t[id] == NULL)
    {
        t[id] = w;
        // printf("%i --- id: %i---word: %s\n",w_count, id, t[id]->word);
        w_count++;
        return true;
    }
    // printf("colision---cur_word: %s---=id: %i\n", t[id]->word, id);
    // printf("strcmp = %d\n", strcmp(t[id]->word, w->word));
    if (bucketCheck(t[id], w->word))
    {
        // printf("duplicated\n");
        return true;
    }
    return bucketInsert(t[id], w);
}

// Inserts a new node to a bucket
bool bucketInsert(node *w_cur, node *w_next)
{
    if (w_cur->next == NULL)
    {
        w_cur->next = w_next;
        w_count++;
        return true;
    }
    else
    {
        return bucketInsert(w_cur->next, w_next);
    }
}

// Search a word on a bucket
bool bucketCheck(node *w, const char *word)
{
    // printf("strcmp = %d\n", strcmp(w->word, word));
    if (strcmp(w->word, word) == 0)
    {
        return true;
    }
    if (w->next == NULL)
    {
        return false;
    }
    return bucketCheck(w->next, word);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < TABLESIZE; i++)
    {
        if (!table[i])
        {
            continue;
        }
        else if (table[i] && table[i]->next)
        {
            if (!bucketUnload(table[i]->next))
            {
                return false;
            }
        }
        else
        {
            free(table[i]);
        }
    }
    w_count = 0;
    if_loaded = false;
    return true;
}

// Unload a new node from a bucket
bool bucketUnload(node *w)
{
    if (w->next == NULL)
    {
        free(w);
        return true;
    }
    else if (w->next != NULL)
    {
        return bucketUnload(w->next);
    }
    else
    {
        printf("Cannot unload '%s'\n", w->word);
        return false;
    }
}

// Convert a string to lower case
char *strToLower(char *s)
{
    static char ls[LENGTH + 1];
    int i = 0;
    for (char *p = s; *p; p++)
    {
        ls[i] = tolower(*p);
        i++;
    }
    ls[i] = '\0';
    return ls;
}