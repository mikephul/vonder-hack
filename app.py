import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from flask import Flask
from flask import request
from flask import jsonify

import time

cred = credentials.Certificate('vonder-44d1a-firebase-adminsdk-61wot-1ff1bfc63e.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vonder-44d1a.firebaseio.com/'
})

app = Flask(__name__)

# Example CRUD operation for firebase
# For more plese see
# https://firebase.google.com/docs/database/admin/save-data
@app.route('/create', methods=['GET'])
def create():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    age = request.args.get('age')
    ref = db.reference('users')
    ref.child(user_id).set({
       'name': name,
       'age': age
    })
    text = {
        "messages": [{
            "text": "Successfully Created"
        }]
    }
    return jsonify(text)

@app.route('/read', methods=['GET'])
def read():
    user_id = request.args.get('user_id')
    ref = db.reference('users')
    user = ref.child(user_id).get()
    text = {
        "messages": [{
            "text": "user name is " + user["name"]
        },
        {
            "text": "user age is " + user["age"]
        }]
    }
    return jsonify(text)

@app.route('/update', methods=['GET'])
def update():
    user_id = request.args.get('user_id')
    age = request.args.get('age')
    ref = db.reference('users')
    ref.child(user_id).update({
       'age': age
    })
    text = {
        "messages": [{
            "text": "user age is now " + age
        }]
    }
    return jsonify(text)

@app.route('/delete', methods=['GET'])
def delete():
    user_id = request.args.get('user_id')
    ref = db.reference('users')
    ref.child(user_id).delete()
    text = {
        "messages": [{
            "text": "Successfully remove user_id " + user_id
        }]
    }
    return jsonify(text)

@app.route('/createScore', methods=['GET'])
def createScore():
    user_id = request.args.get('messenger user id')
    teacher_id = request.args.get('teacher id')
    question_id = request.args.get('question id')
    is_correct = request.args.get('is correct')
    score = request.args.get('score')
    timestamp = time.time()

    ref = db.reference('scores')
    question = ref.child(user_id).child(teacher_id).child(question_id)
    print(question.get())
    if question.get() is not None:
        text = {
            "messages": [{
                "text": "เอ๊ะ ตอบไปแล้วนี่ ขอไม่บันทึกคะแนนซ้ำนะคะ"
            }]
        }
    else:
        question.set({
            "is_correct": is_correct,
            "score": score,
            "timestamp": timestamp
        })
        text = {
            "messages": [{

                "text": "บวก " + score + " เรียบร้อยจ่ะ"
            }]
        }
    return jsonify(text)

if __name__=="__main__":

    # For dev run below
    app.run(debug=True)

    # For production run below
    # app.run(host='0.0.0.0')