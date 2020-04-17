from sys import argv, exit
import re
import csv

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Command line paths to files
db_path = argv[1]
seq_path = argv[2]

# Parse csv files into a dictionary
db_list = []                                # Create a list of the different STRs to be placed in the sequence dictionary
db_file = csv.DictReader(open(db_path))
for row in db_file:
    db_list = db_file.fieldnames

# Remove first column "names" as it's redundant for the sequence dictionary
db_list.pop(0)

# Read DNA Sequence text file
seq_dict = {}                               # A dictionary to store STR for comparison
seq_dict = dict.fromkeys(db_list, 1)

seq = open(seq_path, "r")
if seq.mode == "r":
    contents = seq.read()

# copy the list in a dictionary where the genes are the keys
for item in db_list:
    seq_dict[item] = 1

# iterate trough the dna sequence, when it finds repetitions of the values from sequence dictionary it counts them
for key in seq_dict:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(contents)):
        # after having counted a sequence it skips at the end of it to avoid counting again
        while temp > 0:
            temp -= 1
            continue

        # if the segment of dna corresponds to the key and there is a repetition of it we start counting
        if contents[i: i + l] == key:
            while contents[i - l: i] == contents[i: i + l]:
                temp += 1
                i += l

            # it compares the value to the previous longest sequence and if it is longer it overrides it
            if temp > tempMax:
                tempMax = temp

    # store the longest sequences in the dictionary using the correspondent key
    seq_dict[key] += tempMax

# open and iterate trough the database of people treating each one like a dictionary so it can compare to the sequences one
with open(db_path, newline='') as peoplefile:
    people = csv.DictReader(peoplefile)
    for person in people:
        match = 0
        # compares the sequences to every person and prints name before leaving the program if there is a match
        for contents in seq_dict:
            if seq_dict[contents] == int(person[contents]):
                match += 1
        if match == len(seq_dict):
            print(person['name'])
            exit()

    print("No match")