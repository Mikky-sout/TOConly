from flask import Flask,render_template
import WebReader as wr
app = Flask(__name__)

@app.route('/')
def index():
    data = wr.getJSON()
    return render_template('/index.html',data=data)

app.run()