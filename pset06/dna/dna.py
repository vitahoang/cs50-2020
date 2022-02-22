import csv
import sys


def main():
    """main
    """

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py CSVfile DNAsequence")
        sys.exit()
    # Read database file into a variable
    with open(sys.argv[1], "r", newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        dna_subsequence = next(csvreader)
        dna_subsequence.pop(0)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r", newline='', encoding='utf-8') as seq:
        dna_sequence = seq.read()

    # Find longest match of each STR in DNA sequence
    strs = {}
    for subsequence in dna_subsequence:
        strs[subsequence] = longest_match(dna_sequence, subsequence)

    # Check database for matching profiles
    with open(sys.argv[1], "r", newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        profiles = list(csvreader)
    print(match_profile(strs, profiles))


def longest_match(sequence, subsequence) -> int:
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters)
        # within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def match_profile(strs, profiles) -> str:
    """Return name of the matching individual"""

    strs_keys = list(strs.keys())
    for profile in profiles:
        flag = bool()
        for key in strs_keys:
            if int(profile[key]) == strs[key]:
                flag = True
            else:
                flag = False
                break
        if flag:
            return profile["name"]
    return "No match"


main()
