from flask import Flask, render_template, Response, request, redirect, url_for
import json
import smtplib
import ssl
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from email.utils import formataddr
import os
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

app = Flask(__name__)


with open("courses.json", 'rb') as fp:
    calendar = json.load(fp)


def validate_email(email: str) -> bool:
    """A function used to check the validity of an email address using regulat expressions"""
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True

    return False


def generate_mail(sender, subject,  receiver , list_str):
    body_path = "./mail.html"
    # Set my email address
    if (validate_email(sender) == False):
        logging.error("Sender email address invalid")
        raise TypeError("Sender email address invalid")

    # pesswod = 'wlav xjhy mkde drbr'

    # Create a multipart message and set headers

    message = MIMEMultipart()
    message["From"] = receiver
    message["To"] = formataddr(('Ibrahim Mhamed', sender))
    message["Subject"] = subject
    # Add body to email
    with open(body_path, 'r') as fp:
        msg_body=fp.read()

    msg_body=msg_body[:3522]+list_str+msg_body[3523:]
    message.attach(MIMEText(msg_body, "html"))

    # Open PDF file in binary mode
    return message


def send_mail(sender, pwd, receiver, courses_list):
    # recepient_data={recepient addr: [data to be implemented to email to make it look like its specifically made]}
    # Log in to server using secure context and send email
    context = ssl.create_default_context()

    li_list = '\n<ul >'

    for course_id in courses_list:
        for course_bundle in calendar['kurse']:
            for course in course_bundle['maeglichkeiten']:

                if (course['id'] == int(course_id)):
                    date = datetime.datetime(
                        calendar['jahr'], calendar['monat'], course_bundle['tag'])
                    li_list += '\n<li class="MsoNormal">' + \
                        str(course_bundle['tag'])+' ' + \
                        date.strftime('%a') + ' : '+course['name']+'</li>'
                    break
    li_list += '\n</ul>\n'

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Log into gmail server
        server.login(sender, pwd)
        if (validate_email(receiver) == False):
            logging.error("%s invalid" % receiver)

        msg = generate_mail(
            sender, 'PQZ Hessen Kursnewsletter September 20XX', receiver,li_list)
        server.sendmail(sender, receiver,
                        msg.as_string())
        logging.info('message sent to %s' % receiver)

    return True


@app.route("/", methods=['GET', 'POST'])
def main():
    if (request.method == 'POST'):
        print(json.loads(request.form.get('courses')))
        send_mail('barhooom360@gmail.com', os.getenv("PWD"),
                  request.form.get('email'), json.loads(request.form.get('courses')))

        return redirect(url_for('register'))
    else:
        return render_template('/main.html')


@app.route("/registered",)
def register():
    return render_template('/result.html')


@app.route("/data")
def data():

    return Response(response=json.dumps(calendar),
                    headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")
