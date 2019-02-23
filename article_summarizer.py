import string
import numpy as np
import gensim
# from gensim.parsing.preprocessing import STOPWORDS
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
import string

def strip_punctuation(str):
    return str.translate(string.maketrans("", ""), string.punctuation)

def find_possible_topics(article_words, key_words):
    possible_topics = []
    for i in range(len(article_words)):
        if article_words[i] in key_words:
            possible_topics.append(article_words[i + 1])
    return possible_topics

def print_results(frequencies):
    sentence_structure = "This article is about... (top word choices) "
    print sentence_structure
    for i in range(min(len(frequencies), 20)):
        print(str(i + 1) + ". " + frequencies[i][0])

def preprocess(article_words):
   result = []
   for word in article_words:
       if word not in gensim.parsing.preprocessing.STOPWORDS and len(word) > 3:
           result.append(word)
   return result

def get_valid_summary_words(pos_list):
    valid_words = []
    valid_pos_list = ["NN", "NNP"]
    for word in pos_list:
        if word[1] in valid_pos_list:
            valid_words.append(word[0])
    return valid_words

def summarize_article(article, title):
    article = strip_punctuation(article).lower()
    title = strip_punctuation(title).lower()

    article_words = article.split()
    title_words = title.split()

    # new_article = preprocess(article_words)
    # print(nltk.pos_tag(new_article))

    key_words = ["for", "regarding", "concerning", "regard", "concern", "on", "displays", "predict", "the"]
    possible_topics = find_possible_topics(article_words, key_words)
    # print(possible_topics)
    possible_topics_pos_list = nltk.pos_tag(preprocess(possible_topics))
    # print(possible_topics_pos_list)
    valid_possible_topics = get_valid_summary_words(possible_topics_pos_list)
    # print()
    # print(valid_possible_topics)
    frequencies = {}

    for word in valid_possible_topics:
        if word not in frequencies:
            frequencies[word] = article_words.count(word)

    for word in title_words:
        if word in valid_possible_topics:
            if word not in frequencies:
                frequencies[word] = max(2, article_words.count(word))
            else:
                frequencies[word] += 2

    frequencies = sorted(frequencies.items(),
                        reverse=True,
                        key=lambda x: x[1])

    print_results(frequencies)


sustainability_title = "Sustainability Operations"
sustainability_article = "At Caterpillar, sustainability begins within our own operations. We have established high performance standards for environment, health and safety at our facilities that extend beyond compliance with laws and regulations. Proactive implementation of these standards demonstrates our commitment to sustainability leadership in our industry. We are dedicated to the safety of everyone at Caterpillar. We promote the health and safety of our people with policies and proactive programs that help individuals stay safe, personally and professionally. We develop our products, manufacturing processes, training programs and customer assistance programs to minimize safety risks because the safety of our operations and the unique capabilities of our employees ensure the long-term success of our enterprise. As well, our facilities have been working to minimize the environmental impact of our operations, including a focus on energy conservation, greenhouse gas emissions reductions, water conservation and waste reduction. Our Environment, Health and Safety (EHS) Professionals play a key role in providing expertise and support to Caterpillar operations around the world. They have teamed with Caterpillar leadership to drive tremendous improvement and heightened awareness of the importance of EHS across our enterprise. Employees of Team Caterpillar are engaged in identifying and managing risk and are active participants in continuously improving the environment, health and safety of our operations."

