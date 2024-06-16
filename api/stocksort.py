from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pandas as pd
from model.stockfilter import Stocksort
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from flask_restful import Resource
from flask import Blueprint, jsonify, request 
from flask_restful import Api, Resource

stocks_sort = Blueprint('stocks_sort', __name__, url_prefix='/api/sort')
api = Api(stocks_sort)

class stockssort(Resource):
    
    def __init__(self):
        self.model = Stocksort()  
    def post(self):
        try:
            # get JSON data from the request
            payload = request.get_json()
            print(payload)
            stockModel = Stocksort.get_instance()
            # Predict the item purchased from bakery
            response = stockModel._Jsonclean(payload)
            print(response)
            
            return jsonify(response)

        except Exception as e:
            return jsonify({'error': str(e)})
        
api.add_resource(stockssort, '/sort')