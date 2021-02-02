from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = "Passw0rd" #一个字符串密码
#在此登录的是root用户，要填上密码如123456，MySQL默认端口是3306。并填上创建的数据库名如youcaihua
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:passw0rd@127.0.0.1:3306/pytest?charset=utf8"
#设置下方这行code后，在每次请求结束后会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)#实例化数据库对象，它提供访问Flask-SQLAlchemy的所有功能


'''定义模型，建立关系'''
class Role(db.Model):#所有模型的基类叫 db.Model，它存储在创建的SQLAlchemy实例上。
    #定义表名
    __tablename__ = 'roles'

    #定义对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    #__repr__()方法显示一个可读字符串，虽然不是完全必要，不过用于调试、测试是很不错的。
    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    device = db.relationship('Device', backref='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Device(db.Model):
    __tablename__ = 'device' #设备
    id = db.Column(db.Integer,primary_key=True)
    imei = db.Column(db.String(15), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return '<User {}>'.format(self.imei)

'''进行数据库操作'''
if __name__ == '__main__':
    #删除旧表
    db.drop_all()
    db.create_all()#创建新表

    #给Role表，插入数据，3种角色
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')

    #role属性也可使用，虽然它不是真正的数据序列，但却是一对多关系的高级表示。给User表插入3条数据
    user_john = User(username='john', role=admin_role)
    user_susan = User(username='susan', role=user_role)
    user_david = User(username='david', role=mod_role)

    device1 = Device(imei="12345678901", user=user_john)
    device2 = Device(imei="2222222222", user=user_susan)

    #在将对象写入数据库之前，先将其添加到会话中，数据库会话db.session和Flask session对象没有关系，数据库会话也称 事物 译作Database Transaction。
    db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
    #提交会话到数据库
    db.session.commit()

    #修改roles名
    admin_role.name = 'Administrator'
    db.session.add(admin_role)
    db.session.commit()#注意：删除 和插入、更新一样，都是在数据库会话提交后执行

    #测试1 列出user_john用户的所有设备
    print(Device.query.filter_by(user=user_john).all())

    #测试2 已知imei为2222222222的设备，列出用户名字
    print(Device.query.filter_by(imei="2222222222").first().user)