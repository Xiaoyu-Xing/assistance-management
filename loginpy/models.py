from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db

class Authority(db.Model):
    __tablename__ = 'authority'

    authorlevel = db.Column(db.Integer,primary_key=True)
    explanation = db.Column(db.String(255),nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    # 建立一个表user
    userid = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255),nullable=False)
    ssn=db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    address=db.Column(db.String(255))
    city=db.Column(db.String(255))
    state=db.Column(db.String(255))
    zipcode=db.Column(db.Integer)
    phone=db.Column(db.String(255))
    gender=db.Column(db.String(255))
    age=db.Column(db.Integer)
    authoritylevel=db.Column(db.Integer,db.ForeignKey('authority.authorlevel'))

    #
    # @property
    # def password(self):#外部使用
    #     return self.password
    #
    # @password.setter
    # def password(self,row_password):
    #     self.password=generate_password_hash(row_password)
    #
    # def check_password(self,row_password):
    #     result=check_password_hash(self.password,row_password)
    #     return result
#db.create_all()





