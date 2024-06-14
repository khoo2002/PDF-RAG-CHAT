# save this as app.py
from flask import Flask, flash, request, redirect, url_for, render_template, make_response, send_from_directory, abort, jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
import os
import duckdb
import time
from rag import TestingChat
import json

# Class
# answer
class Answer():
    
    def __init__(self, question_id):
        self.question_id = question_id
        
    def setter(self, user_id, question_id, question, answer_text, created_at, answer_id='hi'):
        self.user_id = user_id
        self.question_id = question_id
        self.question = question
        self.answer_text = answer_text
        self.created_at = created_at

    @staticmethod
    def store_answer(answer_dict):
        conn = duckdb.connect("testing.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            answer_id INTEGER PRIMARY KEY ,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE SEQUENCE IF NOT EXISTS seq_answerid START 1;
        """)
        conn.close()
        conn = duckdb.connect("testing.db")
        result = conn.execute("""
        INSERT INTO answers VALUES (nextval('seq_answerid'),'{question_id}', '{answer_text}', '{created_at}');
        """.format(question_id=answer_dict['question_id'], answer_text=answer_dict['answer_text'], created_at=answer_dict['created_at'])).fetchall()
        conn.close()
        print(result)

    @staticmethod
    def get_answer(question_id):
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM answers WHERE question_id = '{}'".format(question_id)).fetchone()
        conn.close()
        if result:
            answers = []
            question_dict = {
                'answer_id': result[0],
                'question_id': result[1],
                'answer_text': result[2],
                'created_at': result[3]
            }
            answers.append(question_dict)

            return {'answer': answers}

        return None


# question
class Question():
    question_id = ""
    user_id = ""
    question = ""
    ip_address = ""
    endpoint = ""
    request_header = ""
    request_data = ""
    created_at = ""
    
    def __init__(self):
        hi = 0

    def setter(self,user_id, question, ip_address, endpoint, request_header, request_data, created_at, question_id='hi'):
        self.question_id = question_id
        self.user_id = user_id
        self.question = question
        self.ip_address = ip_address
        self.endpoint = endpoint
        self.request_header = request_header
        self.request_data = request_data
        self.created_at = created_at

    def query20results(page):
        per_page = 20
        offset = (page - 1) * per_page
        
        conn = duckdb.connect("testing.db")
        total_questions = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        total_pages = (total_questions + per_page - 1) // per_page
        
        result = conn.execute("SELECT * FROM questions ORDER BY created_at DESC LIMIT {} OFFSET {}".format(per_page, offset)).fetchall()

        questions = []
        for row in result:
            question_dict = {
                'question_id': row[0],
                'user_id': row[1],
                'question': row[2],
                'ip_address': row[3],
                'endpoint': row[4],
               'request_header': row[5],
               'request_data': row[6],
                'created_at': row[7]
            }
            
            # Get the answer text for this question
            answer_result = conn.execute("SELECT answer_text FROM answers WHERE question_id = {}".format(row[0])).fetchone()
            if answer_result:
                question_dict['answer_text'] = answer_result[0]
            else:
                question_dict['answer_text'] = None
            
            # Get the feedback for this question
            feedback_result = conn.execute("SELECT is_correct, reason FROM feedback WHERE answer_id IN (SELECT answer_id FROM answers WHERE question_id = {})".format(row[0])).fetchone()
            if feedback_result:
                question_dict['feedback'] = {
                    'is_correct': feedback_result[0],
                   'reason': feedback_result[1]
                }
            else:
                question_dict['feedback'] = None
            
            questions.append(question_dict)

        return {'questions': questions, 'total_pages': total_pages}

    def newQuestion(question_dict):
        conn = duckdb.connect("testing.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            request_header TEXT NOT NULL,
            request_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        );

        CREATE SEQUENCE IF NOT EXISTS seq_questionid START 1;
        """)
        conn.close()
        
        conn = duckdb.connect("testing.db")
        conn.execute("""
        INSERT INTO questions VALUES (nextval('seq_questionid'),'{user_id}', '{question}', '{ip_address}', '{endpoint}', '{request_header}', '{request_data}', '{created_at}') ON CONFLICT (question_id) DO NOTHING;
        """.format(user_id = question_dict['user_id'], question = question_dict['question'], ip_address = question_dict['ip_address'], endpoint = question_dict['endpoint'], request_header = question_dict['request_header'], request_data = question_dict['request_data'], created_at = question_dict['created_at'])).fetchall()
        
        result = conn.execute("SELECT * FROM questions WHERE question_id = currval('seq_questionid')").fetchone()
        conn.close()
        print(result)
        print(len(result))

        if result:
            tmQ = Question()
            tmQ.setter(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[0])
            return tmQ
        


    

