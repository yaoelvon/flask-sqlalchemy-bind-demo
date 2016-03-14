# -*- coding: utf-8 -*-

#
# @date 2016/03/11
# @auther yaoelvon
# @desc Flask-SQLAlchemy的bind功能例子代码
# @reference http://docs.jinkan.org/docs/flask-sqlalchemy/binds.html
#

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/auth'
app.config['SQLALCHEMY_BINDS'] = {
    'user': 'sqlite:///' + os.path.join(basedir, 'user_test.db')
}

db = SQLAlchemy(app)

class Role(db.Model):
    # 使用默认的SQLALCHEMY_DATABASE_URI数据库
    __tablename__ = 'roless'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='roless')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {0}>'.format(self.name)


class User(db.Model):
    # 使用特定指定的sqlite数据库
    __bind_key__ = 'user'
    __tablename__ = 'userss'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roless.id'))

    def __init__(self, username, role_id):
        self.username = username
        self.role_id = role_id

    def __repr__(self):
        return '<User {0}, {1}>'.format(self.username, self.role_id)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()

    role = Role("worker")
    db.session.add(role)
    db.session.commit()
    print role

    user = User("vwms", role.id)
    db.session.add(user)
    db.session.commit()
    print user

    app.run(debug='DEBUG')
