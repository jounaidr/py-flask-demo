from flask import Flask

app = Flask(__name__)

port = 8000
scores = {}

@app.route('/scores/<>') #shouldn't sort on each get
def get_scores():
    return 'test'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
