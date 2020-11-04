from mangotoeic.ext.db import db, openSession,engine
import pandas as pd
import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
import pickle

import os
basedir= os.path.dirname(os.path.abspath(__file__))
Session = openSession()
session = Session()

class VocablistPro:
    def __init__(self):
        self.fpath = ''
    
class VocablistDto(db.Model):
    __tablename__ ='vocablist'
    __table_args__={'mysql_collate':'utf8_general_ci'}
    # id = db.Column(db.Integer,primary_key=True, index=True)
    vocab = db.Column(db.String(50),primary_key=True)
    # vocabs = db.relationship("VocabDto", backref='vocablist2',lazy=True)
    # vocabs2 = db.relationship("VocabdictDto", backref='vocablist',lazy=True)  
