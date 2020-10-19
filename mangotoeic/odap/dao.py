from mangotoeic.ext.db import db

class OdapDao():

    @classmethod
    def find_all(cls):
        return cls.query.all
    
    @classmethod
    def add_odap(cls, userid, Qid, newq):
        add_odap = cls.query.filter(userid == userid, Qid != Qid).add(newq)
        return add_odap
    
    @classmethod
    def delete_odap(cls, userid, Qid):
        del_odap = cls.query.filter(userid == userid, Qid == Qid).delete(Qid)
        return del_odap