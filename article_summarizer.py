import string
import gensim
import nltk
import string
import numpy as np

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

max_number_of_results = 10
title_frequency_bonus = 3
key_words = ["for", "regarding", "concerning", "regard", "concern", "on", "displays", "predict", "how"]


# cleans the string - strips all punctuation, trims leading/trailing whitespace, and converts to lowercase
def clean_string(str):
    # return str.translate({ord(c): '' for c in string.punctuation})
    return str.translate(string.maketrans("", ""), string.punctuation).strip().lower()


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
        if article_words[i] in key_words and article_words[i + 1] not in possible_topics and not is_stop_word(word):
            possible_topics.append(article_words[i + 1])
    return possible_topics


def clean_words(article_words):
    possible_words = []
    for i in range(len(article_words)):
        if article_words[i] is not is_stop_word(article_words[i]):
            possible_words.append(article_words[i])
    return possible_words


# prints the top 10 results for words to complete the first summary sentence
def print_results(frequencies):
    sentence_structure = "This article is about... (top word choices) "
    print(sentence_structure)
    for i in range(min(len(frequencies), 10)):
        print(str(i + 1) + ". " + frequencies[i][0])

    print("This article covers information about " + frequencies[0][0] + " and " + frequencies[1][0] + ".")


# returns a list of words that have the part of speech (noun, plural noun, etc.) we'd use in our first summary sentence
def get_valid_summary_words(pos_list):
    valid_words = []
    valid_pos_list = ["NN", "NNS", "NNP", "VBG", "FW"]
    for word in pos_list:
        if word[1] in valid_pos_list:
            valid_words.append(word[0])
    return valid_words


def make_word_pairs(possible_topics):
    pairs = []
    for i in range(len(possible_topics)):
        pairs.append(possible_topics[i] + " " + possible_topics[i + 1])
    return pairs


# print options for the first summary sentence for an article
def summarize_article(article, title):
    article = clean_string(article)
    title = clean_string(title)

    article_words = article.split()
    title_words = title.split()

    possible_topics = find_possible_topics(article_words, key_words, title_words)
    possible_topics_pos_list = nltk.pos_tag(possible_topics)
    # print(possible_topics_pos_list)
    # possible_topics_pos_list.extend(make_word_pairs(possible_topics))
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
                frequencies[word] += 3

    # sort the dictionary in reverse order by frequency (so that the words that occur most will be printed first)
    frequencies = sorted(frequencies.items(),
                         reverse=True,
                         key=lambda x: x[1])

    print_results(frequencies)


def make_phrase_list(article):
    sentence_list = article.split('.')
    phrase_list = sentence_list
    for phrase in sentence_list:
        if phrase.__contains__(';'):
            phrase_list.extend(phrase.split(';'))
    return phrase_list


def clean_phrase_list(phrase_list):
    pos_phrase_list = []
    for i in range(len(phrase_list)):
        for word in key_words:
            phrase_list[i] = clean_string(phrase_list[i])
            if phrase_list[i].__contains__(" " + word):
                pos_phrase_list.append(word + phrase_list[i].split(" " + word)[1])
    return pos_phrase_list


def remove_stop_words_within_pos_phrase_array(pos_phrase_list):
    # print(pos_phrase_list)
    words_in_phrase_list = [[]]
    for i in range(len(pos_phrase_list)):
        words_in_sentence = pos_phrase_list[i].split()
        words_in_phrase_list.append(clean_words(words_in_sentence))
        words_in_phrase_list[i] = nltk.pos_tag(words_in_phrase_list[i])
        # print(nltk.pos_tag(words_in_phrase_list[i]))
        words_in_phrase_list[i] = get_valid_summary_words(words_in_phrase_list[i])
    print(words_in_phrase_list)
    return words_in_phrase_list

# sample articles

