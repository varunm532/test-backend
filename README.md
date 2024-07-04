# README for Data Structures and Final Project

## Background

- This project consists of several integrated team features into one, unanimous project.
  - This is the backend for the project. The frontend README contains information regarding crediting and additional context.
- Template for the project was a teacher-provided flask porfolio containing many starter files to aid in building the base system(s) of backend functionality (ex: main.py).

## Stock Project:
---
- Created by Varun Manoj Pillai ( varunm532 )
- Files used in this project: api/stock.py, api/stocksort.py, model/users.py, model/stockfilter.py
  - api/stock.py:
      - contain api endpoint code to:
          - diplay stocks data stored in SQLite3 db and update price through 3rd party api
          - code to handle buying and selling actions
          - code to sent data to frontend to create interactive graph through AnyChart
          - code to display all transactions of user (data from db)
          - code to update single stock
          - code to display sorted stocks based on sector
  - model/users.py:
      - Contains all code to initilize db tables
      - contains all db changes which are utilized in api/stock.py
  - api/stocksort.py:
      - Code to recieve input from user about sectore selection
      - calls sorting program in model/stockfilter.py
      - returns truplet of sorted stocks
  - model/stockfileter.py:
      - code to clean CSV file containing all stocks from S&P 500
      - code to clean json responce to match clean csv data
      - code to bucket sort and code to sort stocks alphebetically
    
