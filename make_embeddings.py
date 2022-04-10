from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.decomposition import PCA 
from matplotlib import pyplot
import csv
from nltk.corpus import stopwords
from adjustText import adjust_text
import numpy as np
from numpy import dot
from numpy.linalg import norm










if __name__ == "__main__":

    # bank = {'antiabortion', 'partialbirth', 'infanticide', 'life', 'prolife', 'conception', 'fetus', 'fetal', 'heartbeat', 'murder', 'morality', 'moral', \
    #          'proabortion', 'abortion', 'abortionrights', 'termination', 'right', 'feminism', 'choice', 'prochoice', 'health', 'equality', 'liberation', \
    #         'womb', 'male', 'mother', 'masculinity', 'husband', 'wowomb', 'female', 'abortion', 'femininity', 'wife', 'family', 'child', \
    #         'gender', 'reproduction', 'reproductive', 'sex', 'sexual', 'sexuality', \
    #         'pregnancy', 'pregnant', 'death', 'life', 'birth', 'harm', 'pain', 'birthcontrol', 'contraception', 'iud', 'condom', 'sti', 'pregnant', 'planned', 'unplanned', \
    #         'rape', 'assault', 'harassment', 'incest', 'ivf', 'gestation', 'fertility', 'fecundity', \
    #         'law', 'legal', 'legality', 'adoption', 'miscarriage', 'virgin', 'pure', 'prostitute', 'homosexual', 'homosexuality', 'samesex', \
    #         'married', 'unmarried', 'marriage', 'baby', 'child'
    #         }    
    

    # get training data 
    sent1, sent2, sent3 = [], [], []

    for i in range(1970, 2021):
        # print(i)
        fn = 'processed/' + str(i) + '_processed.csv'
        file = open(fn, "r")
        csv_reader = csv.reader(file)

        for row in csv_reader:

            if row[2]=='text': continue  # first row
            if not row[0]: continue # empty row

            #=========a regular article row========
            if 'https://' in row[1]: 
                for sent in sent_tokenize(row[2]):
                    sent1.append(word_tokenize(sent))
                    sent2.append(word_tokenize(sent))
                    sent3.append(word_tokenize(sent))

            #=========an excessive character row========
            else:
                for sent in sent_tokenize(row[0]):
                    sent1.append(word_tokenize(sent))
                    sent2.append(word_tokenize(sent))
                    sent3.append(word_tokenize(sent))

        if i!=1970 and i%5==0: # train model every five years
            # train model
            mod1 = Word2Vec(sent1, vector_size=300, min_count=5)
            mod2 = Word2Vec(sent2, vector_size=300, min_count=5)
            mod3 = Word2Vec(sent3, vector_size=300, min_count=5)

            # summarize the loaded model 
            # print(mod1, mod2, mod3)

            # summarize vocab
            # words = list(model.wv.index_to_key)
            # print('prostitute' in words, 'fetus' in words, 'abortion' in words)
            # print(words)

            # access vector for one word
            # print(model.wv['abortion'])

            # save model 
            # model.save('model.bin')
            try:
                a = (mod1.wv['mother'] + mod2.wv['mother'] + mod3.wv['mother']) / 3
                b = (mod1.wv['woman'] + mod2.wv['woman'] + mod3.wv['woman']) / 3
                c = (mod1.wv['father'] + mod2.wv['father'] + mod3.wv['father']) / 3
                d = (mod1.wv['man'] + mod2.wv['man'] + mod3.wv['man']) / 3
                # e = (mod1.wv['rape'] + mod2.wv['rape'] + mod3.wv['rape']) / 3
                # f = (mod1.wv['immigrant'] + mod2.wv['immigrant'] + mod3.wv['immigrant']) / 3
                # g = (mod1.wv['drink'] + mod2.wv['drink'] + mod3.wv['drink']) / 3
                # h = (mod1.wv['alcohol'] + mod2.wv['alcohol'] + mod3.wv['alcohol']) / 3
                # j = (mod1.wv['slave'] + mod2.wv['slave'] + mod3.wv['slave']) / 3
                # k = (mod1.wv['terrorist'] + mod2.wv['terrorist'] + mod3.wv['terrorist']) / 3
                # l = (mod1.wv['underage'] + mod2.wv['underage'] + mod3.wv['underage']) / 3
                # m = (mod1.wv['promiscuity'] + mod2.wv['promiscuity'] + mod3.wv['promiscuity']) / 3

                cos_simb = dot(a, b)/(norm(a)*norm(b))
                cos_simc = dot(d, c)/(norm(d)*norm(c))
                # cos_simd = dot(a, d)/(norm(a)*norm(d))
                # cos_sime = dot(a, e)/(norm(a)*norm(e))
                # cos_simf = dot(a, f)/(norm(a)*norm(f))
                # cos_simg = dot(a, g)/(norm(a)*norm(g))
                # cos_simh = dot(a, h)/(norm(a)*norm(h))
                # cos_simj = dot(a, j)/(norm(a)*norm(j))
                # cos_simk = dot(a, k)/(norm(a)*norm(k))
                # cos_siml = dot(a, l)/(norm(a)*norm(l))
                # cos_simm = dot(a, m)/(norm(a)*norm(m))


                print(cos_simb)
                print(cos_simc)
                print('======')
                # print(cos_simd)
                # print('rape,', cos_sime)
                # print('immigrant', cos_simf)
                # print('drink', cos_simg)
                # print('alcohol', cos_simh)
                # print('slave', cos_simj)
                # print('terrorist', cos_simk)
                # print('underage', cos_siml)
                # print('promiscuity', cos_simm)
            except Exception as  e: 
                print(e)
            sent1, sent2, sent3=[], [],[]
        
# load model 
    # model = Word2Vec.load('model2015.bin')
    # print(model)

#     # ------visualize word embedding

#     # fit a 2d PCA model to the vectors
#     X = model.wv[model.wv.index_to_key]
#     pca = PCA(n_components=2)
#     result = pca.fit_transform(X)

#     # create a scatter plot of the projection
#     words = list(model.wv.index_to_key)

#     # stop_words = set(stopwords.words('english'))
#     i_s = []
#     for i, word in enumerate(words):
#         if word.lower() in bank: 
#             i_s.append(i)
#             pyplot.scatter(result[i,0], result[i,1])
#             pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))

# # texts = [pyplot.text(result[i,0], result[i,0], words[i], ha='center', va='center') for i in i_s]
# # adjust_text(texts)
# pyplot.show()

