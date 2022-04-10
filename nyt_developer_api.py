import json
import requests
import time
import csv
from bs4 import BeautifulSoup





def func():
    # link = 'https://www.nytimes.com/svc/add/v1/sitesearch.json?fq=(-type_of_material%3Aletter%20AND%20document_format%3Afast%20AND%20(asset_id%3A%2F%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%5B0-9%5D%2B%2F%20OR%20timesmachine_url%3A%5B*%20TO%20*%5D))%20OR%20(_exists_%3Atimesmachine_url)&begin_date='+startdate+'&end_date='+enddate+'&page='+str(i)+'&q='+query+'&sort=oldest'
    link = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=abortion&begin_date=18500101&end_date=18501231&sort=oldest&page=0&api-key=J8Xs1TzSY7SLGm2RCEgIJztrHYGya9w9"

    r = requests.get(link)
    data = json.loads(r.text)


    response = data['response']

    docs = response['docs']
    meta = response['meta']
    print(meta)
    for doc in docs: 
        print(doc['web_url'])
        print()


    # key- meta
    # val- {'hits': 52120, 'offset': 0, 'time': 61}





def see_guts(x): 
    r = requests.get(x)
    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.prettify())

    title = soup.find('h1', attrs = {'class':'entry-title'})
    print('title', title.text)

    table = soup.findAll('p', attrs={'class':'story-body-text'})      
    for row in table:
        print(row.text)


    


def get_yearly_counts(): 
    start = 1852
    end = 2022 + 1
    articles=[]

    for i in range(start, end):

        link = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=abortion&begin_date=" + str(i) + "0101&end_date=" + str(i) + "1231&sort=oldest&page=0&api-key=J8Xs1TzSY7SLGm2RCEgIJztrHYGya9w9"
        r = requests.get(link)
        data = json.loads(r.text)

        hits = data['response']['meta']['hits']
        print(i, '\t', hits)
        time.sleep(6)

        article={}
        article['year']=i
        article['count']=hits
        articles.append(article)

    fn = 'yearly_counts.csv'
    with open(fn, 'w', newline='') as f:
        w = csv.DictWriter(f,['year','count'])
        w.writeheader()
        for article in articles:
            w.writerow(article)





def get_all_links(links, year):

    link = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=abortion&begin_date=" + str(year) + "0101&end_date=" + str(year) + "1231&sort=oldest&page=0&api-key=J8Xs1TzSY7SLGm2RCEgIJztrHYGya9w9"
    r = requests.get(link)
    data = json.loads(r.text)

    hit_num = data['response']['docs']['meta']['hits']
    max_page = round(hit_num / 10) + 1     # buffer

    for i in range(0, max_page):
        link = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=abortion&begin_date=" + str(year) + "0101&end_date=" + str(year) + "1231&sort=oldest&page=" + str(i) + "&api-key=J8Xs1TzSY7SLGm2RCEgIJztrHYGya9w9"
        r = requests.get(link)
        data = json.loads(r.text)

        docs = data['response']['docs']

        for doc in docs: 
            links.append(doc)
            print(doc)





def bleh():

    with open('1977.csv') as csvfile: 
        reader = csv.reader(csvfile)

            
        for row in reader: 
                print(row)





def see_diff_hosts_links(year, hosts): 
    fn = 'links_only/' + str(year) + 'links_only' + '.csv'
    print('--------------')
    print(year, end='\t')
    art_count = 0

    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)

        for row in reader: 
        
            if row[0]=='link': continue

            if 'douthat.blogs.nytimes.com' in row[0]: 
                print(row[0])
                break

            hosts[(row[0].split('/'))[2]] = hosts.get((row[0].split('/'))[2], 0) + 1
            art_count += 1
        print(art_count)
    
    return art_count





def test_data_count(year): 
    fn = str(year) + '.csv'
    arts = 0
    data_links = []
    pastrow = None
    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0]=='title': continue # first row
            if 'https://' not in row[1]: continue # extra characters

            if row[2]=='NO TEXT FOUND': 
                print('no text found with link ', row[1])

            data_links.append(row[1])
            pastrow = row
            arts+=1
    print(arts)

    fn = 'links_only/' + str(year) + 'links_only'+ '.csv'
    link_links = []
    with open(fn) as csvfile: 
        reader = csv.reader(csvfile)
        for row in reader: 
            if row[0]=='link': continue # first row
            link_links.append(row[0])

    print('len data, len links', len(data_links), len(link_links))
    error=False
    for i in range(len(link_links)):
        if data_links[i] != link_links[i]: 
            error=True
            print('error with difference', data_links[i], link_links[i]) 
            break
    print('there are difference errors:', error)
        









if __name__ == "__main__":

    # for i in range(1970, 1980):
    #     try: 
    #         print(i,":", end='')
    #         test_data_count(i)
    #     except: 
    #         pass

    
    # bleh()

    # test_data_count(2000)
    see_guts('https://learning.blogs.nytimes.com/2000/01/24/iowas-primarys-colors/')

    # sorted_hosts = sorted(hosts.items(), key=lambda item: item[1], reverse=True)
    # i = 1
    # for k, v in sorted_hosts: 
    #     print(i, k, '---',  v)
    #     i+= 1
    # print('total articles', sum(hosts.values()))
    
    # print(count)
    
    
    