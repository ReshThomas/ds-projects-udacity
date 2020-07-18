# Disaster Response Pipeline Project
Project Submissions for Project2 - Disaster Response Pipeline Project
## Project 2:
Disaster Response Pipeline - ETL , ML Pipeline,Flask Web App
## Installation:
The code was run using Python3
## Project Motivation
This project contains 3 components. The end goal is to input a text message and be able to classify the message into 36 pre-defined categories.
The messages that have been provided are real texts that were sent during disaster events.
In this project I had to process the test messages (ETL) , create an ML pipeline which would classifies these messages and finally
it has a UI component which displays visuals used for exploratory analysis. The web app allows a user to enter new message and get classification results in several categories
## Requirements
The Code was run using Python 3
The following libraries have been used
numpy
sqlite3
sqlalchemy
plotly
pandas
matplotlib
nltk
pickle
seaborn
sklearn
json

## Files:
*ETL Pipeline*
- Code : data/process_data.py
Loads the messages and categories datasets
Merges the two datasets
Cleans the data
Stores it in a SQLite database
- Data Files
  - disaster_categories.csv
  - disaster_messages.csv
  
*ML Pipeline*  
- Code :model/train_classifier.py
Loads data from the SQLite database
Splits the dataset into training and test sets
Builds a text processing and machine learning pipeline
Trains and tunes a model using GridSearchCV
Outputs results on the test set
Exports the final model as a pickle file


*Flask WebPage*
- Code : app/run.py
Outputs data visualizations using Plotly in the web app. 
Provides an interface for a user to input a message and get the cassification

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

## Acknowledgement
The data for the project is povided by Figure 8 ,code templates provided by Udacity