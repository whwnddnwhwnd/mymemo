from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

#client = MongoClient('mongodb://test:test@54.180.114.136',27017)
client = MongoClient('mongodb://test:test@localhost',27017)
db=client.wantkaist


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['post'])
def show():
    memos = list(db.memo.find({}))
    return jsonify({'result': memos})


@app.route('/save', methods=['post'])
def save():
    data = request.get_json()
    title = data['title']
    comment = data['comment']
    memos = list(db.memo.find({}, {'_id': True}).sort('_id', 1))
    if db.memo.find_one({"_id": 0}) is None:
        db.memo.insert({"title": title, "comment": comment, "_id": 0})
        return jsonify({'result': 200})
    temp = memos[-1]
    index = temp['_id']+1
    db.memo.insert({"title": title, "comment": comment, "_id": index})
    return jsonify({'result': 200})


@app.route('/delete', methods=['post'])
def delete():
    index = request.form['index']
    db.memo.remove({'_id': int(index)})
    return redirect('/')


@app.route('/update', methods=['post'])
def update():
    data = request.get_json()
    title = data['title']
    comment = data['comment']
    index = data['index']
    db.memo.update({'_id': int(index)}, {'$set': {'title': title,"comment":comment}})
    return jsonify({'result': 200})

@app.route('/find_one', methods=['post'])
def find_one():
    data = request.get_json()
    index = data['index']
    temp = db.memo.find_one({'_id':int(index)})
    return jsonify({'result': temp})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)