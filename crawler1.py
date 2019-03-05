
# coding: utf-8

# In[ ]:


import urllib.request
import bs4
import queue

nonvisited=queue.Queue()
visited=[]
needcmp=[]
wrongurl="bad request"
def find_soup(url):
    try:
        sauce=urllib.request.urlopen(url)
        soup=bs4.BeautifulSoup(sauce,'lxml')
        visited.append(url)
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
                if cmpurl not in visited:
                    nonvisited.put(cmpurl)
                else:
                    count=count+1
            print("Compare Successful")
    except:
        print("Compare Error")
    
soup=find_soup('http://www.wizardguy.in/')
needcmp=find_urls(soup)
compare()

while not nonvisited.empty():
    soup=find_soup(nonvisited.get())
    needcmp=find_urls(soup)
    compare()
    print("VISITED  " +str(len(visited)))
    print("NON VISITED  " + str(nonvisited.qsize()))





        
        

