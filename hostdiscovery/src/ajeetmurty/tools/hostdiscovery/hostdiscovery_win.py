import logging.config
import os
import platform
import re
import subprocess

logging.config.fileConfig('logging.conf')
logr = logging.getLogger('pylog')
ping_command = 'ping {0} -n 1'
ping_subnet = '192.168.0.'
regex_pass = r'^(.*)(Sent = 1, Received = 1, Lost = 0){1}(.*)$'
list_pass = []
list_fail = []

def main():
    logr.info('start')
    try:
        print_sys_info()
        do_discovery()
    except Exception: 
        logr.exception('Exception')
    logr.info('stop')

def print_sys_info():
    logr.info('login|hostname|os|python : {0}|{1}|{2}|{3}.'.format(os.getlogin(), platform.node() , platform.system() + '-' + platform.release() , platform.python_version()))

def do_discovery():
    # temp_host_ip = '10.1.8.89'
    for i in range (1, 255):
        temp_ip = ping_subnet + str(i)
        do_ping(temp_ip)
    
    print_results()

def do_ping(host_ip):
    ping_command_formatted = ping_command.format(host_ip)
    p = subprocess.Popen(ping_command_formatted, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    ping_output = '--> ' 
    
    if stdout:
        ping_output += stdout.decode("utf-8")
    else:
        ping_output += ' no stdout'
    
    if stderr:
        ping_output += stderr.decode("utf-8")
    else:
        ping_output += ' no stderr'
    
    ping_output = re.sub('[\t\n\r]', ' ', ping_output)
    logr.debug('output for ' + host_ip + ' : ' + ping_output)
    logr.debug('ping command returned fail code: ' + str(p.returncode))
        
    match_pass = re.search(regex_pass, ping_output)
    if(match_pass):
        list_pass.append(host_ip)
        logr.debug('host responding to icmp: ' + host_ip)
    else:
        list_fail.append(host_ip)
        logr.debug('host NOT responding to icmp: ' + host_ip)


def print_results():
    print ('hosts responding to icmp: ')
    for host_ip in list_pass:
        print ('' + host_ip)
    
    print ('hosts NOT responding to icmp: ')
    for host_ip in list_fail:
        print ('' + host_ip)
    

if __name__ == '__main__':
    main()
