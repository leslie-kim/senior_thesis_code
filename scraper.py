import requests
from bs4 import BeautifulSoup
import csv
import json
import nltk 
nltk.download([
        'stopwords',
        'punkt',
        'averaged_perceptron_tagger',
        'brown',
])
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import heapq
from collections import Counter
from nltk.util import ngrams, bigrams, trigrams
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder, QuadgramCollocationFinder
from nltk.tag import pos_tag
from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
import time
import re




# articles is a list of article : dict
def write_new_file(fn, articles : list): 
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f,['title','link', 'text'])
        w.writeheader()
        for article in articles:
            w.writerow(article)





# takes an empty list called "urls," fills up list with the all article links returned from search 
def get_timesmachine_urls(startdate : str, enddate : str, query : str, urls : list):
    num_articles = 0
    end_reached = False
    ind_last_page = 0
    for i in range(70):  # arbitrary constant denoting max page number

        link = 'https://www.nytimes.com/svc/add/v1/sitesearch.json?fq=(-type_of_material%3Aletter%20AND%20document_format%3Afast%20AND%20(asset_id%3A%2F%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%2B%2F%20OR%20timesmachine_url%3A%5B*%20TO%20*%5D))%20OR%20(_exists_%3Atimesmachine_url)&begin_date='+startdate+'&end_date='+enddate+'&page='+str(i)+'&q='+query+'&sort=oldest'
        r = requests.get(link)
        data = json.loads(r.text)

        response = data['response']
        docs = response['docs'] # list 
        meta = response['meta'] # dict 
        related = response['related'] # list
        if len(docs)==0: 
            end_reached = True
            break
        ind_last_page += 1
        for doc in docs: 
            num_articles += 1
            urls.append(doc['web_url'])
            # print(doc['web_url'])
            # print('web_url:', doc['web_url'])  
            # print('pub_date:', doc['pub_date'])              

    print('STATS')
    print('num articles:', num_articles)
    print('end reached:', end_reached)
    print('last_page:', ind_last_page)





def write_links_to_csv(year):

    articles = []

    for i in range(0, 10000):

        link = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=abortion&begin_date=" + str(year) + "0101&end_date=" + str(year) + "1231&sort=oldest&page=" + str(i) + "&api-key=J8Xs1TzSY7SLGm2RCEgIJztrHYGya9w9"
        r = requests.get(link)
        data = json.loads(r.text)

        if i==0: print('hit_num:', data['response']['meta']['hits'])
        if i % 10==0: print('page', i)

        docs = data['response']['docs']

        if len(docs)==0: 
            print('last page', i) # ran out of results
            break 

        for doc in docs: 
            articles.append({'link': doc['web_url']})

        time.sleep(6)

    fn = str(year) + 'links_only' + '.csv'
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f,['link'])
        w.writeheader()
        for article in articles:
            w.writerow(article)





def get_urls_from_csv(urls, year):
    fn = 'links_only/' + str(year) + 'links_only' + '.csv'
    print('getting urls from ', fn)
    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)

        for row in reader: 
            
            if row[0]=='link': continue
            urls.append(row[0])
    print(len(urls), 'urls found from', fn)
    return urls





# pass in list of links 
def scrape_to_csv(urls : list, filename : str):
    counter, ttl_err, text_err = 0, 0, 0
    articles=[]

    for URL in urls: 

        counter += 1
        if counter % 50==0: 
            print('article', counter, ':', URL)
    
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')

        article = {}

        host = (URL.split('/'))[2]

        # ------- new york times only ----------
        if host == 'www.nytimes.com':
            title = soup.find('span', attrs = {'class':'css-fwqvlz'})
            article['title'] = title.text if title else 'NO TITLE FOUND'
            table = soup.findAll('p', attrs={'class':'css-g5piaz evys1bk0'})  
            text=[]
            for row in table:
                text.append(row.text)
            article['text'] = ' '.join(text) if table else 'NO TEXT FOUND'
            article['link'] = URL
            articles.append(article)

        # --------- top domains only -----------
        elif host in ['thecaucus.blogs.nytimes.com', 'opinionator.blogs.nytimes.com', 'takingnote.blogs.nytimes.com', 'prescriptions.blogs.nytimes.com', 'cityroom.blogs.nytimes.com', \
                        'douthat.blogs.nytimes.com', 'learning.blogs.nytimes.com', 'campaignstops.blogs.nytimes.com',  'thelede.blogs.nytimes.com', 'artsbeat.blogs.nytimes.com', 'parenting.blogs.nytimes.com', \
                        'fivethirtyeight.blogs.nytimes.com', 'empirezone.blogs.nytimes.com', 'kristof.blogs.nytimes.com', 'economix.blogs.nytimes.com', 'rendezvous.blogs.nytimes.com', \
                        'sinosphere.blogs.nytimes.com', 'dotearth.blogs.nytimes.com', 'mediadecoder.blogs.nytimes.com',  'roomfordebate.blogs.nytimes.com', 'afterdeadline.blogs.nytimes.com', \
                        'latitude.blogs.nytimes.com']: 
            title = soup.find('h1', attrs = {'class':'entry-title'})
            article['title'] = title.text if title else 'NO TITLE FOUND'
            table = soup.findAll('p', attrs={'class':'story-body-text'})      
            text=[]
            for row in table:
                text.append(row.text)
            article['text'] = ' '.join(text) if table else 'NO TEXT FOUND'
            article['link'] = URL
            articles.append(article)


        # ----------domains we don't care about ---------
        else:       # we don't want any scraps for other domains 
            article['title'], article['link'], article['text']='NO TITLE FOUND', URL, 'NO TEXT FOUND'
            articles.append(article)


        # error checking increment 
        if article['title']=='NO TITLE FOUND': ttl_err+=1
        if article['text']=='NO TEXT FOUND': text_err+=1
   


    fn = str(filename)+'.csv'
    write_new_file(fn, articles)

    print(ttl_err, 'errored titles')
    print(text_err, 'errored texts')





