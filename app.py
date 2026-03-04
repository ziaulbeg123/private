from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        submitted = True
        return redirect(url_for('contact', submitted=1))
    submitted = request.args.get('submitted')
    return render_template('contact.html', submitted=submitted)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)