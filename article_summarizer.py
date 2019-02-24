import string
import gensim
import nltk
import string
import numpy as np

# Using Beautiful Soup library to web scrape sciencedaily.com
from bs4 import BeautifulSoup

# Certification required for Http request
import certifi
import urllib3

# If downloaded the code below is unnecessary
'''nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')'''

# This is a certification with respect to the url with respect to web scraping
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# This is an extra weight that is added if the word is in the title
title_frequency_bonus = 3
key_words = ["regarding", "concerning", "regard", "concern", "on", "displays", "predict", "how", "for", "about"]
original_phrase_list = []


# cleans the string - strips all punctuation, trims leading/trailing whitespace, and converts to lowercase
def clean_string(str):
    str = str
    return str.translate({ord(c): '' for c in string.punctuation}).lower()


# returns true if the word is considered a stop word
def is_stop_word(word):
    return word in gensim.parsing.preprocessing.STOPWORDS or len(word) <= 2


# returns a list of possible topics - words that appear directly after a keyword or words in the title
def find_possible_topics(article_words, key_words, title_words):
    possible_topics = []
    for word in title_words:
        if not is_stop_word(word):
            possible_topics.append(word)

    for i in range(len(article_words)):
        if article_words[i] in key_words and article_words[i + 1] not in possible_topics and not is_stop_word(
                article_words[i]):
            possible_topics.append(article_words[i + 1])
    return possible_topics


# This removes all the stopwords
def clean_words(article_words):
    possible_words = []
    for i in range(len(article_words)):
        if article_words[i] is not is_stop_word(article_words[i]):
            possible_words.append(article_words[i])
    return possible_words


# prints the final result
def print_results(frequencies, title, article):
    if get_frequency(remove_stop_words_within_pos_phrase_array(clean_phrase_list(make_sentence_list(article))), article, title) != "":
        return "This article covers information about " + frequencies[0][0] + " and " + frequencies[1][0] + "." \
               + "\nThe study is " + get_frequency(remove_stop_words_within_pos_phrase_array(clean_phrase_list(make_sentence_list(article))), article, title) + "."
    elif len(frequencies) > 1:
        return "This article covers information about " + frequencies[0][0] + " and " + frequencies[1][0] + "."
    else:
        return "Summary could not be generated"

# returns a list of words that have the part of speech (noun, plural noun, etc.) we'd use in our first summary sentence
def get_valid_summary_words(pos_list):
    valid_words = []
    valid_pos_list = ["NN", "NNS", "NNP", "VBG", "FW"]
    for word in pos_list:
        if word[1] in valid_pos_list:
            valid_words.append(word[0])
    return valid_words


# print options for the first summary sentence for an article
def summarize_article(article_url):

    # Webscraping. Takes in the article url and returns only the text within that article
    url = article_url
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, features="html.parser")
    final_text = ""
    title = soup.find('h1', {'id': 'headline'}).text
    if (soup.find('h2', {'id': 'subtitle'}) is not None):
        title += ". " + soup.find('h2', {'id': 'subtitle'}).text
    # Takes all the <p> tags in the <div> tagged block with id= 'text'
    div = soup.find('div', {'id': 'text'})
    final_text = final_text + soup.find('p', {'id': 'first'}).text
    for p in div.findAll('p'):
        final_text = final_text + p.text

    article = final_text
    title = title

    article_words = article.split()
    title_words = title.split()

    possible_topics = find_possible_topics(article_words, key_words, title_words)
    possible_topics_pos_list = nltk.pos_tag(possible_topics)
    valid_possible_topics = get_valid_summary_words(possible_topics_pos_list)
    frequencies = {}

    # find and save the frequencies of all the words in valid_possible_topics
    for word in valid_possible_topics:
        if word not in frequencies:
            frequencies[word] = article_words.count(word)

    # find and save the frequencies of all words in the title, taking into account a frequency bonus
    # (since words in the title are usually more important)
    for word in title_words:
        if word in valid_possible_topics:
            if word not in frequencies:
                frequencies[word] = max(3, article_words.count(word))
            else:
                frequencies[word] += title_frequency_bonus

    # sort the dictionary in reverse order by frequency (so that the words that occur most will be printed first)
    frequencies = sorted(frequencies.items(),
                         reverse=True,
                         key=lambda x: x[1])

    return print_results(frequencies, title, article)

# This returns a list of sentences. The sentences are split on full stop and semicolon
def make_sentence_list(article):
    sentence_list = article.split('.')
    phrase_list = sentence_list
    for phrase in sentence_list:
        if phrase.__contains__(';'):
            phrase_list.extend(phrase.split(';'))
    return phrase_list

# This returns a list of phrases that contain a key word
def clean_phrase_list(phrase_list):
    pos_phrase_list = []
    for i in range(len(phrase_list)):
        for word in key_words:
            phrase_list[i] = clean_string(phrase_list[i])
            if phrase_list[i].__contains__(" " + word + " "):
                if (word == "how"):
                    pos_phrase_list.append("about ")
                pos_phrase_list.append(word + phrase_list[i].split(" " + word)[1])
    original_phrase_list.extend(pos_phrase_list)
    return pos_phrase_list

# This removes the stop words in phrases
def remove_stop_words_within_pos_phrase_array(pos_phrase_list):
    words_in_phrase_list = []
    for i in range(len(pos_phrase_list)):
        words_in_sentence = pos_phrase_list[i].split()
        words_in_phrase_list.append(clean_words(words_in_sentence))
        words_in_phrase_list[i] = nltk.pos_tag(words_in_phrase_list[i])
        words_in_phrase_list[i] = get_valid_summary_words(words_in_phrase_list[i])
    return words_in_phrase_list

# This gets the frequency of each word in a phrase, totals it to return a weight for each phrase and returns the index
# numbern of that phrase
def get_frequency(words_in_phrase_list, article, title):
    article_words = article.split()
    title_words = title.split()
    frequency_of_phrases = []
    for x in range(len(words_in_phrase_list)):
        count = 0
        for i in range(len(words_in_phrase_list[x])):
            frequencies = {}
            # find and save the frequencies of all the words in valid_possible_topics
            for word in words_in_phrase_list[x][i]:
                if word not in frequencies:
                    frequencies[word] = article_words.count(word)
                    count += article_words.count(word)
        frequency_of_phrases.append(count)
        if len(frequency_of_phrases) > 0:
            return original_phrase_list[frequency_of_phrases.index(max(frequency_of_phrases))]
        return ""

# Example use of code
print(summarize_article("https://www.sciencedaily.com/releases/2019/02/190221141511.htm"))
