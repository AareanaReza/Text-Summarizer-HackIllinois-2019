# Text Summarizer

Our code takes in a link to an article on Science daily and outputs a summary based on our algorithm. 
We chose this website in particular because we thought that our approach to text summarization would work best
on research articles. It also helped that this website had existing summaries so it shortened the time we took to check our model for accuracy. 
In addition to this, we thought people working in healthcare would benefit a lot from
a text summarizer - it would allow them to better filter which research papers they want to read especially when short 
for time. This would allow them to better customize their care for patients.

Once a link is input, our webscrapper retrieves the title and the text of the article using the 
Beautiful Soup 4 library. This data is then input into the model.

The model uses a fill in the blank approach to text summarization. A word is added to a bag of words if it is next to a key word (these are defined in the code).

The first sentence's blanks are filled with the words that have the highest weight in the bag of words.
The second sentence requires a phrase to be filled in. This is  filled in through a similar method described above.

The selling point of this model is that grammar is less likely to be a problem as most of the grammar is filled out by us.
The model only needs to retrieve words or phrases to fill into already complete sentences.

Another advantage of this model is that it can be adapted to any website with relative ease.


  ### Project Features
  * Beautiful soup
  * HTML and CSS
  * Javascript
  * Python
  * Flask
  * nltk
  * gensim

## USAGE
  * Doctors can save time reading irrelevant articles
  * People with disabilities could benefit by being able process information more efficiently
  * Summarizing medical cases
  * Used in a chatbot to display text summaries to the user
  * Keep track of internal document workflow
  * Question answering and Bots
  * Summarizing emails
  * Patent research
  * Summarizing news articles
  
## BUILD/INSTALLATION INSTRUCTIONS
* Install required libraries
* Fork repository

## OTHER SOURCES OF DOCUMENTATION

## Contributor Guide
CONTRIBUTING.md

## License 

Apache License 2.0.

Copyleft licenses require the derivative works or modified versions of existing software to be released under the same license. The Apache License doesn’t have any such requirements. It’s a permissive license. It permits you to release the modified parts of the code under any license of your choice. However, you are required to release all the unmodified parts of the software under the same license (the Apache License).

Apache License 2.0 is compatible with GPLv3, so you can freely mix the code that’s released under these two licenses. The resulting software, however, must be released under GPLv3