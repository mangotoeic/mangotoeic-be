from mangotoeic.ext.db import db

class OdapDao():

    @classmethod
    def find_all(cls):
        return cls.query.all
    
    @classmethod
    def add_odap(cls, userid, qId, newq):
        add_odap = cls.query.filter(userid == userid, qId != qId).add(newq)
        return add_odap
    
    @classmethod
    def delete_odap(cls, userid, qId):
        del_odap = cls.query.filter(userid == userid, qId == qId).delete(qId)
        return del_odap