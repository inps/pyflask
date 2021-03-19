
from flask import Flask, jsonify,abort,g
from flask_httpauth import HTTPTokenAuth



app = Flask(__name__)


auth = HTTPTokenAuth(scheme='Token')
tokens = {
"secret-token-1": "john",
"secret-token-2": "susan"
}
# 回调函数，验证 token 是否合法
@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = tokens[token]
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