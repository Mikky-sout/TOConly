from flask import Flask,render_template
from WebReader import getJSON
app = Flask(__name__)

@app.route('/')
def index():
    data = getJSON()
    return render_template('index.html',database=data)

@app.route('/hi')
def name():
    name = 'shiro'
    age = 23
    return render_template('hi.html',myname = name,age = age)



if __name__ == '__main__':
    app.run()