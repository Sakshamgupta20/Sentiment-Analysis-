# coding: utf-8

# In[1]:


import urllib.request
from urllib.parse import urlparse
import bs4
import queue
import math

import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import string

nltk.download('stopwords')
nltk.download('punkt')

print("Please enter the URL: ")
weblink = input()


in_url=input("How many tokens you want to search: ")
i=1
url_tokens=[]
while i<=int(in_url):
    y=input("Enter {} token: ".format(i))
    url_tokens.append(y)
    i=i+1
    
    
vis=open('visited.txt','w')
invert=open('inverted.txt','w')
invert_count=open('inverted_count.txt','w')
idf=open('idf.txt','w')

parsed_uri = urlparse(weblink)
global baseurl
baseurl ='{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
url_on=baseurl
nonvisited=queue.Queue()
visited=[]
needcmp=[]
wordDict = {}
wordCount = {}

wrongurl="bad request"
def find_soup(url):
    try:
        sauce=urllib.request.urlopen(url)
        soup=bs4.BeautifulSoup(sauce,'lxml')
        #visited.append(url)
        print(url + "   GOOD REQUEST")
        return(soup)
    except:
        print(url + "   BAD REQUEST")
        return(wrongurl)

def find_urls(soup):
    needcmp1=[]
    try:
        if soup != wrongurl:
            for link in soup.findAll('a'):
                url=str(link.get('href'))
                if url.startswith('http'):
                        needcmp1.append(url)
                elif url.startswith('/'):
                        url = baseurl + url
                        needcmp1.append(url)
            return needcmp1
        else:
            return(wrongurl)
        
    except:
        print("Error in Getting Links")
        
def compare():
    count=0
    try:
        if needcmp != wrongurl:
            for cmpurl in needcmp:
                if cmpurl not in visited and cmpurl not in nonvisited.queue:
                    nonvisited.put(cmpurl)
                else:
                    count=count+1
            visited.append(url_on)
            vis.write(url_on)
            vis.write("\n")
            print("Compare Successful")
    except:
        print("Compare Error")
        
def tokens(soup):
    try:
        if soup !=wrongurl:
            words_filtered = ""
            word_dict={}
            for paragraph in soup.findAll('p'):
                stop_words=set(stopwords.words('english')) | set(string.punctuation)
                text=paragraph.text
                text=text.lower()
                text_tokens = word_tokenize(text)
                for w in text_tokens:
                    if w not in stop_words:
                        words_filtered=words_filtered + " " + w
            word_dict[url_on]=words_filtered
            return(word_dict)
        else:
            return(wrongurl)
    except:
        print("Tokenization Failed")
        
def InvertedIndex(inputDict):
    if(inputDict != wrongurl):
        for wordKey, wordText in inputDict.items():
            for word in wordText.lower().split():
                wordCount[word] = wordCount.get(word,0)+1
                if wordDict.get(word,False):
                    if wordKey not in wordDict[word]:
                        wordDict[word].append(wordKey)
                else:
                    wordDict[word] = [wordKey]
        #print(wordDict)
        #print(wordCount)
    else:
        print("ERROR")
    
nonvisited.put(url_on)
#print(wordDict)
#print(wordCount)

i=len(visited)
while i<5:
    url_on=nonvisited.get()
    soup=find_soup(url_on)
    token_dict=tokens(soup)
    if token_dict != wrongurl:
        for key,va in token_dict.items():
            if any(word in va for word in url_tokens):
                needcmp=find_urls(soup)
                compare()
                print("Token Found")
                InvertedIndex(token_dict)
            else:
                print("Token Not Found In this url")
    print("VISITED  " +str(len(visited)))
    print("NON VISITED  " + str(nonvisited.qsize()))
    i = len(visited)
    
    
    

for key,va in wordDict.items():
    st=""
    for vi in va:
        st=st+str(vi)+","
    key=key.encode("utf-8")
    fin=str(key) + " => " + st  
    invert.write(fin)
    invert.write("\n")
    
for key,va in wordCount.items():
    key=key.encode("utf-8")
    fin=str(key) + " => " + str(va)
    invert_count.write(fin)
    invert_count.write("\n")
    
for key,va in wordDict.items():
    ids=len(va)/len(visited)
    value=math.log2(1/ids)
    key=key.encode("utf-8")
    idf.write(str(key) + " => " + str(value))
    idf.write("\n")
    
vis.close()
invert.close()
invert_count.close()
idf.close()

    




        
        

