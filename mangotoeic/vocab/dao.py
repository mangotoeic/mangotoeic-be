from mangotoeic.ext.db import db

class VocabDao():

    @classmethod
    def find_all(cls):
        return cls.query.all
    
    @classmethod
    def add_vocab(cls, userid, vocabid, newv):
        add_vocab = cls.query.filter(userid == userid, vocabid != vocabid).add(newv)
        return add_vocab
    
    @classmethod
    def delete_vocab(cls, userid, vocabid):
        del_vocab = cls.query.filter(userid == userid, vocabid == vocabid).delete(vocabid)
        return del_vocab
