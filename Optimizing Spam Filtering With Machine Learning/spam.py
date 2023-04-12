# -*- coding: utf-8 -*-
"""all millistone.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DWoG4hRZwkm6YpYuBSSxF2LcEwWRZa6L
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split 
import nltk 
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer

df = pd.read_csv("/content/spam.csv",encoding="latin")
df.head()

df.info()

df.isna().sum()

df.rename({"v1":"label","v2":"text"},inplace=True,axis=1)

df.tail()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])

nltk.download("stopwords")

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import re
corpus = []
length = len(df)

for i in range(0,length):
  text = re.sub("^a-Za-Z0-9]"," " ,df["text"][i])
  text = text.lower()
  text = text.split()
  pe = PorterStemmer()
  stopword = stopwords.words("english")
  text = [pe.stem(word) for word in text if not word in set(stopword)]
  text = " ".join(text)
  corpus.append(text)

corpus

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=35000)
x =cv.fit_transform(corpus).toarray()

y = pd.get_dummies(df['label'])
y = y.iloc[:, 1].values

import pickle
pickle.dump(cv, open('cv1.pkl','wb'))

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0)

print("Before OverSampling, counts of label '1': {}".format(sum(y_train == 1)))
print("Before OverSampling, counts of label '0': {}  \n".format(sum(y_train == 0)))

from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state = 2)
x_train_res, y_train_res = sm.fit_resample(x_train, y_train.ravel())

print('After OverSampling, the shape of train_x: {}'.format(x_train_res.shape))
print('After OverSampling, the shape of train_y: {} \n'.format(y_train_res.shape))

print("After OverSampling, counts of label '1': {}".format(sum(y_train == 1)))
print("After OverSampling, counts of label '0': {}".format(sum(y_train == 0)))

df.describe()

df.shape

df["label"].value_counts().plot(kind="bar",figsize=(12,6))
 plt.xticks(np.arange(2),  ('Non spam', 'spam'),rotation=0);

from sklearn.model_selection import train_test_split
 x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=0)

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
 model.fit(x_train_res, y_train_res)

from sklearn.ensemble import  RandomForestClassifier

model = RandomForestClassifier()
 model.fit(x_train_res, y_train_res)

from sklearn.naive_bayes import MultinomialNB
 model = MultinomialNB()

model.fit(x_train_res, y_train_res)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model =  Sequential()

x_train.shape

model.add(Dense(units = x_train_res.shape[1],activation="relu",kernel_initializer="random_uniform"))

model.add(Dense(units =100,activation="relu",kernel_initializer="random_uniform"))

model.add(Dense(units=1,activation="sigmoid"))

model.compile(optimizer="adam",loss="binary_crossentropy",metrics=['accuracy'])

generator = model.fit(x_train_res,y_train_res,epochs=10,steps_per_epoch=len(x_train_res)//64)

y_pred=model.predict(x_test)
 y_pred

y_pr = np.where(y_pred>0.5,1,0)

y_test

from sklearn.metrics import confusion_matrix,accuracy_score
 cm = confusion_matrix(y_test, y_pr)
 score = accuracy_score(y_test,y_pr)
 print(cm)
 print('Accuracy Score Is:- ' ,score*100)

def new_review(new_review):
    new_review = new_review
    new_review = re.sub('[^a-zA-Z]', ' ', new_review)
    new_review = new_review.lower()
    new_review = new_review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    new_review = [ps.stem(word) for word in new_review if not word in   set(all_stopwords)]
    new_review = ' '.join(new_review)
    new_corpus = [new_review]
    new_X_test = cv.transform(new_corpus).toarray()
    new_y_pred = model.predict(new_X_test)
    print(new_y_pred)
    new_X_pred = np.where(new_y_pred>0.5,1,0)
    return new_review
 new_review = new_review(str(input("Enter new review...")))

from sklearn.metrics import confusion_matrix,accuracy_score
 cm=confusion_matrix(y_test,y_pr)
 score = accuracy_score(y_test,y_pr)
 print(cm)
 print('Accuracy Score Is Naive Bayes:- ' ,score*100)

model.save('spam.h5')

!pip install nbconvert

!jupyter nbconvert --to html spam.ipynb

!pip install flask-ngrok

from flask import Flask, render_template, request
import pickle
import numpy as np 
import re
import nltk 
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from tensorflow.keras.models import load_model

loaded_model = load_model('spam.h5')
cv = pickle.load(open('cv1.pkl','rb'))
app = Flask(__name__)

@app.route('/Spam',methods=['POST','GET'])
def prediction():
    return render_template('spam.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
       message = request.form['message']
       data = message 

    new_review = str(data)
    print(new_review)
    new_review = re.sub('[^a-zA-Z]', ' ',new_review)
    new_review = new_review.lower()
    new_review = new_review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    new_review = [ps.stem(word) for word in new_review if not word in   set(all_stopwords)]
    new_review = ' '.join(new_review)
    new_corpus = [new_review]
    new_X_test = cv.transform(new_corpus).toarray()
    new_y_pred = model.predict(new_X_test)
    print(new_y_pred)
    new_X_pred = np.where(new_y_pred>0.5,1,0)
    print(new_X_pred)
    if new_review[0][0]==1:
       return render_template('result.html', prediction="Spam")
    else :
       return render_template('result.html', prediction="Not a Spam")

import os

if __name__=="__main__":
  
    port=int(os.environ.get('PORT',5000))
    app.run(debug=False)