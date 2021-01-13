#!/usr/bin/env python3
'''
@author: Matthew C. Jones, CPA, CISA, OSCP
IS Audits & Consulting, LLC
TJS Deemer Dana LLP

See README.md for licensing information and credits

'''

import smtplib
import argparse
import logging
import os
from configparser import ConfigParser
from email.mime.text import MIMEText

import modules.core

#Change the working directory to the main program directory just in case...
os.chdir(os.path.dirname(os.path.realpath(__file__)))

#------------------------------------------------------------------------------
# Configure Argparse to handle command line arguments
#------------------------------------------------------------------------------
desc = "Automated testing of SMTP servers for penetration testing"

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('server',
                    help='address of target organization email server',
                    action='store'
)
parser.add_argument('-f','--from_addr',
                    help='spoof email address of sender (sender@victim.com)',
                    action='store'
)
parser.add_argument('-t','--to_addr',
                    help='spoof email address of recipient (recipient@victim.com)',
                    action='store'
)
parser.add_argument('-c','--config',
                    help='Configuration file. (default: config/config.cfg)',
                    action='store', default='config/config.cfg'
)
parser.add_argument('--no-spoof',
                    help='Disable spoof email test',
                    dest='perform_spoof', action='store_false', default=True
)
parser.add_argument('--no-tests',
                    help='Disable direct tests against target SMTP server such as Nmap script scans',
                    dest='perform_tests', action='store_false', default=True
)
parser.add_argument('-d','--debug',
                    help='Print lots of debugging statements',
                    action="store_const",dest="loglevel",const=logging.DEBUG,
                    default=logging.WARNING
)
parser.add_argument('-v','--verbose',
                    help='Be verbose',
                    action="store_const",dest="loglevel",const=logging.INFO         
)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel)
logging.info('verbose mode enabled')
logging.debug('Debug mode enabled')

config_file = args.config
from_addr = args.from_addr
to_addr = args.to_addr
target_server = args.server
perform_spoof = args.perform_spoof
perform_tests = args.perform_tests

#------------------------------------------------------------------------------
# Get config file parameters
#------------------------------------------------------------------------------

modules.core.check_config(config_file)

config = ConfigParser()
config.read(config_file)
external_server=config.get("main", "smtp_server")
assessor=config.get("main", "assessor")
assessor_email=config.get("main", "assessor_email")
output_dir=os.path.abspath(config.get("main", "output_dir"))
email_subject=config.get("email", "subject")
email_body=config.get("email", "body")

email_subject=email_subject.replace("[ASSESSOR]", assessor)
email_subject=email_subject.replace("[ASSESSOR_EMAIL]", assessor_email)
email_body=email_body.replace("\\n", "\n")
email_body=email_body.replace("[ASSESSOR]", assessor)
email_body=email_body.replace("[ASSESSOR_EMAIL]", assessor_email)

#------------------------------------------------------------------------------
# Other initialization stuff
#------------------------------------------------------------------------------
modules.core.cleanup_routine(output_dir)

#------------------------------------------------------------------------------
# SMTP server tests
#------------------------------------------------------------------------------
if perform_tests:
    # Nmap SMTP server checks
    command =  "nmap -PN -sV -p 25 --script=smtp* "+ target_server
    output_file_path = os.path.join(output_dir, target_server + "_nmap.txt")
    result = modules.core.execute(command,False)
    modules.core.write_outfile(output_dir, target_server+"_nmap.txt",result)
    
    # MXToolbox smtp server test
    print("Running MXToolbox.com smtp server tests on "+target_server)
    url = "http://mxtoolbox.com/SuperTool.aspx?action=smtp:"+target_server+"&run=toolpage"
    output_file_path = os.path.join(output_dir, target_server + "_mxtoolbox.jpg")
    command = "cutycapt --out="+output_file_path+" --url="+ url
    modules.core.execute(command, True)

#------------------------------------------------------------------------------
# Spoof email test
#------------------------------------------------------------------------------
if perform_spoof:
    if from_addr and to_addr:
        
        print("Performing email spoof tests\n")
        
        #email message 1 - external smtp server
        print("Sending mail from external email server "+external_server)
        
        email_message = email_body+ "SMTP spoof test 1 \n"
        email_message += "External SMTP server "+external_server
        
        msg = MIMEText(email_message)
        msg['Subject'] = email_subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        
        try:
            s = smtplib.SMTP(external_server)
            s.sendmail(from_addr, to_addr, msg.as_string())
            s.quit
        except Exception as e:
            print("Error connecting / sending mail using external email server "+external_server)
            print(e)
        
        #email message 2 - target smtp server
        print("Sending mail from target email server "+target_server)
        
        email_message = email_body+ "SMTP spoof test 2 \n"
        email_message += "Target SMTP server - "+target_server
        
        msg = MIMEText(email_message)
        msg['Subject'] = email_subject
        msg['From'] = from_addr
        msg['To'] = to_addr
        
        try:
            s = smtplib.SMTP(target_server)
            s.sendmail(from_addr, to_addr, msg.as_string())
            s.quit
        except Exception as e:
            print("Error connecting / sending email using target email server "+target_server)
            print(e)
    else:
        print("Spoof addresses not specified; skipping spoof tests")

print("\nDone!")