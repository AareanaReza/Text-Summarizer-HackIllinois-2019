import numpy as np
import gensim
import string
from gensim.parsing.preprocessing import STOPWORDS
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import string

def strip_punctuation(str):
    return str.translate({ord(c):'' for c in string.punctuation})

def split_article(article):
    article = strip_punctuation(article).lower()
    return article.split()

article_title = "Sustainability Operations"
article = "At Caterpillar, sustainability begins within our own operations. We have established high performance standards for environment, health and safety at our facilities that extend beyond compliance with laws and regulations. Proactive implementation of these standards demonstrates our commitment to sustainability leadership in our industry. We are dedicated to the safety of everyone at Caterpillar. We promote the health and safety of our people with policies and proactive programs that help individuals stay safe, personally and professionally. We develop our products, manufacturing processes, training programs and customer assistance programs to minimize safety risks because the safety of our operations and the unique capabilities of our employees ensure the long-term success of our enterprise. As well, our facilities have been working to minimize the environmental impact of our operations, including a focus on energy conservation, greenhouse gas emissions reductions, water conservation and waste reduction. Our Environment, Health and Safety (EHS) Professionals play a key role in providing expertise and support to Caterpillar operations around the world. They have teamed with Caterpillar leadership to drive tremendous improvement and heightened awareness of the importance of EHS across our enterprise. Employees of Team Caterpillar are engaged in identifying and managing risk and are active participants in continuously improving the environment, health and safety of our operations."

 def preprocess(article):
    result = []
    for token in split_article(article):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(token)
    return result

new_article = preprocess(article)
nltk.pos_tag(new_article)