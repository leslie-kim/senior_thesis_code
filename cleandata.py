import requests
from bs4 import BeautifulSoup
import csv
import json
import nltk 
from nltk.corpus import stopwords, words, wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import heapq
from collections import Counter
from nltk.util import ngrams, bigrams, trigrams
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder, QuadgramCollocationFinder
from nltk.tag import pos_tag
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import re
from collections import defaultdict





# articles is a list of article : dict
def write_new_file(fn, articles : list): 
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f,['title','link', 'text'])
        w.writeheader()
        for article in articles:
            w.writerow(article)





def clean_data(filename): 

    articles = []

    pattern = r'[^a-zA-z0-9\s]'

    links = set()
    extras = set()
    dup_count_links, dup_count_extras, notext_counts=0, 0, 0

    fn = 'data/'+str(filename)+'.csv'


    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)


        for row in reader: 
            # print(row[1])
            
            if row[2]=='text': continue  # first row 
            if not row[0]: continue # empty row 


            #=========a regular article row========
            if 'https://' in row[1]:
                if row[1] in links:         # get rid of duplicates
                    print('duplicate found:', row[1])
                    dup_count_links+=1
                    continue

                if row[2]=='NO TEXT FOUND' or not row[2]: #get rid of broken links and non-top domains 
                    notext_counts+=1
                    continue

                links.add(row[1])

                # get rid of non-alphanumeric characters
                text = re.sub(pattern, '', row[2])
                articles.append({'title': row[0], 'link': row[1], 'text': text})


            #=========an excessive character row========
            else: 
                if row[0] in extras:         # get rid of duplicates
                    dup_count_extras+=1
                    print('dup extra', row[0])
                    continue

                extras.add(row[0])

                # get rid of non-alphanumeric characters
                text = ''.join(row)
                text = re.sub(pattern, '', text)
                articles.append({'title': text, 'link': '', 'text': ''})    # if its too long it goes onto next line
                

    new_fn = 'cleaned/'+ str(filename)+'_cleaned'+'.csv'
    write_new_file(new_fn, articles)

    print('dup count links', dup_count_links)
    print('dup count extras', dup_count_extras)
    print('no text counts', notext_counts)





def clean_part_two(year):
    articles = []

    fn = 'cleaned/'+ str(year) + '_cleaned' + '.csv'
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # pos tag map
    tag_map = defaultdict(lambda : wordnet.NOUN)
    tag_map['J'] = wordnet.ADJ
    tag_map['V'] = wordnet.VERB
    tag_map['R'] = wordnet.ADV

    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)


        for row in reader: 
            # print(row[1])
            
            if row[2]=='text': continue  # first row 
            if not row[0]: continue # empty row 

            #=========a regular article row========
            if 'https://' in row[1]:

                # de-capitalize and get rid of stop words
                text_list = [word.lower() for word in word_tokenize(row[2]) if word.lower() not in stop_words]
                new_text = ' '.join(text_list)

                # lemmatize all words 
                new_text_tokens = [word for word in  word_tokenize(new_text)]
                lemma_text = []
                for token, tag in pos_tag(new_text_tokens): 
                    lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
                    lemma_text.append(lemma)

                articles.append({'title': row[0], 'link': row[1], 'text': ' '.join(lemma_text)})

            #=========an excessive character row========
            else:
                
                # de-capitalize and get rid of stop words
                text = ''.join(row)
                text_list = [word.lower() for word in text.split() if word.lower() not in stop_words]
                new_text = ' '.join(text_list)

                # lemmatize all words
                new_text_tokens = [word for word in  word_tokenize(new_text)]
                lemma_text = []
                for token, tag in pos_tag(new_text_tokens): 
                    lemma = lemmatizer.lemmatize(token, tag_map[tag[0]])
                    lemma_text.append(lemma)

                articles.append({'title': ' '.join(lemma_text), 'link': '', 'text': ''})



    new_fn = 'processed/'+ str(year) + '_processed'+'.csv'
    write_new_file(new_fn, articles)










if __name__ == "__main__":
    for i in range(2009, 2022):
        print('====== starting', i, '==========' )
        clean_part_two(str(i))