sleep_title = "Sleep apnea: Daytime sleepiness might help predict cardiovascular risk"
sleep_article = "A recent study categorizing people with obstructive sleep apnea based on their differing symptoms found a strong link between excessive daytime sleepiness and cardiovascular disease. Obstructive Sleep Apnea (OSA) causes sporadic airflow blockages during sleep. All of the different types of sleep apnea, OSA is the most common. Symptoms include snoring, daytime sleepiness, difficulty concentrating, and high blood pressure.OSA occurs when the throat muscles relax too much to keep the airway open. When these breathing pauses occur, the oxygen level in the blood gets low, and these frequent bouts of low oxygen levels during sleep may damage the blood vessels that supply the heart. During these pauses, the heart beats faster and the blood pressure goes up. Severe OSA can also cause the heart to become enlarged. When this occurs, the heart receives less oxygen and works less efficiently. Previous studies have identified a link between OSA and heart disease. However, to understand the association better, researchers categorized people with OSA based on their symptoms and conducted a new study. Excessive sleepiness: A marker of risk? The researchers categorized the participants into four subtypes of OSA according to the symptoms they reported, which included: difficulty falling and staying asleep, snoring, fatigue, drowsy driving, disturbed sleep, moderate sleepiness, and excessive sleepiness. The four subtypes were: those with disturbed sleep, those with few symptoms, those who felt moderately sleepy, those who felt excessively sleepy. The study analyzed data from more than 1,000 adults who had moderate to severe OSA (which the scientists defined as having at least 15 breathing pauses while sleeping or reduced breathing). All had participated in the Sleep Heart Health Study, which was available from the National Sleep Research Resource. The team followed the participants for about 12 years. Multiple studies from our group, explains study co-author Dr. Diego Mazzotti, at the University of Pennsylvania in Philadelphia, have shown that patients with moderate to severe OSA throughout the world can be categorized into specific subtypes based on their reported symptoms. However, he notes, until now, it was unclear whether these subtypes had different clinical consequences, especially in regard to future cardiovascular risk. A surrogate marker. The analysis showed that participants with OSA who experienced excessive sleepiness had higher rates of cardiovascular disease at enrollment when compared with people without OSA. Also, they were around twice as likely to experience cardiovascular issues during the follow-up period. The researchers are aware that these results do not prove that excessive sleepiness is a causal factor for cardiovascular disease. That said, they do believe that this specific symptom of OSA could be a surrogate marker of underlying cardiovascular risk pathways. Despite the study's limitations, the team suggests that treatments for OSA, such as continuous positive airway pressure (CPAP), should focus on people who have the excessive sleepiness subtype, as they would benefit the most. CPAP uses machines that keep airways open to allow people to breathe properly during sleep."

sci_daily_title = "Fungus from the intestinal mucosa can affect lung health. Our microbiome can impair our immune system through the harmless fungus Candida albicans"
sci_daily_article = "The composition of the microbiome -- the countless bacteria, fungi and viruses that colonize our body surface, skin, intestines or lungs -- makes a decisive contribution to human health or disease. However, biological mechanisms that cause inflammations in the microbiome are still largely unknown. Together with a group of researchers from the University of Kiel and the University Hospital of Schleswig-Holstein, Professer Dr. Oliver Cornely (head of the Center of Excellence for Invasive Fungal Diseases at Cologne University Hospital) has deciphered a mechanism by which specific intestinal microbiota amplify inflammatory reactions in the lungs. The results of the study, published in Cell, could accelerate the development of new therapies for common diseases. 'The fungus Candida albicans, which colonizes the intestines, skin and mucous membranes, is actually harmless', Cornely said. 'However, our study has shown that Candida albicans affects the balance of our immune system.' Candida albicans stimulates the immune system to produce specific defence cells, so-called Th17 cells. However, some of these Th17 cells then attack other fungi, such as Aspergillus fumigatus. This phenomenon is called cross-reactivity. The research showed that immune-compromised individuals have an increased level of cross-reactive Th17 cells in their lung tissue. This concentration is associated with a deterioration of these patients' health. The protective Th17 reaction in the intestine seems to amplify pathogenic immune processes in the lungs. 'With this observation, we were able to show for the first time how a single member of the microbiome, Candida albicans, influences the specific immune response to a large group of other microbes. Immune cross-reactivity is probably a common mechanism by which the microbiome manipulates the immune system -- with both protective and harmful effects', Cornely remarked. Deciphering such specific effects of individual microbes will in future contribute to the development of targeted therapies."

summarize_article(sustainability_article, sustainability_title)
summarize_article(sleep_article, sleep_title)
summarize_article(sci_daily_article, sci_daily_title)

# new_article = preprocess(sci_daily_article)
# nltk.pos_tag(new_article)
