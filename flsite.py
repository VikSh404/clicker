from flask import Flask, render_template, url_for, request, redirect
import redis
import os
REDIS_PORT=6379
HOST='redis'

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/index")
@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', title="Clicker")

@app.route("/reset")
def reset():
    #print(url_for('index'))
    conn = redis.Redis(host=HOST, port=REDIS_PORT)
    outValue=conn.delete('number')
    return redirect(url_for('index'))


@app.route("/api/number", methods=('GET', 'POST'))
def number():
    if request.method == 'GET':
        conn = redis.Redis(host=HOST, port=REDIS_PORT)
        outValue=conn.get('number')
        if outValue == None:
            outValue=0
            conn.set('number', 0)
        else:
            outValue=outValue.decode('utf-8')
    if request.method == 'POST':
        conn = redis.Redis(host=HOST, port=REDIS_PORT)
        outValue=conn.get('number')
        if outValue == None:
            outValue=0
            conn.set('number', 0)
        else:
            outValue=outValue.decode('utf-8')
            conn.set('number', int(outValue)+1)
    return str(outValue)


if __name__ == "__main__":
    app.run(debug=True)
