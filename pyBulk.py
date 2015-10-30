#! /usr/local/bin/python
# pylint: disable=C0103, W0201
"""
Simple bulk mailer with a personal touch
"""
import json
import sys
import csv
from smtplib import SMTP as SMTP # USE SMPT and starttls() not STMP_SSL
from email.MIMEText import MIMEText

class Bulkmailer(object):
    """Bulkmailer class
    """
    def __init__(self, recipients):
        """
        Initialise Bulkmailer object providing the recipients file

        :param recipients: file containing recipients
        :type recipients: string

        """
        # init some vals
        self.recipients = recipients
        self.subject = "Hello dear friend"
        self.content = """
Bulkmailer ftw!Bulkmailer ftw!Bulkmailer ftw!
Bulkmailer ftw!Bulkmailer ftw!Bulkmailer ftw!
Bulkmailer ftw!Bulkmailer ftw!Bulkmailer ftw!
Bulkmailer ftw!Bulkmailer ftw!Bulkmailer ftw!

Bye,
your Bulkmailer
        """

        # get credentials
        self.readConfig('conf.json')

    def setSalutation(self, salutation):
        """ Set the default salutation

        :param salutation: default salutation used if none given
        :type salutation: string
        """

        self.salutation = salutation

    def readConfig(self, configFile):
        """ Read credentials from JSON
        """
        with open(configFile) as dataFile:
            data = json.load(dataFile)

        self.HOST = data["HOST"]
        self.PORT = data["PORT"]
        self.USER = str(data["USER"])   # has to be str not u''
        self.PASS = str(data["PASS"])   #   --""--
        self.FROM = data["FROM"]

    def connect(self):
        """
        Connect to SMTP server and store connection instance
        """
        #connect via SMTP and init starttls() by hand
        self.conn = SMTP(self.HOST, self.PORT)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.set_debuglevel(True)
        self.conn.login(self.USER, self.PASS)

    def sendMessage(self, recipient, content, msgType="plain"):
        """
        Send the message to a <recipient>
        """

        # connect
        self.connect()

        # assemble message

        msg = MIMEText(content, msgType)
        msg["Subject"] = self.subject
        msg["From"] = self.FROM

        # and deliver
        try:
            self.conn.sendmail(self.FROM, recipient, msg.as_string())
        except Exception, exc:
            sys.exit("mail failed; %s" % str(exc)) # give a error message
        finally:
            self.conn.close()

    def send(self):
        """
        The actual sending
        """

        with open(self.recipients) as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                to = row[0]
                # switch salutation
                if len(row[1]) == 0:
                    body = self.salutation + self.content
                else:
                    body = row[1] + self.content

                #send
                self.sendMessage(to, body)


if __name__ == '__main__':

    bm = Bulkmailer('contacts.csv')
    bm.setSalutation('Dear somebody')
    bm.send()





