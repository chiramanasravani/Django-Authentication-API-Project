from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),  # Use EMAIL_FROM from environment variables
            to=[data['to_email']]
        )
        
        # Send the email
        email.send()
