from flask import render_template
from data_access.models.email_model import Email
from data_access.repos.base_repo import BaseRepo
from datetime import datetime
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailRepo(BaseRepo):
    def upload_email(self, email_info):
        doc_ref = self.db.collection(u'emails').document()
        email_model = Email.from_dict(email_info)
        doc_ref.set(email_model.to_dict())
    
    def get_all_emails(self):
        email_list = []
        for email in self.db.collection(u'emails').stream():
            create_date = datetime.utcfromtimestamp(int(email.create_time.seconds)).strftime('%Y-%m-%d %H:%M:%S')
            last_update = datetime.utcfromtimestamp(int(email.update_time.seconds)).strftime('%Y-%m-%d %H:%M:%S')
            email_to_return = Email.from_dict(email.to_dict())
            email_to_return.create_date = create_date
            email_to_return.last_update = last_update
            email_list.append(email_to_return)
        return email_list

    def send_email(self, form):
        email_subject = form['subject']
        email_content = form['content']
        self.send_all_notification(email_subject, email_content, None, None, None)

    def send_all_notification(self, subject, content, subscription_type, img, body):
        secrets_file = None
        subscription_is_howto = subscription_type == 'howto'
        subscription_is_post = subscription_type == 'post'
        subscription_is_not_listed = subscription_type == None
        default_subject = 'New Post From RVAWOL!:'
        default_content = "Rvawol has a new post!"
        subject = default_subject if not subject else subject
        content = default_content if not content else content
        link_post = subject.replace(' ', '-')
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets:
                secrets_file = json.load(secrets)

            if secrets_file:
                API_KEY = secrets_file["SEND_GRID_API"]
                sg = SendGridAPIClient(API_KEY)
                for recipient_email in self.db.collection(u'emails').stream():
                    receiving_email = Email.from_dict(recipient_email.to_dict())
                    if receiving_email.howto_subscribed and subscription_is_howto or \
                    receiving_email.post_subscribed and subscription_is_post \
                    or subscription_is_not_listed:
                        if subscription_is_not_listed:
                            message = Mail(
                                from_email='rvawol.emailer@gmail.com',
                                to_emails=f'{receiving_email.email_address}',
                                subject=subject,
                                html_content=content
                            )
                        else:
                            message = Mail(
                                from_email='rvawol.emailer@gmail.com',
                                to_emails=f'{receiving_email.email_address}',
                                subject=subject,
                                html_content=render_template('email.html', email_info={
                                    'img1': img,
                                    'link': f'https://rvawol.com/posts/{link_post}',
                                    'body': body
                                }) 
                            )

                        response = sg.send(message)

        except Exception as e:
            print(e.message)
