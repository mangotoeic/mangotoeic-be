from mangotoeic.ext.db import db

class VocabDao():

    @classmethod
    def find_all(cls):
        return cls.query.all
    
    @classmethod
    def add_vocab(cls, userid, vocabId, newv):
        add_vocab = cls.query.filter(userid == userid, vocabId != vocabId).add(newv)
        return add_vocab
    
    @classmethod
    def delete_vocab(cls, userid, vocabId):
        del_vocab = cls.query.filter(userid == userid, vocabId == vocabId).delete(vocabId)
        return del_vocab
