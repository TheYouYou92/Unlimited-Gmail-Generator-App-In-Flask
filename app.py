from flask import Flask, request, render_template, session, make_response
import itertools
import string
import csv
import io
import secrets

app = Flask(__name__)

app.secret_key = "df45sdf5ds1fsd5d51sf1sd5"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        #print(f"Email input: {email}")
        username, domain = email.split('@')
        combinations = generate_combinations(username)
        emails = [f"{username}@{domain}" for username in combinations]
        #print(f"Generated emails: {emails}")
        return render_template('index.html', emails=emails)
    return render_template('index.html')



def generate_combinations(username):
    parts = list(username)
    combinations = []

    for i in range(len(parts) - 1):
        for subset in itertools.combinations(range(1, len(parts)), i):
            temp_parts = parts.copy()
            for index in subset:
                temp_parts[index] = '.' + temp_parts[index]
            combinations.append(''.join(temp_parts))

    return combinations




@app.route('/plus', methods=['GET', 'POST'])
def plus():
    if request.method == 'POST':
        num = min(int(request.form.get('num')), 10000)
        email = request.form.get('email')
        #print(f"Email input: {email}")
        username, domain = email.split('@')
        combinations = generate_plus_combinations(username, num)
        emails = [f"{username}@{domain}" for username in combinations]
        #print(f"Generated emails: {emails}")
        session['emails'] = emails 
        return render_template('plus.html', emails=emails)
    return render_template('plus.html')


def generate_plus_combinations(username, num):
    combinations = []

    for i in range(num):  # Generate num combinations
        random_string = ''.join(secrets.SystemRandom().choices(string.ascii_lowercase + string.digits, k=5))
        combinations.append(username + '+' + random_string)

    return combinations

@app.route('/download')
def download():
    emails = session.get('emails', [])
    if not emails:
        return "No emails to download", 400

    si = io.StringIO()
    cw = csv.writer(si)
    
    for email in emails:
        cw.writerow([email])  # Write each email to a new row
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=emails.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True)