sustainability_title = "Sustainability Operations"
sustainability_article = "At Caterpillar, sustainability begins within our own operations. We have established high performance standards for environment, health and safety at our facilities that extend beyond compliance with laws and regulations. Proactive implementation of these standards demonstrates our commitment to sustainability leadership in our industry. We are dedicated to the safety of everyone at Caterpillar. We promote the health and safety of our people with policies and proactive programs that help individuals stay safe, personally and professionally. We develop our products, manufacturing processes, training programs and customer assistance programs to minimize safety risks because the safety of our operations and the unique capabilities of our employees ensure the long-term success of our enterprise. As well, our facilities have been working to minimize the environmental impact of our operations, including a focus on energy conservation, greenhouse gas emissions reductions, water conservation and waste reduction. Our Environment, Health and Safety (EHS) Professionals play a key role in providing expertise and support to Caterpillar operations around the world. They have teamed with Caterpillar leadership to drive tremendous improvement and heightened awareness of the importance of EHS across our enterprise. Employees of Team Caterpillar are engaged in identifying and managing risk and are active participants in continuously improving the environment, health and safety of our operations."

sleep_title = "Sleep apnea: Daytime sleepiness might help predict cardiovascular risk"
sleep_article = "A recent study categorizing people with obstructive sleep apnea based on their differing symptoms found a strong link between excessive daytime sleepiness and cardiovascular disease. Obstructive Sleep Apnea (OSA) causes sporadic airflow blockages during sleep. All of the different types of sleep apnea, OSA is the most common. Symptoms include snoring, daytime sleepiness, difficulty concentrating, and high blood pressure.OSA occurs when the throat muscles relax too much to keep the airway open. When these breathing pauses occur, the oxygen level in the blood gets low, and these frequent bouts of low oxygen levels during sleep may damage the blood vessels that supply the heart. During these pauses, the heart beats faster and the blood pressure goes up. Severe OSA can also cause the heart to become enlarged. When this occurs, the heart receives less oxygen and works less efficiently. Previous studies have identified a link between OSA and heart disease. However, to understand the association better, researchers categorized people with OSA based on their symptoms and conducted a new study. Excessive sleepiness: A marker of risk? The researchers categorized the participants into four subtypes of OSA according to the symptoms they reported, which included: difficulty falling and staying asleep, snoring, fatigue, drowsy driving, disturbed sleep, moderate sleepiness, and excessive sleepiness. The four subtypes were: those with disturbed sleep, those with few symptoms, those who felt moderately sleepy, those who felt excessively sleepy. The study analyzed data from more than 1,000 adults who had moderate to severe OSA (which the scientists defined as having at least 15 breathing pauses while sleeping or reduced breathing). All had participated in the Sleep Heart Health Study, which was available from the National Sleep Research Resource. The team followed the participants for about 12 years. Multiple studies from our group, explains study co-author Dr. Diego Mazzotti, at the University of Pennsylvania in Philadelphia, have shown that patients with moderate to severe OSA throughout the world can be categorized into specific subtypes based on their reported symptoms. However, he notes, until now, it was unclear whether these subtypes had different clinical consequences, especially in regard to future cardiovascular risk. A surrogate marker. The analysis showed that participants with OSA who experienced excessive sleepiness had higher rates of cardiovascular disease at enrollment when compared with people without OSA. Also, they were around twice as likely to experience cardiovascular issues during the follow-up period. The researchers are aware that these results do not prove that excessive sleepiness is a causal factor for cardiovascular disease. That said, they do believe that this specific symptom of OSA could be a surrogate marker of underlying cardiovascular risk pathways. Despite the study's limitations, the team suggests that treatments for OSA, such as continuous positive airway pressure (CPAP), should focus on people who have the excessive sleepiness subtype, as they would benefit the most. CPAP uses machines that keep airways open to allow people to breathe properly during sleep."

