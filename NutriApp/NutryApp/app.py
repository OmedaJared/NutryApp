from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/2')
def formulario():
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)