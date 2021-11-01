######################################################################
#   File:    word_suggestion.py
#   Author:  Joseph Morelli
#   Purpose: Given a users input, the program suggests what the
#            next word may be in a sentence by referencing bigrams
#            of a small dataset of messages
######################################################################
from re import sub
from nltk import word_tokenize, ngrams, FreqDist

with open("messages.txt") as f:  # opens text file

    word_bag = []  # initializes empty list for words

    for token in word_tokenize(f.read()):  # reads file line by line
        token = sub("'s|[^a-zA-Z0-9\-]", "", token.lower())  # creates token to be placed in word bag
        word_bag.append(token)  # appends token to word bag

    bigrams = FreqDist(ngrams(word_bag, 2))  # initializes bigram counter

while True:  # while loop to make program continous
    user_in = input("Please enter a word for a suggestion: ").strip().lower()  # await user input and format it to lc

    possible_suggestions = []  # initializes empty list for possible words to suggest
    pair_freq = []  # initializes a list to hold pair frequencies
    pad_words = ["the", "this", "of"]  # list of pad words
    total_usage = 0  # initializes counter for

    for word, freq in bigrams.most_common():  # iterates through all the bigrams by most common
        if user_in == word[0]:  # checks if user input matches any of the words in the first position
            possible_suggestions.append(word[1])  # appends word from second bigram position to suggestions list
            total_usage += freq  # increments total by frequency of pair
            pair_freq.append(freq)  # appends that frequency to list

    if len(possible_suggestions) < 3:  # checks if list of suggestions is less than 3
        suggestions_remain = 3 - len(possible_suggestions)  # calculates how many available suggestions there are
        for i in range(suggestions_remain):  # iterates through the remaining spots
            possible_suggestions.append(pad_words[i])  # appends pad word to suggestions
            pair_freq.append(1)  # appends 1 as a pair frequency for pad word
            total_usage += .01  # increments total by an arbitrary non-zero number since it's an artificial pairing

    pad_counter = 0  # initializes counter for pad words

    for i in range(3):  # iterates through the top 3 suggestions
        confidence = (pair_freq[i] / total_usage) * 100  # calculates the confidence of those suggestions
        if confidence > 10:  # checks if confidence is greater than 65%
            print(f"Your next word might be {possible_suggestions[i]}")  # suggests word
        else:  # if confidence is less than 65%
            print(f"Your next word might be {pad_words[pad_counter]}")  # suggest pad word
            pad_counter += 1  # increment pad counter
