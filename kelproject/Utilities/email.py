__name__ = 'EmailOperations Class'
__doc__ = 'Email Operations'
__version__ = 'v1.0'
# Standart Libray

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from postmarker.core import PostmarkClient
import smtplib

class EmailOperations(object):

    postmark = PostmarkClient(server_token='45e220fe-d5b0-490d-98f2-7c50fff32f07')

    def sendEmail(self, sender, to, subject, body):
        if 'datapare.com' in to:
            self.sendEmailOutside(sender, to, subject, body)
            #self.sendEmailInside(sender, to, subject, body)
        else:
            self.sendEmailOutside(sender, to, subject, body)

    def sendEmailInside(self,sender, to, subject, body):

        fromaddr = "info@datapare.com"
        toaddr = "serkan@datapare.com"
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject

        body = body
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "##16L8582##")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    def sendEmailOutside(self,sender, to, subject, body):

        self.postmark.emails.send(
            From=sender,
            To=to,
            Subject=subject,
            HtmlBody=body
        )