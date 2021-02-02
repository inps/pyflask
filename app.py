
from flask import Flask, jsonify,abort

app = Flask(__name__)
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
    return 'Hello World'


if __name__ == '__main__':
    app.debug = True 
    app.run() 