
# coding: utf-8

# In[3]:


import urllib.request
from urllib.parse import urlparse
import bs4

count=0
wrongurl="wrong"
titles=[]
urls=[]
products_dict={}
user_choice=input("Enter Your Choice: ")
user_search=input("Enter Your Topic: ")
if user_choice=="flipkart":
    if user_search!="":
        user_search=urllib.parse.quote(user_search)
    user_search="https://www.flipkart.com/search?q="+user_search
else:
    user_search=urllib.parse.quote(user_search)
    user_search="https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+user_search+"&ie=UTF8&qid=1541145831&lo=none"
review_urls=set()
review_url=""
reviews=open("reviews.txt","w",encoding="utf-8")

def find_soup(url):
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(url)
        soup=bs4.BeautifulSoup(response,'lxml')
        #visited.append(url)
        print(url + "   GOOD REQUEST")
        return(soup)
    except:
        print(url + "   BAD REQUEST")
        return(wrongurl)    
def find_vertical_title(soup):                             #Getting vertical title
    if soup!=wrongurl:
        data= soup.findAll('div',{"class":"_3wU53n"})
        for i in data:
            titles.append(i.text)
    else:
        return(wrongurl)
        
def find_vertical_urls(soup):                               #Getting vertical urls
    if soup!=wrongurl:
        data= soup.findAll('a',{"class":"_31qSD5"})
        for i in data:
            url="https://www.flipkart.com"+i.get('href')
            urls.append(url)
    else:
        return(wrongurl)
    
def Making_Dictonary(titles,urls): 
    for i in range(len(titles)):                                
        products_dict[titles[i]]=urls[i]
        
def find_horizontal_dictonary(soup):                    #Getting horizontal title,url and making dictonary
    if soup!=wrongurl:
        data= soup.findAll('a',{"class":"_2cLu-l"})
        for i in data:
            products_dict[i.get('title')]="https://www.flipkart.com"+i.get('href')
    else: 
        return(wrongurl)
    
def find_horizontal_dictonary_amazon(soup):              #Getting horizontal title,url and making dictonary
    if soup!=wrongurl:
        data= soup.findAll('a',{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
        for i in data:
            products_dict[i.get('title')]=i.get('href')
    else: 
        return(wrongurl)
    
def find_urls_flipkart(soup):                                    #Finding Links of Review Urls
    if soup!=wrongurl:
        data= soup.findAll('a',{"class":"_33m_Yg"})
        for link in data:
            review_urls.add(link.get('href'))
    else:
        return(wrongurl)
def find_reviews_flipkart(soup):                                 #Finding Reviews
    global count
    if soup!=wrongurl:
        content = soup.findAll("div", class_="qwjRop")
        for j in content:
            for i in j.find('span'):
                i.replace_with('')
            print(j.text)
            count=count+1
            reviews.write(j.text)
            reviews.write("\n")
    else:
        return(wrongurl)
    
def find_urls_amazon(soup):                                    #Finding Links of Review Urls
    if soup!=wrongurl:
        data= soup.findAll('li',{"class":"page-button"})
        for link in data:
            ii=link.findAll('a')
            for  i in ii:
                review_urls.add(i.get('href'))
    else:
        return(wrongurl)
def find_reviews_amazon(soup):                                 #Finding Reviews
    global count
    if soup!=wrongurl:
        content = soup.findAll("span", class_="a-size-base review-text")
        for i in content:
            count=count+1
            print(i.text)
            re=str(i.text)
            reviews.write(re)
            reviews.write("\n")
    else:
        return(wrongurl)
    
if user_choice== "flipkart":
    
    x=find_soup(user_search)

    find_vertical_title(x)
    if titles:
        find_vertical_urls(x)
        Making_Dictonary(titles,urls)
    else:
        find_horizontal_dictonary(x)

    for key,val in products_dict.items():
        print(key)

    if bool(products_dict):

        Product_url=input("Enter Your Search: ")

        Product_url=products_dict[Product_url]

        x=find_soup(Product_url)                        #finding read more url
        for i in x.findAll('div',{"class":"col _39LH-M"}):
            y=i.findAll('a')
            for ii in y:
                review_url=ii.get('href')
                
        if "/product-reviews/" in review_url:           #Finding Links of Review Urls
            review_url="https://www.flipkart.com"+review_url
            find_urls_flipkart(find_soup(review_url))
            if review_urls:
                for url in review_urls:                           #finding reviews through review urls
                    url="https://www.flipkart.com"+url
                    find_reviews_flipkart(find_soup(url))
            else:
                find_reviews_flipkart(find_soup(review_url))
        else:
            find_reviews_flipkart(find_soup(Product_url))

    else:
        print("No Results Found")

else:
    x=find_soup(user_search)
    find_horizontal_dictonary_amazon(x)
    for key,val in products_dict.items():
        print(key)
    
    if bool(products_dict):

        Product_url=input("Enter Your Search: ")

        Product_url=products_dict[Product_url]

        x=find_soup(Product_url)                        #finding read more url
        for i in x.findAll('a',{"class":"a-link-emphasis a-text-bold"}):
            review_url=i.get('href')
        if "=all_reviews" in review_url:
            review_url="https://www.amazon.in"+review_url    
            find_urls_amazon(find_soup(review_url))
        
            if review_urls:
                for url in review_urls:                           #finding reviews through review urls
                    url="https://www.amazon.in"+url
                    find_reviews_amazon(find_soup(url))
        else:
            print("No Reviews Yet")
    else:
        print("No Results Found")

print(count)
if count >0:
    print("Done")
else:
    print("No Reviews found")
reviews.close()

