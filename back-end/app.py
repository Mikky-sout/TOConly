from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {"name":'shiro',"age":23,"height":158}
    return render_template('index.html',data=data)

@app.route('/hi')
def name():
    name = 'shiro'
    age = 23
    return render_template('hi.html',myname = name,age = age)



if __name__ == '__main__':
    app.run()