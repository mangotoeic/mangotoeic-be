from mangotoeic.ext.db import db, openSession,engine
import pandas as pd
import json
from typing import List
from flask import request, jsonify
from flask_restful import Resource, reqparse
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
    id: int = db.Column(db.Integer, index=True)
    vocab: str = db.Column(db.String(50), primary_key=True)
    vocabs = db.relationship("VocabDto", backref='vocablist',lazy=True)
    vocabs2 = db.relationship("VocabdictDto", backref='vocablist',lazy=True)
    