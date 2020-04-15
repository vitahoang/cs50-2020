#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct candidate
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        printf("%s %i\n", candidates[i].name, candidates[i].votes);
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");
        for (int x = 0; x < strlen(name); x++)
        {
            printf("%c\n", name[x]);
        }
        vote(name);
        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    bool a;
    for (int i=0; i < MAX; i++)
    {
        if (candidates[i].name == name)
        {
            candidates[i].votes++;
            a = true;
            break;
        }
        else a = false;
    }
    return a;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    string winner_name[MAX];
    winner_name[0] = candidates[0].name;
    int votes_max = candidates[0].votes, pcount = 0;
    for (int i=1; i < MAX; i++)
    {
        if (votes_max < candidates[i].votes)
        {
            votes_max = candidates[i].votes;
            pcount = 0;
            winner_name[0] = candidates[i].name;
        }
        if (votes_max == candidates[i].votes)
        {
            pcount++;
            winner_name[pcount] = candidates[i].name;
        }
    }
    for (int i=0; i <= pcount; i++)
    {
        printf("%s\n",winner_name[i]);
    }
    return;
}