# user
class User(UserMixin):
    id = ""
    username = ""
    password = ""
    role = ""
    timeCreated = "" 
    
    def __init__(self):
        hi = 0

    def setter(self,username, password, role, timeC, user_id='hi'):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.timeCreated = timeC
    
    def store(self):
        conn = duckdb.connect("testing.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE SEQUENCE IF NOT EXISTS seq_userid START 1;
        """)
        conn.close()
        conn = duckdb.connect("testing.db")
        result = conn.execute("""
        INSERT INTO users VALUES (nextval('seq_userid'),'{username}', '{password}', '{role}', '{timestamp}') ON CONFLICT (username) DO NOTHING;
        """.format(username=self.username, password=self.password, role=self.role, timestamp = self.timeCreated)).fetchall()
        conn.close()
        print(result)

    def update(self):
        hi = 1

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"
    
    def queryByID(user_id):
        conn = duckdb.connect("testing.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE SEQUENCE IF NOT EXISTS seq_userid START 1;
        """)
        conn.close()
        conn = duckdb.connect("testing.db")
        result = conn.execute("""
        SELECT user_id,username,password,role,created_at from users where user_id={userid};
        """.format(userid = user_id)).fetchall()
        conn.close()
        if result != []:
            userTmp = User()
            userTmp.setter(result[0][1],result[0][2],result[0][3],result[0][4],result[0][0])
            return userTmp
    
    def queryByUsername(username):
        print(username)
        conn = duckdb.connect("testing.db")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE SEQUENCE IF NOT EXISTS seq_userid START 1;
        """)
        conn.close()
        conn = duckdb.connect("testing.db")
        result = conn.execute("""
        SELECT user_id,username,password,role,created_at from users where username='{username}';
        """.format(username = username)).fetchall()
        conn.close()
        if result != []:
            userTmp = User()
            userTmp.setter(result[0][1],result[0][2],result[0][3],result[0][4],result[0][0])
            return userTmp


# Database
conn = duckdb.connect("testing.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS pdf_files (
    id INTEGER PRIMARY KEY,
    file_path TEXT,
    file_name TEXT
);

CREATE SEQUENCE IF NOT EXISTS seq_fileid START 1;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY ,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS seq_userid START 1;
             
CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    request_header TEXT NOT NULL,
    request_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);
             
CREATE SEQUENCE IF NOT EXISTS seq_questionid START 1;

CREATE TABLE IF NOT EXISTS answers (
    answer_id INTEGER PRIMARY KEY ,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS seq_answerid START 1;
             
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY ,
    answer_id INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS seq_feedbackid START 1;
             
CREATE TABLE IF NOT EXISTS api_access (
    access_id INTEGER PRIMARY KEY ,
    ip_address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS seq_accessid START 1;
             
CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY ,
    user_id INTEGER REFERENCES users(user_id),
    ip_address TEXT,
    endpoint TEXT,
    request_data JSON,
    response_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS seq_logid START 1;
             
""")
conn.close()

