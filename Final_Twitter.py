#these are the libraries used for these sns.twitter scrape methods using a customizes streamlit website
import streamlit as st
import base64
from PIL import Image
import snscrape.modules.twitter as sntwitter
import numpy as np
import datetime
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import pandas as pd
from pymongo import MongoClient



#connecting MongoDB-Database and creating a collection
conn = MongoClient("mongodb://Guvi:guvi123@ac-oayeiwq-shard-00-00.mx1b0j2.mongodb.net:27017,ac-oayeiwq-shard-00-01.mx1b0j2.mongodb.net:27017,ac-oayeiwq-shard-00-02.mx1b0j2.mongodb.net:27017/?ssl=true&replicaSet=atlas-9f37hz-shard-0&authSource=admin&retryWrites=true&w=majority")
db = conn["snscrape"]
coll = db["twitter-data"]


#This is used to make the streamlit web-page customized
img = Image.open("Twitter_Logo.jpeg")
st.set_page_config(page_title="Twitter scraping",page_icon = img,layout = "wide")
def get_img_as_base64(file):
    with open(file,"rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img_1 = get_img_as_base64("wp12022834.jpg")

hide_st_style = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;} 
header {visibility:hidden;} 
</style> 
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image :url("data:image/png;base64,{img_1}");
background-size : cover;
}}
[data-testid="stHeader"]{{
background:rgba(0,0,0,0);
}}
</style>

"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.header("TWITTER SCRAPING")

#It enables user to scrape the data from twitter using "snscrape"
def ScrapingTheTweets(word,From,To,maxTweets):
  tweets_list = []
  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{From} until:{To}').get_items()):
      if i>(maxTweets-1):
          break
      tweets_list.append([tweet.date,tweet.id,tweet.user.username,tweet.url,tweet.rawContent,tweet.replyCount,tweet.likeCount,tweet.retweetCount,tweet.lang,tweet.source ])
  tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id','User Name','URL','Content','ReplyCount','LikeCount','Retweet-Count','Language','Source'])
  tweets_df.to_json("user-tweets.json")
  tweets_df.to_csv("user-tweets.csv")
  return tweets_df

#It is to visualize the most frequent word used by peoples along with the search word in wordcloud form
def word_cloud():
    stopwords = set(STOPWORDS)
    data = pd.read_csv("user-tweets.csv")
    mask = np.array(Image.open("tweetie.png"))
    text = " ".join(review for review in data.Content)
    wordcloud = WordCloud(background_color = "white",max_words=500,mask=mask).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    plt.savefig("word-cloud.png",format="png")
    return plt.show()

#It is to upload the search document in Mongodb database
def Tweets_In_Database(n_word):
    db = conn["snscrape"]
    coll = db[n_word]
    df = pd.read_csv("user-tweets.csv")
    df_dict = df.to_dict("records")
    coll.insert_many(df_dict)


col1,col2,col3 = st.columns(3)
col1.image(Image.open("pngwing.com.png"),width=350)
col2.image(Image.open("pngwing.com (1).png"),width=250)
col3.image(Image.open("pngwing.com (2).png"),width=350)

col1,col2,col3,col4,col5,col6,col7,col8= st.columns(8)
col1.image(Image.open("facebook.png"),width = 100)
col2.image(Image.open("whatsapp.png"),width = 75)
col3.image(Image.open("Linkedin.png"),width = 100)
col4.image(Image.open("instagram.png"),width = 100)
col5.image(Image.open("twitter.png"),width = 100)
col6.image(Image.open("youtube.png"),width=100)
col7.image(Image.open("telegram.png"),width = 100)
col8.image(Image.open("mail.png"),width = 100)

if st.button(" What is Twitter :bird: ?"):
    st.write('# Twitter :bird:')
    st.balloons()
    col1,col2 = st.columns(2)
    col2.image(Image.open("twitter12345.png"),width = 600)
    col1.write("### Twitter is a social media platform where users can post short messages called tweets of up to 280 characters. These tweets can contain text, images, videos, or links to other content.")   
    col1.write("### Users can follow other users to see their tweets in their feed, and they can also like or retweet tweets to share them with their followers. ")
    col1.write("### Twitter is known for its use of hashtags, which allow users to tag their tweets with specific keywords or phrases. This helps to organize tweets around common topics and makes it easier for users to find content related to their interests. ")  
    col1.write("### It has become a popular platform for news, entertainment, politics, and communication between individuals and organizations. ") 
    col1.write("### Twitter was founded in 2006 and has grown to become one of the most popular social media platforms in the world, with over 330 million active monthly users as of 2023")