sci_daily_title = "Fungus from the intestinal mucosa can affect lung health. Our microbiome can impair our immune system through the harmless fungus Candida albicans"
sci_daily_article = "The composition of the microbiome -- the countless bacteria, fungi and viruses that colonize our body surface, skin, intestines or lungs -- makes a decisive contribution to human health or disease. However, biological mechanisms that cause inflammations in the microbiome are still largely unknown. Together with a group of researchers from the University of Kiel and the University Hospital of Schleswig-Holstein, Professer Dr. Oliver Cornely (head of the Center of Excellence for Invasive Fungal Diseases at Cologne University Hospital) has deciphered a mechanism by which specific intestinal microbiota amplify inflammatory reactions in the lungs. The results of the study, published in Cell, could accelerate the development of new therapies for common diseases. 'The fungus Candida albicans, which colonizes the intestines, skin and mucous membranes, is actually harmless', Cornely said. 'However, our study has shown that Candida albicans affects the balance of our immune system.' Candida albicans stimulates the immune system to produce specific defence cells, so-called Th17 cells. However, some of these Th17 cells then attack other fungi, such as Aspergillus fumigatus. This phenomenon is called cross-reactivity. The research showed that immune-compromised individuals have an increased level of cross-reactive Th17 cells in their lung tissue. This concentration is associated with a deterioration of these patients' health. The protective Th17 reaction in the intestine seems to amplify pathogenic immune processes in the lungs. 'With this observation, we were able to show for the first time how a single member of the microbiome, Candida albicans, influences the specific immune response to a large group of other microbes. Immune cross-reactivity is probably a common mechanism by which the microbiome manipulates the immune system -- with both protective and harmful effects', Cornely remarked. Deciphering such specific effects of individual microbes will in future contribute to the development of targeted therapies."

