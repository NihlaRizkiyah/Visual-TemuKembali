# from app import app
# import os
# from flask import Flask, render_template, request
# import smtplib

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']

#         # Replace the placeholders with your email server details
#         smtp_server = 'your_smtp_server'
#         smtp_port = 587
#         smtp_username = 'your_email@example.com'
#         smtp_password = 'your_email_password'
#         to_email = 'farhanabdilah204@gmail.com'

#         # Create the email message
#         subject = 'New Contact Form Submission'
#         body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

#         # Send the email
#         try:
#             with smtplib.SMTP(smtp_server, smtp_port) as server:
#                 server.starttls()
#                 server.login(smtp_username, smtp_password)

#                 server.sendmail(smtp_username, to_email, f'Subject: {subject}\n\n{body}')

#             return 'Your message has been sent successfully!'
#         except Exception as e:
#             return f'Error sending the message. Please try again later. Error: {str(e)}'

#     return render_template('contact.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# port = int(os.getenv("PORT",5000))
# if __name__ == "__main__":
#     # app.run(host='0.0.0.0', port=port)
#     app.run(host='0.0.0.0', port=port)

from app import app
import os
from flask import Flask, render_template, request
import smtplib

app = Flask(__name__)

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/sendsmtp', methods=['POST'])
def sendsmtp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Replace the placeholders with your email server details
        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        smtp_username = 'farhanyutub068@gmail.com'
        smtp_password = 'uxwb mksa ieoz wjfm'
        to_email = 'farhanyutub068@gmail.com'

        # Create the email message
        subject = 'New Contact Form Submission'
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)

                server.sendmail(smtp_username, to_email, f'Subject: {subject}\n\n{body}')

            return 'Your message has been sent successfully!'
        except Exception as e:
            return f'Error sending the message. Please try again later. Error: {str(e)}'

    return render_template('contact_html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
