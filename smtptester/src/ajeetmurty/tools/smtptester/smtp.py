import logging.config
import os
import platform
import datetime
import smtplib
from email.mime.text import MIMEText

logging.config.fileConfig('logging.conf')
logr = logging.getLogger('pylog')
smtp_host_ip = '127.0.0.1'
smtp_host_port = 25
smtp_host_timeout = 5
smtp_from_address = 'from@smtp.org'
smtp_to_addresses = ['to01@smtp.org', 'to02@smtp.org']

def main():
    logr.info('start')
    try:
        print_sys_info()
        do_smtp()
    except Exception: 
        logr.exception('Exception')
    logr.info('stop')

def print_sys_info():
    logr.info('login|hostname|os|python : {0}|{1}|{2}|{3}.'.format(os.getlogin(), platform.node() , platform.system() + '-' + platform.release() , platform.python_version()))

def do_smtp():
    logr.info('SMTP host|port|timeout|from|to : {0}|{1}|{2}|{3}|{4}.'.format(smtp_host_ip, smtp_host_port, smtp_host_timeout, smtp_from_address, smtp_to_addresses))
    message_raw = 'Test Email formulated at: {0}.'.format(datetime.datetime.now())
    message_raw += '\nEmail Sent To - smtp server|port|timeout|from|to: {0}|{1}|{2}|{3}|{4}.'.format(smtp_host_ip, smtp_host_port, smtp_host_timeout, smtp_from_address, smtp_to_addresses)
    message_raw += '\nCheck Performed By - login|hostname|os|python : {0}|{1}|{2}|{3}.'.format(os.getlogin(), platform.node() , platform.system() + '-' + platform.release() , platform.python_version())
    message_formatted = MIMEText(message_raw)
    message_formatted['Subject'] = 'SMTP Test Script'
    message_formatted['From'] = smtp_from_address
    message_formatted['To'] = ", ".join(smtp_to_addresses)
    logr.info('smtp formatted message: \n{0}'.format(message_formatted))
    smtp = smtplib.SMTP(smtp_host_ip, port=smtp_host_port, timeout=smtp_host_timeout)
    smtp.set_debuglevel(True)
    smtp.sendmail(smtp_from_address, smtp_to_addresses, message_formatted.as_string())
    smtp.quit()
    logr.info('email sent')
    
if __name__ == '__main__':
    main()