conn = duckdb.connect("testing.db")
result = conn.execute("""
INSERT INTO users VALUES (nextval('seq_userid'),'admin', 'adminMCMC123', 'admin', '{timestamp}') ON CONFLICT (username) DO NOTHING;
""".format(timestamp=datetime.datetime.now().isoformat())).fetchall()
conn.close()

conn = duckdb.connect("testing.db")
result = conn.execute("""
Select * from users;
""").fetchall()
conn.close()
print("")
print("Users:")
print(result)

conn = duckdb.connect("testing.db")
result = conn.execute("""
Select * from questions;
""").fetchall()
conn.close()
print()
print("Questions:")
print(result)
print()
print()
print()
print()

conn = duckdb.connect("testing.db")
result = conn.execute("""
Select * from answers;
""").fetchall()
conn.close()
print()
print("Answers:")
print(result)
print()
print()
print()
print()


conn = duckdb.connect("testing.db")
result = conn.execute("""
Select * from feedback;
""").fetchall()
conn.close()
print()
print("Feedback:")
print(result)
print()
print()
print()
print()


# variable
app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
UPLOAD_FOLDER = '/home/khoo/Downloads/llm/llama3/zhaowei_module/uploaded'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

ingesting = False

test = TestingChat()

@app.before_request
def limit_access():
    if request.remote_addr not in ['127.0.0.1', '192.168.0.0/16', '10.0.0.0/8']:  # Add your local network IP ranges here
        return 'Access denied', 403
    if ingesting:
        return 'Services will return soon. Try again later!', 503


# Login & Authentication
@login_manager.user_loader
def load_user(user_id):
    return User.queryByID(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.queryByUsername(username)
        
        if user and user.password == password:
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("adminHalo"))
            else:
                return redirect(url_for("userHalo"))
        return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        if role not in ["user", "admin"]:
            return render_template("register.html", error="Invalid role")
        user = User()
        user.setter(username, password, role, datetime.datetime.now().isoformat())
        user.store()        
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#page
@app.route("/")
def hello():
    return render_template("index.html")

@app.get("/admin")
@login_required
def adminHalo():
    if current_user.role!= "admin":
        return redirect(url_for("userHalo"))
    return render_template("admin.html")

@app.get("/user")
@login_required
def userHalo():
    if current_user.role!= "admin" and current_user.role!= "user":
        return redirect(url_for("login"))
    return render_template("user.html")

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.route("/questionlog", methods=["GET"])
@login_required
def questionlog():
    if current_user.role != "admin":
        return redirect(url_for("home"))
    return render_template("question.html")

# API
@app.route('/api/admin/file/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = duckdb.connect("testing.db")
            conn.execute("""
            INSERT INTO pdf_files 
            VALUES (nextval('seq_fileid'),'{file_path}', '{file_name}')
            ON CONFLICT (id) DO NOTHING;
            """.format(file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename), file_name = filename))
            conn.close()
        
        return "Success", 200
    else:
        return "Bad Request", 404

@app.route('/api/admin/file/get', methods=['POST','GET'])
def get_file():
    if request.method == 'GET':
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM pdf_files").fetchall()
        conn.close()
        response = make_response(result, 200)
        return  response
    else:
        return "Bad Request", 404

@app.route('/api/admin/file/get/<file>', methods=['POST','GET'])
def get_filename(file):
    if request.method == 'GET':
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM pdf_files").fetchall()
        conn.close()
        if(file in str(result)):
            try:
                if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],file))):
                    return send_from_directory(app.config['UPLOAD_FOLDER'], file)
                    # return send_from_directory(app.config['UPLOAD_FOLDER'], file, as_attachment=True)
            except FileNotFoundError:
                abort(404, 'File not found.')
        else:
            return "Not found in database", 404
    else:
        return "Bad Request", 404


