from flask import Flask, render_template, request
import pandas as pd
import validate_email

app = Flask(__name__)

def is_valid_email(email):
    return validate_email.validate_email(email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def validate_emails():
    if 'file' not in request.files:
        return render_template('index.html', error='No file selected')

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected')

    if not file.filename.endswith('.xlsx'):
        return render_template('index.html', error='Invalid file format. Only Excel files (.xlsx) are supported.')

    try:
        df = pd.read_excel(file)
        emails = df['Email'].tolist()
        valid_emails = [email for email in emails if is_valid_email(email)]
        return render_template('index.html', valid_emails=valid_emails)

    except Exception as e:
        return render_template('index.html', error='Error reading the Excel file')

@app.route('/validate_email', methods=['POST'])
def validate_email_address():
    email = request.form['email']
    is_valid = is_valid_email(email)

    return render_template('index.html', email=email, is_valid=is_valid)

if __name__ == '__main__':
    app.run()
