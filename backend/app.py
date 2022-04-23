from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import pymongo




app = Flask(__name__)



import mongoconn

client = mongoconn.retrieve_client()
import urls

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0",port=5000)