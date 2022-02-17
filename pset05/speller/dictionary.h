// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Prototypes

void tableInit();
bool check(char *word);
unsigned int hash(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);
bool tableInsert(node *table[], int id, node *w);
bool bucketInsert(node *w_cur, node *w_next);
bool bucketUnload(node *w);
bool bucketCheck(node *w, const char *word);
char *strToLower(char *s);

#endif // DICTIONARY_H