# computes basic stats on all words given csv file of articles
def stats(year): 

    fn = 'cleaned/' + str(year) + '_cleaned.csv'
    file = open(fn, "r")
    csv_reader = csv.reader(file)

    num_articles=0
    sum_article_length=0
    for row in csv_reader:

        if row[2]=='text': continue
        if not row[0]: continue # empty row 


        #=========a regular article row========
        if 'https://' in row[1]:
            num_articles+=1
            sum_article_length += len(   word_tokenize(row[2])   )

        #=========an excessive character row========
        else:
            sum_article_length += len(    word_tokenize[row[0]]   )

    return num_articles, sum_article_length










if __name__ == "__main__":


    # scrape_to_csv(urls, '1975')

    # sanitize_articles('1970')

    # compute_stats('pre_texas_act')

    # filtered_articles = filter_down('1970')

    # count_per_month('1975')

    # measure_sentiment('1975')
    # year = input().strip()

    # i=1989
    # print('---------------')
    # print('year:', i)
    # # write_links_to_csv(i)
    # urls = []
    # urls = get_urls_from_csv(urls, i)
    # scrape_to_csv(urls, i)

    # for i in range(1970, 2022): 
    #     x, y = stats(i)
    #     print(i, ',', x, ',', y)

    bank = {('new', 'york'), ('per', 'cent'), ('last', 'year'), ('york', 'city'), ('new', 'jersey'), ('united', 'states'),  
            ('year', 'ago'), ('last', 'week'), ('say', 'would'), ('york', 'state'), ('say', 'mr'), ('official', 'say'), }

    sev_list, oct_list, non_list, zero_list, dec_list, vien_list = [], [], [], [], [], []
    for i in range(1970, 1980): 
        sev_list.extend(return_all_words(i, sev_list))
    print('==============len of sev list', len(sev_list))
    bifinder = BigramCollocationFinder.from_words(sev_list)
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])

    for i in range(1980, 1990): 
        oct_list.extend(return_all_words(i, oct_list))
    print('==============len of oct list', len(oct_list))
    bifinder = BigramCollocationFinder.from_words(oct_list)    
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])

    for i in range(1990, 2000): 
        non_list.extend(return_all_words(i, non_list))
    print('==============len of non list', len(non_list))
    bifinder = BigramCollocationFinder.from_words(non_list) 
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])

    for i in range(2000, 2010): 
        zero_list.extend(return_all_words(i, zero_list))
    print('==============len of zero list', len(zero_list))
    bifinder = BigramCollocationFinder.from_words(zero_list) 
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])

    for i in range(2010, 2020): 
        dec_list.extend(return_all_words(i, dec_list))
    print('==============len of dec list', len(dec_list))
    bifinder = BigramCollocationFinder.from_words(dec_list) 
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])

    for i in range(2021, 2022): 
        vien_list.extend(return_all_words(i, vien_list))
    print('==============len of vien list', len(vien_list))
    bifinder = BigramCollocationFinder.from_words(vien_list) 
    res = bifinder.ngram_fd.most_common(30)
    for r in res: 
        if r[0] in bank: 
            continue
        else: 
            print(' '.join(r[0]), ',', r[1])
        
