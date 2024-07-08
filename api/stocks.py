import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
#from auth_middleware import token_required
from model.users import User, Stocks, Stock_Transactions, NewTransactractionlog, currentprice, usermoney, newquantity, updatemoney, numstockowned, filterdb,updatestockprice,querytables
from sqlalchemy import func, case, select
#from auth_middleware1 import token_required1
import sqlite3
from __init__ import app, db, cors, dbURI
import requests







from model.users import Stocks,User,Stock_Transactions

stocks_api = Blueprint('stocks_api', __name__,
                   url_prefix='/api/stocks')
api = Api(stocks_api)

class StocksAPI(Resource):
    class _Displaystock(Resource):
        #@token_required1("Admin")
        
        def get(self):
            #updates stock price:
            topstock = True
            stocks = updatestockprice(topstock=topstock)
            print(stocks)
            api_key = 'OyGEcU5tCO127eOKHqoraOGY0TNAwlFS'  # Replace with your FMP API key
            #F2RXN9arcI1Yyh0CSkmHGarjMIpfZ2ow
            #xAxPbodLC12nNCwa5gHiK6YZVQecllPA
            for stock in stocks:
                #print("this is stock:"+ stock)
                symbol = stock.symbol
                url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    
                    if data:  # Check if the list is not empty
                        latest_price = data[0].get('price')
                        latest_quantity = data[0].get('marketCap')
                        # Use .get() to avoid KeyError
                        if latest_price is not None:
                            updatestockprice(isloop = True,latest_price= latest_price,stock=stock)
                            print(f"Updated price for {symbol} to {latest_price}")
                        else:
                            print(f"Price data not found for {symbol}")
                    else:
                        print(f"Empty data for {symbol}")
                else:
                    print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")                          
            #displays database data:
            json_ready = filterdb(display=stocks)
            #print("this is " + str(json_ready))
            return jsonify(json_ready)
    class _Sortdisplay(Resource):
        def post(self):
            body = request.get_json()
            #print(body)
            isloop = False
            stocks = updatestockprice(body,isloop) 
            returnlist = []
            newlist = []
            json_ready = filterdb(display=stocks)
            for stock in body:
                sym = stock[0]
                #print("this is symbol" + sym)
                transaction = querytables(body,type= sym,table=Stocks)
                #print("this is transacotin: " + str(transaction))
                returnlist.append(transaction)
            #print("this is list: " + str(returnlist))
            for i in returnlist:
                json_ready = filterdb(display=i)
                #print("this is json" + str(json_ready[0]))
                new_json_ready = json_ready[0]
                newlist.append(new_json_ready)
            #print("this is new list" + str(newlist))
            data = jsonify(newlist)
            return data
    ##class _Singleupdata0(Resource):
    ##    # works old
    ##    def post(self):
    ##        #updates stock price:
    ##        body = request.get_json()
    ##        symbol = body.get("symbol")
    ##        print("this is body: " + str(symbol))
    ##        api_key = 'xAxPbodLC12nNCwa5gHiK6YZVQecllPA'  # Replace with your FMP API key
    ##        url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
    ##        stocks = Stocks.query.all()
    ##        response = requests.get(url)
    ##        json_ready = [stock.read() for stock in stocks]
    ##        print("this is jsonready:" + str(json_ready))
    ##        list1 = [item for item in json_ready if item.get('symbol') == symbol]
    ##        print(str(list1))
    ##        for stock in stocks:
    ##            if stock.symbol == symbol:
    ##                
    ##                if response.status_code == 200:
    ##                    data = response.json()
    ##                    
    ##                    if data:  # Check if the list is not empty
    ##                        latest_price = data[0].get('price')
    ##                        latest_quantity = data[0].get('marketCap')
    ##                        # Use .get() to avoid KeyError
    ##                        if latest_price is not None:
    ##                            print("this is stock:" + str(stock))
    ##                            stock.sheesh = latest_price
    ##                            price = stock.sheesh
    ##                            #stock.quantity =latest_quantity
    ##                            db.session.commit()
    ##                            print(f"Updated price for {symbol} to {latest_price}")
    ##                        else:
    ##                            print(f"Price data not found for {symbol}")
    ##                    else:
    ##                        print(f"Empty data for {symbol}")
    ##                else:
    ##                    print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
    ##                newprice = list1[0]["sheesh"]
    ##                print("this is new price" +  str(price))
    ##                data = jsonify(str(price))
    ##                print("this is data" + str(data))
    ##        return data 
    class _Singleupdata(Resource):
        def post(self):
            #updates stock price:
            body = request.get_json()
            symbol = body.get("symbol")
            isloop = False
            api_key = 'xAxPbodLC12nNCwa5gHiK6YZVQecllPA'  # Replace with your FMP API key
            url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
            stocks = updatestockprice(body,isloop)
            response = requests.get(url)
            for stock in stocks:
                if stock.symbol == symbol:
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if data:  # Check if the list is not empty
                            latest_price = data[0].get('price')
                            # Use .get() to avoid KeyError
                            if latest_price is not None:
                                print("this is stock:" + str(stock))
                                isloop = True
                                price = updatestockprice(body,isloop,latest_price,stock)
                                print(f"Updated price for {symbol} to {latest_price}")
                            else:
                                print(f"Price data not found for {symbol}")
                        else:
                            print(f"Empty data for {symbol}")
                    else:
                        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
                    print("this is new price" +  str(price))
                    data = jsonify(str(price))
                    print("this is data" + str(data))
            return data           
    ##class _Transactionsdisplay(Resource):
    ## not using
    ##    #@token_required1("Admin")
    ##    
    ##    def get(self):
    ##        transaction = Stock_Transactions.query.all()
    ##        json_ready = [transactions.read() for transactions in transaction]
    ##        return jsonify(json_ready)
    
    ##class _Transaction2(Resource):
    ##    ## old code: still working 
    ##    def post(self):
    ##        body = request.get_json()
    ##        quantitytobuy = body.get('buyquantity')
    ##        uid = body.get('uid')
    ##        isbuy = True
    ##        symbol = body.get('symbol')
    ##        newquantity = body.get('newquantity')
    ##        ## update for stocks table to change the amound of stocks left
    ##        stocks = Stocks.query.all()
    ##        json_ready = [stock.read() for stock in stocks]
    ##        list1 = [item for item in json_ready if item.get('symbol') == symbol]
    ##       
    ##        user_ids = User.query.filter(User._uid == uid).value(User.id)
    ##      
    ##        print(user_ids)
    ##       
    ##        usermoney = User.query.filter(User._uid == uid).value(User._stockmoney)
    ##        
    ##        print(usermoney)
    ##      
    ##        currentstockmoney = currentprice(body)
    ##        print("this is current money" + str(currentstockmoney))
    ##        if (usermoney > currentstockmoney*quantitytobuy):
    ##            ## updates stock quantity in stocks table
    ##            tableid = list1[0]['quantity']
    ##            #print(tableid)
    ##            tableid = list1[0]['id']
    ##            print("this is tableid" + str(tableid))
    ##            tableid = Stocks.query.get(tableid)
    ##            print("this is tableid" + str(tableid))
    ##            tableid.update(quantity=newquantity )
    ##            db.session.commit()
    ##            ## updates user money
    ##            updatedusermoney = usermoney - (currentstockmoney*quantitytobuy)
    ##            print(updatedusermoney)
    ##            tableid_user = User.query.get(user_ids)
    ##            print(tableid_user)
    ##            tableid_user.stockmoney = updatedusermoney
    ##            db.session.commit()
    ##            ## creates log for transaction
    ##            transactionamount = (currentstockmoney*quantitytobuy)
    ##            db.session.commit()
    ##            
    ##            NewTransactractionlog(body,transactionamount,isbuy)
