
from flask import Flask, jsonify,abort,g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere'
# 在Authorization 的Bearer方式进行认证
auth = HTTPTokenAuth(scheme='Bearer')

serializer = Serializer("secretkey", expires_in=600)
users = ['john', 'susan']



# 生成 token
for user in users:
    token = serializer.dumps({'username': user})
    print('Token for {}: {}'.format(user, token))

# 回调函数，对 token 进行验证
@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = serializer.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False







books = [
    {
        'id': 1,
        'title': u'论语',
        'auther': u'孔子',
        'price': 18
    },
    {
        'id': 2,
        'title': u'道德经',
        'auther': u'老子',
        'price': 15
    }
]

@app.route('/bookstore/api/v1/books', methods=['GET'])
@auth.login_required
def get_tasks():
    #return "Hello, %s!" % g.user
    return jsonify({'books': books})


@app.route('/bookstore/api/v1/books/<int:id>', methods=['GET'])
def get_task(id):
    for book in books:
        if book['id']==id:
            return jsonify({'book': book})
    abort(404)



@app.route('/')

def index():
    return 'Hello World  flask'


if __name__ == '__main__':
    app.debug = True 
    app.run() 