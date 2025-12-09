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
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # For realism, process form (e.g., print to console; extend to send email)
        print(f"Contact Form: Name={name}, Email={email}, Message={message}")
        return redirect(url_for('contact'))  # Redirect after submit
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)