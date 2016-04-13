from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db,login_manager

class Role(db.Model):
    __tablename__ ='roles'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    users = db.relationship('User',backref='roles', lazy='dynamic')#lazy?

    def __repr__(self):
        return '<Role %r>'%self

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    email =db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))
    confirmed =db.Column(db.Boolean,default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')

    @password.setter
    def password(self,token):
        #存储的是根据password生成的hash序列，
        self.password_hash = generate_password_hash(token)

    #接受字符串password，但是此时存储的不是直接的password，而是hash序列，
    #所以不能直接比较，比较封装成check函数中
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirm_token(self,expiration=3600):#expiration截至日期
        s =Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dump({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False

        self.confirmed=True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self



@login_manager.user_loader
def load_user(user_id):
    ##因为id是主键，能用get()，常用方法还有：all(),first()
    return User.query.get(user_id)


