import urllib2
import ssl
import re
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# define mail sender function


def msender():
    msg = MIMEMultipart('alternative')
    msg['subject'] = 'New item'
    msg['From'] = ''
    msg['To'] = 'mail@gmail.com'
    html = """<html>
            </html>"""

    ht = MIMEText(html, 'html')
    msg.attach(ht)
    s = smtplib.SMTP('')
    s.sendmail('', ['mail@gmail.com'], msg.as_string())
    s.quit()


# define get request function

def get():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    html = urllib2.urlopen('https://www.avito.ru/', context=ctx)
    x = html.read()
    pat = re.compile('<div class=\"item item_table clearfix.*? id=\"(i\d+)\"')
    res = pat.findall(x)
    return res


# compare new list of ads IDs and old send alert if there is new ad

while True:
    result = get()
    f = open('html.txt', 'r+')
    if f.read() != str(result):
        msender()
        print 'New item!'
    f.close()
    f = open('html.txt', 'w')
    f.write(str(result))
    f.close()
    time.sleep(7)
    print 'cycle'
