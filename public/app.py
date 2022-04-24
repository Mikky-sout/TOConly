from flask import Flask,render_template
import WebReader as wr
app = Flask(__name__)

@app.route('/')
def index():
    data = wr.getJSON()

    return render_template('index.html',data=data)
@app.route('/hi')
def name():
    name = 'shiro'
    age = 23
    return render_template('hi.html',myname = name,age = age)

if __name__ == '__main__':
    app.run()