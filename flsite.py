from flask import Flask, render_template, render_template_string, url_for, request
import redis
import os
REDIS_PORT=6379

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
    conn = redis.Redis(port=REDIS_PORT)
    outValue=conn.delete('number')
    return str(outValue)

@app.route("/api/number", methods=('GET', 'POST'))
def number():
    if request.method == 'GET':
        conn = redis.Redis(port=REDIS_PORT)
        outValue=conn.get('number')
        if outValue == None:
            outValue=0
            conn.set('number', 0)
        else:
            outValue=outValue.decode('utf-8')
    if request.method == 'POST':
        conn = redis.Redis(port=REDIS_PORT)
        outValue=conn.get('number')
        if outValue == None:
            outValue=0
            conn.set('number', 0)
        else:
            outValue=outValue.decode('utf-8')
            conn.set('number', int(outValue)+1)
    return str(outValue)


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('path', i=111, thepath='111/reee/ggg'))

if __name__ == "__main__":
    app.run(debug=True)
