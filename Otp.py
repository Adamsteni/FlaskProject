from flask import Flask, render_template, request, redirect, url_for, session, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'kingteni3000@gmail.com'  # Replace with your email address
EMAIL_PASSWORD = 'kpnn mapv rwla keqj'  # Replace with your email password or app password

# Helper function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Redirect to the login page when the form is submitted
        return redirect(url_for('login'))
    return render_template('index.html')  # Render the index page when accessed

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        send_via = request.form.get('send_via')
        email = request.form.get('email')

        if send_via == 'email' and email:
            otp = generate_otp()
            session['otp'] = otp
            session['email'] = email

            # Send OTP directly within the login route
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = email
                msg['Subject'] = 'Your Verification Code'

                body = f'Your OTP is {otp}'
                msg.attach(MIMEText(body, 'plain'))

                # Set up the server and send the email
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()  # Secure the connection
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)

                flash('OTP sent successfully! Check your email.')  # Simple flash message
                print(f"OTP Sent To {email}") #to Show the otp was successfully sent
            except Exception as e:
                flash(f'Error sending OTP.Please try agin.')  # Simple error message incase of any issues met
                print(f"Error occurred while sending email: {e}") #To log the actual error
                return redirect(url_for('login'))

            # Redirect to the verify page after sending OTP
            return redirect(url_for('verify'))
        else:
            flash('Please select an OTP delivery method and enter the required details.')

    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_otp = request.form.get('otp')  # Get the OTP entered by the user
        if user_otp == session.get('otp'): #this is to check if the Otp matches the  OTP
            flash('Email verified successfully!')
            # Clear session data after successful verification
            session.pop('otp', None)
            session.pop('email', None)
            return redirect(url_for('successful'))  # Redirect to the index page after verification
        else:
            flash('Invalid OTP. Please try again.')
    return render_template('verify.html')

@app.route('/successful', methods=['GET'])
def successful():
    return render_template('successful.html')

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

