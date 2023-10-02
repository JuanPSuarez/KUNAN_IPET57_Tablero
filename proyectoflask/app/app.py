from flask import Flask, render_template

app=Flask(__name__)
app.config['TEMPLATES_FOLDER']='templates'

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/reporter')
def reporter():
    return render_template('reporter.html')

if __name__ == '__main__':
    app.run()