import mysql.connector
import json

def saveToDB():
    shortData = open('shortData.json')
    prices = json.load(shortData)
    values = (
        prices['USD'],
        prices['AUD'],
        prices['EUR'],
        prices['BRL'],
        prices['CNY'],
        prices['GBP'],
        prices['HRK'],
        prices['INR'],
        prices['RON'],
        prices['KRW']
    )
    mydb = mysql.connector.connect(
        host="localhost",
        user="historyuser",
        password="password1!",
        database="historydb"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO history(USD,AUD,EUR,BRL,CNY,GBP,HRK,INR,RON,KRW) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    mycursor.execute(sql, values)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#saveToDB();