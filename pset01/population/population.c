#include <cs50.h>
#include <stdio.h>

int MIN_SIZE = 9;

int main(void)
{
    // TODO: Prompt for start size
    int population_size;
    do
    {
        population_size = get_int("Start size:");
    } while (population_size < MIN_SIZE);

    // TODO: Prompt for end size
    int target_size;
    do
    {
        target_size = get_int("End size:");
    } while (target_size < population_size);

    // TODO: Calculate number of years until we reach threshold
    int growth;
    int years = 0;
    while (population_size < target_size)
    {
        growth = population_size / 3 - population_size / 4;
        population_size += growth;
        years += 1;
    }

    // TODO: Print number of years
    printf("Years: %i\n", years);
}