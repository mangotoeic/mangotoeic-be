from mangotoeic.ext.db import db
from mangotoeic.odap.dto import OdapDto
from mangotoeic.odap.pro import OdapPro
import pandas as pd
import json

class OdapDao():

    @classmethod
    def find_all(cls):
        sql = cls.query
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))
    
    @classmethod
    def add_odap(cls, userid, qId, newq):
        add_odap = cls.query.filter(userid == userid, qId != qId).add(newq)
        return add_odap
    
    @classmethod
    def delete_odap(cls, userid, qId):
        del_odap = cls.query.filter(userid == userid, qId == qId).delete(qId)
        return del_odap