##
    ##        else:
    ##            return jsonify({'error': 'Insufficient funds'}), 400
    class _Transaction3(Resource):
        def post(self):
            body = request.get_json()
            quantitytobuy = body.get('buyquantity')
            isbuy = True
            # Current price of stock
            currentstockmoney = currentprice(body)
            # Amount of money user has
            userbal = usermoney(body)
            if (userbal >= currentstockmoney*quantitytobuy):
                # Cretes a log for transaction
                transactionamount = (currentstockmoney*quantitytobuy)
                NewTransactractionlog(body,transactionamount, isbuy)
                # Updates stock quantity in stock table
                newquantity(body,isbuy)
                # Updates user money
                newbal = userbal - (currentstockmoney*quantitytobuy)
                updatemoney(body,newbal)
            else:
                return jsonify({'error': 'Insufficient funds'}), 400
            
                        
                
            
    ##class _Transactionsdisplayuser0(Resource):
    ##    # old sttill works
    ##    def post(self):
    ##        body = request.get_json()
    ##        uid = body.get('uid')
    ##        print(uid)
    ##        # Save uid as an instance variable to access it in other methods
    ##        self.uid = uid
    ##        transactions = Stock_Transactions.query.all()
    ##        json_ready = [transaction.read() for transaction in transactions]
    ##        
    ##        # Filter transactions based on uid
    ##        filtered_transactions = [item for item in json_ready if item.get('uid') == uid]
    ##        print("test")
    ##        print(json_ready)
    ##        return jsonify(filtered_transactions)
    class _Transactionsdisplayuser(Resource):
        def post(self):
            body= request.get_json()
            data = filterdb(body)
            return jsonify(data)
    ##class _Stockmoney(Resource):
        ## old code still working
    ##    def post(self):
    ##        body = request.get_json()
    ##        uid = body.get('uid')
    ##        print (uid)
    ##        users = User.query.all()
    ##        json_ready = [user.read() for user in users]
    ##    # Filter transactions based on uid
    ##        filtered_transactions = [item for item in json_ready if item.get('uid') == uid]
    ##        print("test")
    ##        print(filtered_transactions[0]['stockmoney'])
    ##        return jsonify(filtered_transactions[0]['stockmoney'])
    class _Stockmoney1(Resource):
        def post(self):
            body = request.get_json()
            return jsonify(usermoney(body))
    class _Portfolio2(Resource):
        def post(self):
            body = request.get_json()
            for_portfolio = True
            symbol_list = filterdb(body,for_portfolio)
            i = 0
            portfolio_data = []
            for i in symbol_list:
                totalquantity = numstockowned(body,for_portfolio,i)
                if totalquantity == 0:
                    pass
                else:
                    currentstockprice = currentprice(body,i)
                    value = currentstockprice * totalquantity
                    payload = {
                            "SYMBOL": i,
                            "TOTAL_QNTY": totalquantity,
                            "VALUE": value
                        }
                    portfolio_data.append(payload)
            return {"portfolio": portfolio_data}, 200
                    
            
            
    ##class _Portfolio3(Resource):
    ### old working code
    ##    def post(self):
    ##        body = request.get_json()
    ##        uid = body.get('uid')
    ##        
    ##        symbols_list = display(body,for_portfolio= True)
    ##        print("this is list:")
    ##        print(symbols_list)
    ##        i = 0
    ##        portfolio_data = []
    ##        for i in symbols_list:
    ##            #print(i)
    ##            # to find # of stock bought
    ##            buyquantity = (
    ##                db.session.query(
    ##                    Stock_Transactions._symbol,
    ##                    func.sum(Stock_Transactions._quantity).label("total_quantity")
    ##                )
    ##                .filter(Stock_Transactions._uid == uid, Stock_Transactions._symbol == i, Stock_Transactions._transaction_type == 'buy')
    ##                .group_by(Stock_Transactions._symbol)
    ##                .all()
    ##            )
    ##            quantitybuy= buyquantity[0][1]
    ##            # to find stocks sold
    ##            sellquantity = (
    ##                db.session.query(
    ##                    Stock_Transactions._symbol,
    ##                    func.sum(Stock_Transactions._quantity).label("total_quantity")
    ##                )
    ##                .filter(Stock_Transactions._uid == uid, Stock_Transactions._symbol == i,Stock_Transactions._transaction_type == 'sell' )
    ##                .group_by(Stock_Transactions._symbol)
    ##                .all()
    ##            )
    ##            #print("this is sellquantity")
    ##            value = 0
    ##            #checks if the is a sell
    ##            if not sellquantity:
    ##                totalstock = quantitybuy
    ##                if totalstock == 0:
    ##                    pass
    ##                else:
    ##                    print("symbol:")
    ##                    print(i)
    ##                    print("this is quantity:")
    ##                    print(quantitybuy)
    ##                    stockprice = Stocks.query.filter(Stocks._symbol == i).value(Stocks._sheesh)
    ##                    value = totalstock*stockprice
    ##                    print("this is value:")
    ##                    print(value)
    ##                    payload = {
    ##                        "SYMBOL": i,
    ##                        "TOTAL_QNTY": totalstock,
    ##                        "VALUE": value
    ##                    }
    ##                    #for i in symbols_list
    ##                    
    ##                    portfolio_data.append(payload)      
    ##                    print("this is portfolio_data:")
    ##                    print(portfolio_data)   
    ##            else:
    ##                quantitysell = sellquantity[0][1]
    ##                totalstock = quantitybuy -quantitysell
    ##                if totalstock == 0:
    ##                    pass
    ##                else:
    ##                    
    ##                    #    print(sellquantity)
    ##                    #value
    ##                    #print("total quantity:")
    ##                    #print(totalstock)
    ##                    stockprice = Stocks.query.filter(Stocks._symbol == i).value(Stocks._sheesh)
    ##                    value = totalstock*stockprice
    ##                    print("this is symbol")
    ##                    print(i)
    ##                    print("this is quantity")
    ##                    print(totalstock)
    ##                    print("this is value")
    ##                    print(value)
    ##                    payload = {
    ##                        "SYMBOL": i,
    ##                        "TOTAL_QNTY": totalstock,
    ##                        "VALUE": value
    ##                    }
    ##                    
    ##                    #for i in symbols_list
    ##                    
    ##                    portfolio_data.append(payload)      
    ##                    print("this is portfolio_data:")
    ##                    print(portfolio_data)
    ##        return {"portfolio": portfolio_data}, 200
    ##class _SellStock(Resource):
    ##    # old still work
    ##    def post(self):
    ##        # getting key variables from frontend
    ##        body = request.get_json()
    ##        symbol = body.get('symbol')
    ##        uid = body.get('uid')
    ##        quantity = body.get('quantity')
    ##        #other variables:
    ##        transactiontype = 'sell'
    ##        #SQL taking data from transation table
    ##        result = db.session.query(
    ##            Stock_Transactions._symbol.label("SYMBOL"),
    ##            (func.sum(case([(Stock_Transactions._transaction_type == 'buy', Stock_Transactions._quantity)], else_=0)) -
    ##            func.sum(case([(Stock_Transactions._transaction_type == 'sell', Stock_Transactions._quantity)], else_=0))
    ##            ).label("TOTAL_QNTY"),
    ##            (func.sum(Stock_Transactions._quantity * Stocks._sheesh)).label("VALUE"),
    ##        ).join(Stocks, Stocks._symbol == Stock_Transactions._symbol) \
    ##        .filter(Stock_Transactions._uid == uid, Stock_Transactions._symbol == symbol) \
    ##        .group_by(Stock_Transactions._symbol) \
    ##        .all()
    ##        print("this is result1"+str(result))
    ##        ownedstock = result[0][1]
    ##        print(ownedstock)
    ##        #logic for selling stock
    ##        if (ownedstock >= quantity):
    ##            #logic for transaction log
    ##            sellquantity = -quantity
    ##            stocks = Stocks.query.all()
    ##            json_ready = [stock.read() for stock in stocks]
    ##            list1 = [item for item in json_ready if item.get('symbol') == symbol]
    ##            currentprice = list1[0]['sheesh']
    ##            transactionamount = currentprice*quantity
    ##            Inst_table = Stock_Transactions(uid=uid, symbol=symbol,transaction_type=transactiontype, quantity=quantity, transaction_amount=transactionamount)
    ##            print(Inst_table)
    ##            Inst_table.create()   
    ##            db.session.commit()
    ##            #logic for updating money in user table
    ##            users = User.query.all()
    ##            json_ready = [user.read() for user in users]
    ##            list2 = [item for item in json_ready if item.get('uid') == uid]
    ##            currentmoney = list2[0]['stockmoney']
    ##            newmoney = currentmoney + transactionamount
    ##            user_ids = User.query.filter(User._uid == uid).value(User.id)
    ##            tableid_user = User.query.get(user_ids)
    ##            print(tableid_user)
    ##            tableid_user.stockmoney = newmoney
    ##            db.session.commit()
    ##            ### update quantity in stock table
    ##            tableid = list1[0]['quantity']
    ##            print(tableid)
    ##            newquantity = tableid + quantity
    ##            tableid = list1[0]['id']
    ##            tableid = Stocks.query.get(tableid)
    ##            tableid.update(quantity=newquantity )
    ##            db.session.commit()
    ##             # Call the _Graph class to generate and save the graph
    ##            return {'message': 'Stock sold successfully'}, 200
    ##        else:
    ##            return {'message': 'Insufficient stock quantity to sell'}, 400
    class _SellStock1(Resource):
        def post(self):
            body = request.get_json()
            isbuy = False
            quantity = body.get('quantity')
            # gets number of stock currently owned by user
            ownedstock = numstockowned(body)
            # Current price of stock
            currentstockmoney = currentprice(body)
            # Amount of money user has
            userbal = usermoney(body)
            if (ownedstock >= quantity):
                # Cretes a log for transaction
                transactionamount = (currentstockmoney*quantity)
                NewTransactractionlog(body,transactionamount, isbuy)
                # Updates stock quantity in stock table
                newquantity(body,isbuy)
                # Updates user money
                newbal = userbal + (currentstockmoney*quantity)
                updatemoney(body,newbal)
                return {'message': 'Stock sold successfully'}, 200
            else:
                return  {'message': 'Insufficient stock quantity to sell'}, 400
                
            
            
    class _Owned(Resource):
        def post(self):
            body = request.get_json()
            uid = body.get("uid")
            listdata = [[0,1000]]
            transaction = querytables(body,type= '_uid',table=Stock_Transactions)
            #sortedtransactio = transaction[0]
            #print("this is transactionx:"+str(sortedtransactio.uid))
            #print("this is transactiony:"+str(sortedtransactio.transaction_type))
            x = 1
            totalamount = 1000
            for i in transaction:
                ##y=i.id-1
                ##print("this is y:" + str(y))
                ##transactionamount = transaction[y]
                transactionmoney = i.transaction_amount

                
                if str(i.transaction_type) == "buy":
                    
                    totalamount = totalamount - transactionmoney
                    print("this is totalamount:" + str(totalamount))
                    list1 = [x,totalamount]
                    listdata.append(list1)
                if str(i.transaction_type) == "sell":
                    totalamount = totalamount + transactionmoney
                    
                    list1 = [x,totalamount]
                    listdata.append(list1)
                x += 1
            data = jsonify(listdata)
            return data



                    
                
            
                
        
            

            
            
            
        
    api.add_resource(_Displaystock, '/stock/display')
    ##api.add_resource(_Transactionsdisplay, '/transaction/displayadmin')
    api.add_resource(_Transactionsdisplayuser, '/transaction/display')
    api.add_resource(_Transaction3, '/transaction')
    api.add_resource(_Stockmoney1, '/stockmoney')
    api.add_resource(_Portfolio2, '/portfolio')
    api.add_resource(_SellStock1, '/sell')
    api.add_resource(_Owned, '/owned')
    api.add_resource(_Sortdisplay, '/sortdisplay')
    api.add_resource(_Singleupdata, '/singleupdate')


            
        
    
        
         