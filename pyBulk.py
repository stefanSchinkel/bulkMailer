#! /usr/local/bin/python
"""
Simple Script to bulk mail multiple recipients
"""
import json
import sys
# USE SMPT and starttls()
from smtplib import SMTP as SMTP
from email.MIMEText import MIMEText


def readConfig(configFile='conf.json'):
    """ Read credentials from JSON
    """
    with open(configFile) as dataFile:
        AUTH = json.load(dataFile)

    return  AUTH

def connect():
    """
    Connect to SMTP server and return connection instance

    :returns: SMTP instancce
    :rtype: smtplib.SMTP_SSL
    """

    # read config
    AUTH = readConfig()

    #connect via SMTP and init starttls() by hand
    conn = SMTP(AUTH["HOST"])
    conn.ehlo()
    conn.starttls()
    conn.set_debuglevel(True)
    # convert to python sring, unicode fails
    conn.login(str(AUTH["USER"]), str(AUTH["PASS"]))

    return conn

def sendMessage(sender, recipient, subject, content, msgType="plain"):
    """
    Send an email from <sender> to <recipient> with the subject <subject>
    and the content <content>. The message type can be set.

    :arg sender: from address
    :arg recipient: to address
    :arg subject: message subject
    :arg content: message body

    :type sender: string
    :type recipient: string
    :type subject: string
    :type content: string

    :returns: success
    :rtype: bool
    """

    # connect to server
    conn = connect()


    # assemble message
    msg = MIMEText(content, msgType)
    msg['Subject'] =  subject
    msg['From']  = sender

    # and deliver
    try:
        conn.sendmail(sender, recipient, msg.as_string())
    except Exception, exc:
         sys.exit( "mail failed; %s" % str(exc) ) # give a error message
    finally:
        conn.close()

def main():
    """ The thing as such
    """


    # typical values for text_subtype are plain, html, xml
    sender = "Foo@bar.baz"
    recipient = 'foo@baz.bar'
    subject = "Sent from Python"
    content = "Test message"
    msgType = "plain"

    sendMessage(sender, recipient, subject, content, msgType)


if __name__ == '__main__':
    main()