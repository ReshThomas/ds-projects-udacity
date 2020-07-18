import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import pickle

def load_data(database_filepath):
    '''
    INPUT 
        database_filepath - Filepath used for importing the database     
    OUTPUT
        Returns the following variables:
        X - Input features- messages 
        y - Output variable -categories 
        category_names - Labels for classification - Category columns
    '''
    engine = create_engine('sqlite:///data/DisasterResponse.db')
    df =  pd.read_sql_table('disasterresponse', engine)
    cols=['id','message','original', 'genre','categories']
    X = df['message']
    y = df.drop(cols, axis=1)
    #print(y)
    y=y.astype(int)
    category_names=y.columns
    print category_names
    return X,y,category_names


def tokenize(text):
    '''
     Tokenize and lemmatize each word in a given text
    '''

    #Tokenize the string text and initiate the lemmatizer
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    # Lemmatize each word in tokens
    clean_tokens = []
    for tok in tokens:
      clean_tok = lemmatizer.lemmatize(tok).lower().strip()
      clean_tokens.append(clean_tok)
    return clean_tokens



def build_model():
    '''
     Define pipeline with transformations and parameters to build model.
    '''

    pipeline = Pipeline([
   

        ('text_pipeline', Pipeline([

            ('vect', CountVectorizer(tokenizer=tokenize)),

            ('tfidf', TfidfTransformer())

        ])),

        ('clf',  MultiOutputClassifier(RandomForestClassifier()))
    ])

    parameters = {'clf__estimator__n_estimators': [20],
                  'clf__estimator__min_samples_split': [2, 5]
                 }
   
    cv = GridSearchCV(pipeline, param_grid=parameters, n_jobs=-1, verbose=10)
    
    return cv


def evaluate_model(model, X_test, y_test, category_names):
    '''
     evaluate model with test data
    '''
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=category_names))
    


def save_model(model, model_filepath):
    '''
     export model as a pickle file
    '''
     pickle.dump(model, open(model_filepath, 'wb'))
     


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()