sci_daily_volcano_title = "Do volcanoes or an asteroid deserve blame for dinosaur extinction?"
sci_daily_volcano_article = "Based on new data published today in the journal Science, it seems increasingly likely that an asteroid or comet impact 66 million years ago reignited massive volcanic eruptions in India, half a world away from the impact site in the Caribbean Sea. But it leaves unclear to what degree the two catastrophes contributed to the near-simultaneous mass extinction that killed off the dinosaurs and many other forms of life. The research sheds light on huge lava flows that have erupted periodically over Earth's history, and how they have affected the atmosphere and altered the course of life on the planet. In the study, University of California, Berkeley, scientists report the most precise and accurate dates yet for the intense volcanic eruptions in India that coincided with the worldwide extinction at the end of the Cretaceous Period, the so-called K-Pg boundary. The million-year sequence of eruptions spewed lava flows for distances of at least 500 kilometers across the Indian continent, creating the so-called Deccan Traps flood basalts that in some places are nearly 2 kilometers thick. Now that we have dated Deccan Traps lava flows in more and different locations, we see that the transition seems to be the same everywhere. I would say, with pretty high confidence, that the eruptions occurred within 50,000 years, and maybe 30,000 years, of the impact, which means they were synchronous within the margin of error, said Paul Renne, a professor-in-residence of earth and planetary science at UC Berkeley, director of the Berkeley Geochronology Center and senior author of the study, which will appear online Feb. 21. That is an important validation of the hypothesis that the impact renewed lava flows. The new dates also confirm earlier estimates that the lava flows continued for about a million years, but contain a surprise: three-quarters of the lava erupted after the impact. Previous studies suggested that about 80 percent of the lava erupted before the impact. If most of the Deccan Traps lava had erupted before the impact, then gases emitted during the eruptions could have been the cause of global warming within the last 400,000 years of the Cretaceous Period, during which temperatures increased, on average, about 8 degrees Celsius (14.4 degrees Fahrenheit). During this period of warming, species would have evolved suited to hothouse conditions, only to be confronted by global cooling from the dust or by climate cooling gases caused by either the impact or the volcanos. The cold would have been a shock from which most creatures would never have recovered, disappearing entirely from the fossil record: literally, a mass extinction. But if most of the Deccan Traps lava emerged after the impact, this scenario needs rethinking. This changes our perspective on the role of the Deccan Traps in the K-Pg extinction, said first author Courtney Sprain, a former UC Berkeley doctoral student who is now a postdoc at the University of Liverpool in the United Kingdom. Either the Deccan eruptions did not play a role -- which we think unlikely -- or a lot of climate-modifying gases were erupted during the lowest volume pulse of the eruptions. The hypothesis that climate-altering volcanic gases leak out of underground magma chambers frequently, and not just during eruptions, is supported by evidence from present-day volcanos, such as those of the gas-spewing Mt. Etna in Italy and Popocatepetl in Mexico, the researchers said. Magma stewing below the surface is known to transmit gases to the atmosphere, even without eruptions. We are suggesting that it is very likely that a lot of the gases that come from magma systems precede eruptions; they don't necessarily correlate with eruptions, Renne said. In the case of the K-Pg extinction, the symptoms of significant climate change occurred before the peak in volcanic eruptions. Flood basalts. Renne, Sprain and their colleagues are using a precise dating method, argon-argon dating, to determine when the impact occurred and when the Deccan Traps erupted to clarify the sequence of catastrophes at the end of the Cretaceous Period and beginning of the Tertiary Period -- the K-Pg boundary, formerly referred to as the K-T boundary. In 2013, using rocks from Montana, they obtained the most precise date yet for the impact, and in 2018, they updated that to 66,052,000 years ago, give or take 8,000 years. Then, in 2015, they determined from a handful of samples in India that, in at least one spot, the peak of the Deccan Traps eruptions occurred within about 50,000 years of that date, which means, in geologic time, that the incidents were basically simultaneous. Now, with three times more rock samples from areas covering more of the Deccan Traps, the researchers have established that the time of peak eruptions was the same across much of the Indian continent. This supports the group's hypothesis that the asteroid impact triggered super-earthquakes that caused a strong burst of volcanism in India, which is almost directly opposite the impact site, the Chicxulub crater in the Caribbean Sea. Sprain and Renne argue that the coincident catastrophes likely delivered a one-two punch to life on Earth, but the details are unclear. Volcanic eruptions produce lots of gases, but some, like carbon dioxide and methane, warm the planet, while others, like sulfur aerosols, are cooling. The impact itself would have sent dust into the atmosphere that blocked sunlight and cooled the Earth, though no one knows for how long. Both the impact and Deccan volcanism can produce similar environmental effects, but these are occurring on vastly differing timescales, Sprain said. Therefore, to understand how each agent contributed to the extinction event, assessing timing is key. Which gases in the Deccan Traps are emitted when is a question that's hard to answer, because there are no flood basalt eruptions going on today, despite numerous ones in Earth's history. The most recent, near the Columbia River in the Pacific Northwest, dwindled 15 million years ago after 400,000 years of eruptions. The paucity of information about flood basalts is one reason Renne and Sprain are interested in the Deccan Traps, which are still young enough to contain information about the sequence, effects and scale of the eruptions, and perhaps the cause.It makes we wonder whether we may see some external forcing mechanism, like the impact for the Deccan Traps, for other flood basalts that lead up to major peaks in eruptions, like the Columbia River basalts or the Siberian Traps, Renne said. Could a major earthquake in nearby subduction zones or the accumulation of pressure due to rising magma unleash these major episodes in flood basalts? Sprain noted that, in the same issue of Science, a research group at Princeton University also will publish new dates related to the Deccan Traps, some of which differ from those of the Berkeley group. Whereas the Berkeley group dated the mineral plagioclase from the actual lava flows, the Princeton group dated zircons in the sediment deposited between flows. Because it's unclear where the zircons came from, however, those dates provide only a maximum age for the lava, she said."

# summarize_article(sustainability_article, sustainability_title)
# summarize_article(sleep_article, sleep_title)
summarize_article(sci_daily_article, sci_daily_title)
summarize_article(sci_daily_volcano_article, sci_daily_volcano_title)
print(remove_stop_words_within_pos_phrase_array(clean_phrase_list(make_phrase_list(sci_daily_article))))
