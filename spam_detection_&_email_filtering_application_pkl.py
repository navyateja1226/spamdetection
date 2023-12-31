# -*- coding: utf-8 -*-
"""Spam detection & email filtering application.pkl

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zwYMvHQUVxM2_QtvOXd4hlkAZYMmGrzU

Importing Libraries
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

"""Loading Dataset"""

data = pd.read_csv('/content/spam.csv',encoding='ISO-8859-1')

data.sample(10)

"""**Data Cleaning**"""

# Size of the dataset
data.size

# Shape of the dataset
data.shape

# Columns in the dataset
data.columns

# Information about the dataset
data.info()

# Describes aboit the dataset
data.describe()

# Checking the null values in the dataset
data.isnull().sum()

# Renaming the Columns

data.rename({'v1':'Type','v2':'Email'},axis=1,inplace=True)
data

# Removing the Irrelavent Data or Columns from the dataset

df = data.drop(['Unnamed: 2','Unnamed: 3',	'Unnamed: 4'],axis=1)
df.sample(10)

# LabelEncoding For the column name Type for easy calculations
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

df['Type'] = le.fit_transform(df['Type'])
df.sample(10)

# Checking Unique Values in the column of Type
df['Type'].unique()

# Checking null values after removing the columns form the dataset
df.isnull().sum()

# Checking for duplicated columns in the dataset
df.duplicated().sum()

# Removing Duplicates from the dataset

df = df.drop_duplicates(keep='first')
df.tail()

# Shape of the dataset after removing the unused columns from the dataset
df.shape

# Checking the size of the dataset after removing the unused columns fron the dataset
df.size

# Checking the duplicateed rows in the dataset
df.duplicated().sum()

"""**Exploratory Data Analysis**"""

# importing the matplotlib for visualizing part
import matplotlib.pyplot as plt

# Plot a pie chart
plt.pie(df['Type'].value_counts(),labels=['ham','spam'],autopct='%0.2f%%',explode=[0.1,0])
plt.show()

"""From the above pie chart we can observe that the data is imbalanced. So, now we are going to do Analysis on Number of Characters, Words, and Sentences Used in every Message"""

# importing the nltk and downlading all methods to perform on sentencs and characters, and words
import nltk
nltk.download('all')

# Finding out Number of characters in each Message

df['num_of_characters'] = df['Email'].apply(len)
df.sample(10)

# Now Number of Words

df['num_words'] = df['Email'].apply(lambda x : len(nltk.word_tokenize(x)))
df.sample(10)

# Number of Sentences

df['num_sentence'] = df['Email'].apply(lambda x : len(nltk.sent_tokenize(x)))
df.sample(10)

##ham

df[df['Type'] == 0][['num_of_characters','num_words','num_sentence']].describe()

##Spam

df[df['Type'] == 1][['num_of_characters','num_words','num_sentence']].describe()

# importing the seaborn for visualizing part
import seaborn as sns

# Plot a histogram to show the distributiions of dataset
plt.figure(figsize=(10,10))
sns.histplot(df[df['Type'] == 0]['num_of_characters'],color='orange')
sns.histplot(df[df['Type'] == 1]['num_of_characters'],color='green')
plt.show()

plt.figure(figsize=(10,10))
# Plot a histogram to show the distributiions of dataset
sns.histplot(df[df['Type'] == 0]['num_words'],color = 'orange')
sns.histplot(df[df['Type'] == 1]['num_words'],color='green')
plt.show()

plt.figure(figsize=(10,10))
# Plot a histogram to show the distributiions of dataset
sns.histplot(df[df['Type'] == 0]['num_sentence'],color='orange')
sns.histplot(df[df['Type'] == 1]['num_sentence'],color='green')
plt.show()

# Pairwise relation in dataset
sns.pairplot(df,hue='Type')
plt.show()

# Coorelation in dataset
sns.heatmap(df.corr(),annot=True)
plt.show()

'''The box shows the quartiles of the dataset while the whiskers extend to show the rest of the distribution,
except for points that are determined to be "outliers" using a methodthat is a function of the inter-quartile range.'''
plt.figure(figsize=(10,8))
sns.boxplot(x='Type',y='num_of_characters',data=df)

# Python program to generate WordCloud

# importing all necessary modules
from wordcloud import WordCloud, STOPWORDS




comment_words = ''
stopwords = set(STOPWORDS)

# iterate through the csv file
for val in df.Email:

    # typecaste each val to string
    val = str(val)

    # split the value
    Type = val.split()

    # Converts each token into lowercase
    for i in range(len(Type)):
        Type[i] = Type[i].lower()

    comment_words += " ".join(Type)+" "

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)

# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()

"""Train Test Split Dataset

CountVectorizer to convert the text into matrices
"""

from sklearn.feature_extraction.text import CountVectorizer
x = df.Email
cv = CountVectorizer()
x = cv.fit_transform(x)

x.toarray()

x.reshape(-1,1)

"""Naive Bayes have threee Classifier ( Bernouli, Multinominal, Gaussian). Here, I use Multinominal Bayes beacuse here data in a discrete form discrete data"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,df.Type,test_size=0.10,random_state=104)

from sklearn.naive_bayes import MultinomialNB

"""Training The Model"""

from sklearn.pipeline import Pipeline

mut = MultinomialNB()

mut.fit(x_train,y_train)

mut.score(x_test,y_test)

from sklearn.naive_bayes import BernoulliNB
bnb = BernoulliNB()

bnb.fit(x_train,y_train)

bnb.score(x_test,y_test)

"""Perfomrnace Metrics"""

# history = mut.fit(x_train, y_train,validation_data=(x_test, y_test))
y_predict = [1 if o>0.5 else 0 for o in mut.predict(x_test)]

from sklearn.metrics import confusion_matrix,f1_score, precision_score,recall_score
cf_matrix =confusion_matrix(y_test,y_predict)
tn, fp, fn, tp = confusion_matrix(y_test,y_predict).ravel()
print("Precision: {:.2f}%".format(100 * precision_score(y_test, y_predict)))
print("Recall: {:.2f}%".format(100 * recall_score(y_test, y_predict)))
print("F1 Score: {:.2f}%".format(100 * f1_score(y_test,y_predict)))

"""Confusion Matrix"""

import seaborn as sns
import matplotlib.pyplot as plt
ax= plt.subplot()
#annot=True to annotate cells
sns.heatmap(cf_matrix, annot=True, ax = ax,cmap='Blues',fmt='');
# labels, title and ticks
ax.set_xlabel('Predicted labels');
ax.set_ylabel('True labels');
ax.set_title('Confusion Matrix');
ax.xaxis.set_ticklabels(['Not Spam', 'Spam']); ax.yaxis.set_ticklabels(['Not Spam', 'Spam']);

vectorizer = CountVectorizer()
features = vectorizer.fit_transform(df['Email'])

# Train the Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(features, df['Type'])

def predict_spam(email_text):
    email_features = vectorizer.transform([email_text])
    prediction = classifier.predict(email_features)
    if prediction[0] == 1:
        return "Spam"
    else:
        return "Not Spam"

# Example usage
email_text = "Get rich quick!"
prediction = predict_spam(email_text)
print("Prediction:", prediction)

import pickle











