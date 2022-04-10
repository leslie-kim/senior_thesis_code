from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import sys
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.tokenize import word_tokenize




def measure_sentiment(fn):
    fn = 'processed/' + str(fn) + '_processed.csv'

    sia = SentimentIntensityAnalyzer()

    last_text = None
    count = 0
    pos, neg, neu, comp = 0, 0, 0, 0
    added = 0


    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)

        for row in reader: 

            count+=1

            if row[2]=='text': continue  # first row
            if not row[0]: continue # empty row 


            
            #=======corner case, always going to be regular article
            if count==2: 
                last_text=row[2]
                continue

            
            #=========a regular article row========
            if 'https://' in row[1]:                # need to hold off on calculating row until we hit next row

                res = sia.polarity_scores(last_text) 

                pos += res['pos']
                neg += res['neg']
                neu += res['neu']
                comp += res['compound']

                # if res['compound'] > 0.05: 
                #     if res['compound']>pos_score and len(last_text) < 1000: 
                #         pos_score=res['compound']
                #         most_pos = last_text
                #         pos_link = row[1]
                # elif res['compound'] < -0.05 and len(last_text) < 1000: 
                #     if res['compound']<neg_score: 
                #         neg_score=res['compound']
                #         most_neg = last_text
                #         neg_link = row[1]
                # else: 
                #     pass

                added+=1
                last_text = row[2]
                

            #=========an excessive character row========
            else:

                last_text += row[0]

    return pos, neg, neu, comp, added





def make_wordcloud(year):

    bank = {'say', 'would', 'go', 'one', 'two', 'make', 'take', 'also', 'many', 'get', 'like',  'think', 'could', \
     'even', 'u', 'mr', 'new', 'york', 'time', 'give',  'year', 'come', 'day', 'may', 'percent', 'call', 'know', 'm', \
     'way', 'week', 'last', 'see', 'use', 'page', 'include', 'write', 'become', 'ing', 'abor', 'tion', 'three', 'per', \
     'cent', 'seem', 'ask', 'first', 'another', 'though', 'well', 'find', 'tell', 'part', 'report', 'without', 'tions', \
    'tell', 'begin', 'little', 'million', 'yesterday', 'still' \
     }

    pos_text = ''
    neg_text = ''
    last_text = None
    count = 0
    sia = SentimentIntensityAnalyzer()

    fn = 'processed/' + str(year) + '_processed.csv'

    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)

        for row in reader: 

            count+=1

            if row[2]=='text': continue  # first row
            if not row[0]: continue # empty row 

            #=======corner case, always going to be regular article
            if count==2: 
                last_text=row[2]
                continue
            
            #=========a regular article row========
            if 'https://' in row[1]:                # need to hold off on calculating row until we hit next row

                res = sia.polarity_scores(last_text) 
                to_add = [word for word in word_tokenize(last_text) if word not in bank]

                if res['compound'] > 0.05: # pos text 
                    pos_text += ' '.join(to_add)
                elif res['compound'] < -0.05: 
                    neg_text += ' '.join(to_add)

                last_text=row[2]

                
            #=========an excessive character row========
            else:
                last_text += row[0]


    # Create and generate a word cloud image:
    print(len(pos_text), len(neg_text))
    wordcloud = WordCloud(background_color='white').generate(pos_text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    wordcloud = WordCloud(background_color='white').generate(neg_text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    








if __name__ == "__main__":

    # make_wordcloud(1970)

    # mn, ns = None, 100
    # mp, ps = None, -100
    # pl, nl = '', ''

    for i in range(1970, 2022):
        pos, neg, neu, comp, total = measure_sentiment(i)

        print(round(pos/total, 5), ',', round(neg/total, 5), ',', round(neu/total, 5), ',', round(comp / total, 5))

        # if pos_score>ps: 
        #     ps=pos_score
        #     mp = most_pos
        #     pl = pos_link
        # if neg_score<ns:
        #     ns=neg_score
        #     mn = most_neg
        #     nl = neg_link

    # print(mp, ps, pl)
    # print(mn, ns, nl)

