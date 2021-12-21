from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World'


@app.route('/get_content', methods=['POST', 'GET'])
def upload():
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

    return render_template('1.html')


if __name__ == '__main__':
    app.run()
