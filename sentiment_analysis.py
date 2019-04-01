
# coding: utf-8

# In[ ]:


from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import string
import matplotlib.pyplot as plt 
#nltk.download('punkt')
#nltk.download('stopwords')
stop_words=set(stopwords.words('english')) | set(string.punctuation)

reviews=open('reviews.txt','r',encoding='utf-8')
review_list=[]
positive_review=[]
negative_review=[]
neutral_review=[]

def get_sentiment(review): 
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'
        
for text in reviews:
    text=text.lower()
    text = text.replace(".", " ")
    text= ''.join([i if ord(i) < 128 else ' ' for i in text])
    words_filtered = ""
    text_tokens = TextBlob(text)
    text_tokens=text_tokens.words
    for w in text_tokens:
        if w not in stop_words:
            words_filtered=words_filtered + " " + w
    review_list.append(words_filtered)

for i in review_list:
    if get_sentiment(i)=="positive":
        positive_review.append(i)
    elif get_sentiment(i)=="neutral":
        neutral_review.append(i)
    else:
        negative_review.append(i)
positive=("Positive review percentage: {} %".format(100*len(positive_review)/len(review_list)))
negative=("Negative review percentage: {} %".format(100*len(negative_review)/len(review_list)))
neutral=("Neutral review percentage: {} %".format(100*len(neutral_review)/len(review_list)))

labels = ['Positive', 'Negative', 'Neutral']
sizes=[len(positive_review),len(negative_review),len(neutral_review)]
colors = ['green', 'red', 'yellow']
explode = (0.05, 0, 0)

plt.pie(sizes,explode=explode, labels=labels, colors=colors, startangle=90, autopct='%.1f%%')
plt.show()

