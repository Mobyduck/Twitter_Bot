# Title: Lenda dos Infinitos
# Author: Paulo Belato
# version: 0.6
# About: A test twitter bot that tweets all the lines from the translated
# file of Endless Legend, once every 2 hours.

def split_sentence(sentence, max_char=280):
    if sentence == '':
        return False

    new_sentences = [''] # a list to store our new sentences
    words = sentence.split() # a list to store all the words in the sentence
    cur_sentence = 0
    for i in range(len(words)):
        limit = len(new_sentences[cur_sentence]) + len(words[i])
        if limit >= (max_char -3): # If the limit is about to be reached, start new sentence
            new_sentences[cur_sentence] += '...'
            cur_sentence += 1
            new_sentences.append('...')

        new_sentences[cur_sentence] += words[i]
        new_sentences[cur_sentence] += ' '

    return new_sentences


def get_line(file, index=1):
    global main_index
    '''All this function does is return me the line I want from
    the file I opened.'''
    with open(file, 'rt', encoding='utf-8') as f:
        for i in range(index): # Go through each line until we get to the one we want
            data_file = f.readline()

        while data_file.isspace(): # Skip blank lines
            main_index += 1
            data_file = f.readline()

    return data_file


def parse_quotes(file, index=3):
    global main_index
    '''This function parses the given .xml line and returns
    whatever is inside the code: "<'example'>String to be returned<'/example'>"
    The index value equals to the line to be read'''
    data_file = get_line(file, index)
    while data_file.count('<') <= 1:
        main_index += 1
        data_file += get_line(file, (main_index))

    first_sep = data_file.partition('>') # Remove everything before the first '>'
    final_sep = first_sep[2].partition('<') # Remove everything after the second '<'

    return final_sep[0]


import tweepy
import time

CONSUMER_KEY = '***'
CONSUMER_SECRET = '***'
ACCESS_TOKEN = '***'
ACCESS_TOKEN_SECRET = '***'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

running = True

# Initiate by grabbing the index from the file
with open("my_index.txt", 'rt') as f:
    my_index = f.readline()
main_index = int(my_index) # line to start at

max_size = 280 # max amount of chars for a tweet
while running:
    twit = parse_quotes("endless_legend_pt.xml", main_index)
    # We need to check how long it is, and split if necessary
    if len(twit) > 280:
        split_twit = split_sentence(twit)
        for i in range(len(split_twit)):
            if split_twit == '':
                break
            api.update_status(split_twit[i])
            time.sleep(60)
    else:
        api.update_status(twit)

    main_index += 1
    # Save the index of the next tweet in the file
    with open("my_index.txt", 'wt') as f:
        f.write(str(main_index))
    time.sleep(3600)