if st.button("How to Scrape the twitter data ?"):
    st.write('# snsscrape :rocket:')
    col1,col2 = st.columns(2)
    col1.write("### Social networking site (SNS) scraping refers to the process of using automated tools or software to extract or collect data from social networking sites such as Facebook, Twitter, LinkedIn, Instagram, and others.")
    col1.write("### SNS scraping can involve collecting user profiles, posts, comments, likes, or any other publicly available data on the social networking site")
    col1.write("### SNS scraping can be used for various purposes, such as market research, sentiment analysis, competitor analysis, social media monitoring, or even for creating datasets for machine learning and data analysis")
    col1.write("### Using this we can also save the scraped data in various formats such as CSV, JSON etc")
    col2.image(Image.open("sns.png"),width = 600)
    st.success("OK..It's time to scrape some twitter data :bird: ")
    st.balloons()


col1,col2,col3 = st.columns(3)
col1.image(Image.open("searchman.png"),width = 250)
col2.image(Image.open("searchcom.png"),width = 250)
col3.image(Image.open("searchint.png"),width= 250)                     
word = st.text_input("Enter Word to Search")
if word:
    From = st.date_input("From Date")
    if From:
        To = st.date_input("To Date")
        if To:
            maxTweets = st.number_input("Number of Tweets",1,1000)
            if maxTweets:
                check = st.button("Scrap the tweets")
                if check:
                    st.dataframe(ScrapingTheTweets(word,From,To,maxTweets).iloc[0:10])
                    st.snow()



col1,col2,col3 = st.columns(3)
col1.image(Image.open("data-base.png"),width = 250)
col3.image(Image.open("Mongodb.png"))
col2.header("You can add your Previous Searched DATA into MongoDB database")

list = ['',"Store in data-base","View as data-frame"]
CHOICE = st.selectbox("SELECT",list)
if CHOICE=="Store in data-base":
    n_word = st.text_input("Enter the Key-word on which you want to store the data in Mongo DB database")
    upload = st.button("upload")
    if upload:
        Tweets_In_Database(n_word)
        st.success("Your DATA-BASE has been UPDATED SUCCESSFULLY :smiley:")
        st.balloons()
            
if CHOICE=="View as data-frame":
    if st.button("view :goggles:"):
        df = pd.read_csv("user-tweets.csv")
        st.dataframe(df)
        st.balloons()



col1,col2,= st.columns(2)
col1.image(Image.open("download.png"),width = 300)
col2.header("You can Download your searched data here")
choice1 = ["Select","Searched-data"]
menu=st.selectbox("SELECT", choice1)
if menu=="Searched-data":
    with open("user-tweets.csv") as CSV:
        if st.download_button("DOWNLOAD THE TWEETS IN --> .csv ",CSV,file_name="My-Tweets.csv"):
            st.success("My-TWEETS.csv..! has been downloaded")
    with open("user-tweets.json") as JSON:
        if st.download_button("DOWNLOAD THE TWEETS IN --> .json",JSON,file_name="My-Tweets.json"):
            st.success("My-TWEETS.json..! has been downloaded")


st.write("---")
st.title("About me")
name = "Vigneshwar Gekuru"
mail = (f'{"Mail Me At :"}  {"vigneshwargekuru@gmail.com"}')
description = "An aspiring DATA-SCIENTIST with brilliant ideas"

col1,col2,col3= st.columns(3)
col2.image(Image.open("my.png"),width = 240)
with col1:
    st.header(name)
    st.write(description)
    st.write(mail)
    st.image("mail.png",width = 50)
with col3:
  st.image("sucesshand.png",width=250)
  st.write("###### If you like my work kindly reach out to me by given links")
    

col1,col2,col3,col4,col5 = st.columns(5)

col1.write('[Twitter](https://twitter.com/G_Vigneshwar_01)')
col1.image(Image.open("twitter.png"),width = 200)
col2.write('[GIT-Hub](https://github.com/VigneshwarGekuru)')
col2.image(Image.open("Github.png"),width = 170)
col3.write('[linkedIN](https://www.linkedin.com/in/vigneshwar-gekuru-6834a5240/)')
col3.image(Image.open("Linkedin.png"),width = 200)
col4.write('[Facebook]()')
col4.image(Image.open("facebook.png"),width = 200)
col5.write('[Instagram]()')
col5.image(Image.open("instagram.png"),width = 200)