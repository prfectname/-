from flask import Flask, render_template, request, jsonify, session
import pymysql

app = Flask(__name__)

app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        get_username = request.form.get('User')
        get_password = request.form.get('Password')

        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='typing', charset='utf8')
        cursor = db.cursor()
        cursor.execute("select * from users where username = '%s'" % (get_username))
        a = cursor.fetchall()
        password = ''
        for i in a:
            password = i[1]
        cursor.close()
        db.close()

        # print(password)
        # print(get_username)
        # print(get_password)

        if password == '':
            return jsonify('账户不存在')
        else:
            if int(get_password) == int(password):
                print('ssss')
                # return jsonify('登录成功')
                session["username"] = request.form.get("User")
                print(session)
                print('a')
                return jsonify('cg')
            else:
                return jsonify('密码错误')

    else:
        print(request.method)
        print('method bu dui')

    return render_template('login.html')


@app.route('/regist', methods=['POST', 'GET'])
def regist():
    if request.method == 'POST':
        get_username = request.form.get('User')
        get_password = request.form.get('Password')

        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='typing')
        cursor = db.cursor()
        cursor.execute("select * from users where username = '%s'" % (get_username))
        a = cursor.fetchall()
        password = ''
        for i in a:
            password = i[1]

        print(password)
        print(get_username)
        print(get_password)

        if password != '':
            cursor.close()
            db.close()
            # print('账号已存在')
            return jsonify('账号已存在')

        else:
            if password == '':
                cursor.execute("insert into users(username,password)values('%s','%s')" % (get_username, get_password))
                db.commit()
                db.close()
                print('注册成功')
                # return jsonify('注册成功')
            else:
                cursor.close()
                db.close()
                # print('注册失败')
                return jsonify('注册失败')

    else:
        print(request.method)
        print('method bu dui')

    return render_template('regist.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')
        print(name)
        print(content)
        db = pymysql.connect(host='localhost', user='root', password='123456', database='typing')
        cursor = db.cursor()
        try:
            cursor.execute("insert into upload(name,content)values('%s','%s')" % (name, content))
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()

    else:
        print(request.method)
        print('method bu dui')
    return render_template('upload.html')


@app.route('/caiji', methods=['POST', 'GET'])
def cj():
    if request.method == 'POST':
        cj = request.form.get('cj')
        username = session["username"]
        db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='typing', charset='utf8')
        cursor = db.cursor()
        print(cj)
        print(username)
        print('a')
        try:
            cursor.execute("insert into score(username,score)values('%s','%s')" % (username, cj))
            # cursor.execute("insert into upload(name,textarea)values('1','1')" )
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()

        return 'jjjj'


@app.route('/look', methods=['POST', 'GET'])
def look():
    db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='typing', charset='utf8')
    cursor = db.cursor()
    cursor.execute("select username from score order by score")
    a = cursor.fetchall()
    cursor.execute("select score from score  order by score")
    b = cursor.fetchall()

    username = []
    for row in a:
        first = row[0]
        username.append(first)
    print(username)

    score = []
    for row in b:
        second = row[0]
        score.append(second)

    test = {
        'username': username,
        'score': score
    }

    db.close()
    if request.method == 'POST':
        print(test,type(test))

        return test
    else:
        print('method bu dui')

    return render_template('look.html')


@app.route('/get_content', methods=['POST', 'GET'])
def get_content():
    if request.method == 'POST':
        # name = request.form.get('name')
        # content = request.form.get('content')
        # print(name)
        # print(content)
        db = pymysql.connect(host='localhost', user='root', password='123456', database='typing')
        cursor = db.cursor()
        # cursor.execute("insert into upload(name,content)values('%s','%s')" % (name,content))
        # db.commit()
        cursor.execute('select content from upload')
        a = cursor.fetchall()
        test = []
        for i in a:
            test.append(i[0])

        print(test)

        db.close()
        test = jsonify(test)
        return test
    else:
        print('method is ')


@app.route('/index')
def cg():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