@app.route('/api/admin/file/delete/<file>', methods=['POST','GET'])
def delete_file(file):
    if request.method == 'POST':
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM pdf_files").fetchall()
        conn.close()

        if(file in str(result)):
            conn = duckdb.connect("testing.db")
            result = conn.execute("DELETE FROM pdf_files WHERE file_name='{filename}';".format(filename=file)).fetchall()
            conn.close()

        if(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'],file))):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],file))
    
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM pdf_files").fetchall()
        conn.close()

        response = make_response(result, 200)
        return  response
    else:
        return "Bad Request", 404

@app.route('/api/admin/file/ingest', methods=['GET'])
def file_ingest():
    global ingesting
    if request.method == 'GET':
        ingesting = True
        test.ingest()
        ingesting = False
        response = make_response("Ingesting done!", 200)
        return response
    else:
        return "Bad Request", 404
    
@app.route('/api/admin/questions/<int:page>', methods=['GET'])
def question_page(page):
    if request.method == 'GET':
        res = Question.query20results(page)
        return jsonify(res), 200
    else:
        return "Bad Request", 404
    
@app.route('/api/admin/answers/<int:questionId>', methods=['GET'])
def get_answer(questionId):
    if request.method == 'GET':
        res = Answer.get_answer(questionId)
        return jsonify(res), 200
    else:
        return "Bad Request", 404

# user api

@app.route('/api/user/chat/', methods=['POST'])
@login_required
def prompting():
    if request.method == 'POST':
        json_dict = request.get_json()
        ip_address = request.remote_addr
        endpoint = request.path
        request_header = dict(request.headers)
        request_data = json_dict
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(current_user.id)
        # Record the data
        record = {
            'user_id': current_user.id,
            'question': json_dict['prompt'],
            'ip_address': ip_address,
            'endpoint': endpoint,
           'request_header': json.dumps(request_header),
           'request_data': json.dumps(request_data),
            'created_at': timestamp
        }

        tmpQ = Question.newQuestion(record)

        response_text = test.ask(json_dict['prompt'])

        # Store the answer
        answer_record = {
            'question_id': tmpQ.question_id,  # Use the same question ID as the question
            'answer_text': response_text,
            'created_at': timestamp
        }
        answer = Answer.store_answer(answer_record)
        answer = Answer.get_answer(tmpQ.question_id)
        answer_id = answer['answer'][0]['answer_id']
        return jsonify({'answer_text': response_text, 'answer_id': answer_id}), 200

    else:
        return "Bad Request", 404
    

@app.route('/api/user/feedback/', methods=['POST'])
@login_required
def get_feedback():
    if request.method == 'POST':
        json_dict = request.get_json()
        answer_id = json_dict['answer_id']
        is_correct = json_dict['is_correct']
        reason = json_dict['reason']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store the feedback
        feedback_record = {
            'answer_id': answer_id,
            'is_correct': is_correct,
            'reason': reason,
            'created_at': timestamp
        }

        conn = duckdb.connect("testing.db")
        conn.execute("""
        INSERT INTO feedback 
        VALUES (nextval('seq_feedbackid'),'{answer_id}', {is_correct}, '{reason}', '{timestamp}');
        """.format(answer_id=answer_id, is_correct=is_correct, reason=reason, timestamp=timestamp))
        conn.close()

        return make_response("Feedback recorded successfully", 200)

    else:
        return "Bad Request", 404

@app.route('/api/user/feedback/<int:answer_id>', methods=['GET'])
@login_required
def get_feedback_for_answer(answer_id):
    if request.method == 'GET':
        conn = duckdb.connect("testing.db")
        result = conn.execute("SELECT * FROM feedback WHERE answer_id={}".format(answer_id)).fetchall()
        conn.close()

        if result:
            feedback_dict = {
                'answer_id': result[0][1],
                'is_correct': result[0][2],
            'reason': result[0][3],
                'created_at': result[0][4]
            }
            return jsonify(feedback_dict), 200
        else:
            return "Feedback not found", 404

    else:
        return "Bad Request", 404

if __name__ == '__main__':
    app.run(debug=True, port=8001)