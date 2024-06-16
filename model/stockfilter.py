import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
# Import the required libraries for the TitanicModel class
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np


class Stocksort:
    _instance = None
    def __init__(self):
        self.data = pd.read_csv('S&P500.csv')
    #def _clean(self):
    #    ##self.data.drop(columns=['CIK','Date added','Headquarters Location'],inplace=True)
    #    #self.data['GICS Sector'] = self.data['GICS Sector'].astype(str).str.strip().str.lower()
    #   ## #print (self.data['GICS Sector'])
    #   ## self.data['GICS Sector'] = self.data['GICS Sector'].apply(
    #   ##     lambda x:(
    #   ##               1 if x == 'Communication Services' else
    #   ##               2 if x == 'consumer discretionary' else
    #   ##               3 if x == 'consumer staples' else
    #   ##               4 if x == 'energy' else 
    #   ##               5 if x == 'financials' else
    #   ##               6 if x == 'health care' else
    #   ##               7 if x == 'industrials' else
    #   ##               8 if x == 'information technology' else
    #   ##               9 if x == 'materials' else 
    #   ##               10 if x == 'real estate' else
   #    ##               0
    #   ##               #print("value of x:" + x)
    #   ##     )
    #  # # 
    #   ## )
       ## data = self.data['GICS Sector']
       ## #return data.tolist()
       # return data
    #def clean_sector(x):
    #    if x == "communication services":
    #        return 1
    #    elif x == 'consumer discretionary':
    #        return 2
    #    elif x == 'consumer staples':
    #        return 3
    #    elif x == 'energy':
    #        return 4
    #    elif x == 'financials':
    #        return 5
    #    elif x == 'health care':
    #        return 6
    #    elif x == 'industrials':
    #        return 7
    #    elif x == 'information technology':
    #        return 8
    #    elif x == 'materials':
    #        return 9
    #    elif x == 'real estate':
    #        return 10
    #    else:
    #        return 0
    #def _clean(self):
    #    self.data['GICS Sector'] = self.data['GICS Sector'].apply(clean_sector)
    #    return self.data
    
    # Load the CSV file into a DataFrame
    def _clean(self):
        df = pd.read_csv("S&P500.csv")

        # Display the column names and a few rows of the DataFrame to verify
        #print(df.columns)
        #print(df.head())

        # Define the mapping dictionary
        sector_mapping = {
            "Communication Services": 1,
            "Consumer Discretionary": 2,
            "Consumer Staples": 3,
            "Energy": 4,
            "Financials": 5,
            "Health Care": 6,
            "Industrials": 7,
            "Information Technology": 8,
            "Materials": 9,
            "Real Estate": 10
        }
        # Define the mapping function
        def map_sector(sector):
            return sector_mapping.get(sector, 0)  # Return 0 if the sector is not found
        # Apply the mapping function to the "GICS SECTOR" column
        df['GICS_SECTOR_NUMERIC'] = df['GICS Sector'].apply(map_sector)
        # Print the unique values to check the mapping
        print(df['GICS_SECTOR_NUMERIC'].unique())
        # Check a sample of the DataFrame to verify the new column
        # Sort the DataFrame based on the numeric values
        sorted_df = df.sort_values(by='GICS_SECTOR_NUMERIC')
        # Print the sorted DataFrame to verify
        result_list = sorted_df[['Symbol', 'GICS_SECTOR_NUMERIC']].to_records(index=False).tolist()
        return result_list

    def _Jsonclean(self,payload):
        payload_df = pd.DataFrame(payload, index=[0])
        payload_df['GICS Sector'] = payload_df['GICS Sector'].apply(
            lambda x: 1 if x == 'Communication Services' else
                      2 if x == 'Consumer Discretionary' else
                      3 if x == 'Consumer Staples' else
                      4 if x == 'Energy' else 
                      5 if x == 'Financials' else
                      6 if x == 'Health Care' else
                      7 if x == 'Industrials' else
                      8 if x == 'Information Technology' else
                      9 if x == 'Materials' else 
                      10 if x == 'Real Estate' else
                      0
        )
        num = int(payload_df['GICS Sector'])
        initialbucket = self._sort()
        sortedate = initialbucket[num]
        print("this is sortedate:" + str(sortedate[1][0]))
        n=len(sortedate)
        for i in range(n - 1):
            swapped = False
            for j in range(0, n - i - 1):
                if sortedate[j][0] > sortedate[j + 1][0]:
                    sortedate[j], sortedate[j + 1] = sortedate[j + 1], sortedate[j]
                    swapped = True
            if not swapped:
                break
            print(str(sortedate))
        
        
        return sortedate
    def _sort(self):
        result_list = self._clean()  # Corrected the method call
        print(result_list)
        unique = self.data['GICS Sector'].unique().tolist()
        print(unique)
        print(len(unique))
        initialbucket = []
        for i in unique:
            newbucket = []
            initialbucket.append(newbucket)
        print(initialbucket)
        for i in result_list:
            print(i[1])
            sortnum = i[1]
            initialbucket[sortnum].append(i)
        print(initialbucket)
        return initialbucket
    @classmethod
    def get_instance(cls):
        """Gets, and conditionally cleans and builds, the singleton instance of the Food model."""
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
        return cls._instance
def initstock():
    Stocksort.get_instance()


        
        