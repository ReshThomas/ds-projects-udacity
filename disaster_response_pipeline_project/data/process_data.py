#!/usr/bin/python
# -*- coding: utf-8 -*-
# import libraries

import sys
import pandas as pd
import sqlite3
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """

    Loads messages,categories data sets and merge them to create dataframe

    """

    # load messages dataset

    messages = pd.read_csv(messages_filepath, dtype=str)

    # load categories dataset

    categories = pd.read_csv(categories_filepath, dtype=str, sep=',')

    # merge datasets

    df = pd.concat([messages, categories], axis=1, join='inner')
    return df




def clean_data(df):

    """

    Splits categories column into separate columns with 0/1,re-name colums and remove duplicate to create final data frame

    """    



    # Split the values in the categories column on the ; character so that each value becomes a separate column

    categories = pd.Series(df['categories']).str.split(pat=';', expand=True)



    # rename the columns of `categories`

    row = categories.iloc[0]

    category_colnames = row.apply(lambda r: r[:-2]).tolist()
    # Rename the columns of `categories`
    categories.columns = category_colnames
    categories['related'] = categories['related'].replace('related-2', 'related-1')



    # Iterate through the category columns in df to keep only the last character of each string (the 1 or 0)

    for column in categories:

      # set each value to be the last character of the string

      categories[column] = pd.Series(categories[column], dtype='object').str[-1]

      

      # convert column from string to numeric

      categories[column] = categories[column].astype(int)



    # drop the original categories column from `df`

    df.drop('categories', axis=1)
    #concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1, join='inner')

    # remove duplicates

    df=df.drop_duplicates(['message'], keep='last')
    



    return df


def save_data(df, database_filename):
    """
           Save the clean dataset into an sqlite database    
    """

    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('disasterresponse', engine, index=False)


def main():
    if len(sys.argv) == 4:

        (messages_filepath, categories_filepath, database_filepath) = \
            sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'

              .format(messages_filepath, categories_filepath))

        df = load_data(messages_filepath, categories_filepath)

        print ('Cleaning data...')
        df = clean_data(df)

        print ('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print ('Cleaned data saved to database!')
    else:

       print('Please provide the filepaths of the messages and categories '\

              'datasets as the first and second argument respectively, as '\

              'well as the filepath of the database to save the cleaned data '\

              'to as the third argument. \n\nExample: python process_data.py '\

              'disaster_messages.csv disaster_categories.csv '\

              'DisasterResponse.db')



if __name__ == '__main__':
    main()

