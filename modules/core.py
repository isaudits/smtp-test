#!/usr/bin/env python3
'''
@author: Matthew C. Jones, CPA, CISA, OSCP
IS Audits & Consulting, LLC
TJS Deemer Dana LLP

Core functions

See README.md for licensing information and credits

'''
import sys
import os
import shutil
import subprocess
import logging
import time, datetime
import dns.resolver, dns.reversename

#------------------------------------------------------------------------------
# Global core functions
#------------------------------------------------------------------------------

# exit routine
def exit_program():
    print("\n\nQuitting...\n")
    sys.exit()
    
# cleanup old or stale files
def cleanup_routine(output_dir):
    '''Returns 'False' if the output directory is dirty and users select not to clean'''
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    try:
        if not os.listdir(output_dir) == []:
            response = input("\nOutput directory is not empty - delete existing contents? (enter no if you want to append data to existing output files)? [no] ")
            if "y" in response or "Y" in response:
                print("Deleting old output files...\n")
                shutil.rmtree(output_dir, True)
            else:             
                return False
    except:
        pass

def check_config(config_file):
    if os.path.exists(config_file):
        pass
    else:
        logging.warn("Specified config file not found. Copying example config file...")
        shutil.copyfile("config/default.example", config_file)

def execute(command, suppress_stdout=False):
    '''
    Execute a shell command and return output as a string
    
    By default, shell command output is also displayed in standard out, which can be suppressed
    with the boolean suppress_stdout
    '''
    
    output = ""
    try:
        process = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
        # Poll process for new output until finished
        while True:
            nextline = process.stdout.readline()
            output += nextline
            if nextline == '' and process.poll() != None:
                break
            if not suppress_stdout:
                sys.stdout.write(nextline)
            sys.stdout.flush()
        
        return output
    except KeyboardInterrupt:
        logging.warn("\n[!] Keyboard Interrupt - command '%s' killed..." % command)
        logging.warn("[!] Continuing script execution...")
        return ""

    except Exception as exception:
        logging.error("[!] Error running command '%s'" % command)
        logging.error("[!] Exception: %s" % exception)
        return ""

def write_outfile(path, filename, output_text, overwrite=False):
    if output_text:
        if not os.path.exists(path):
            os.makedirs(path)
            
        outfile = os.path.join(path, filename)
        
        if overwrite==True:
            file = open(outfile,'w+')
        else:
            file = open(outfile, 'a+')
            
        file.write(output_text)
        file.close

def getTimestamp(human=False):
    t = time.time()
    if human:
        timestamp = datetime.datetime.fromtimestamp(t).strftime("%d %b %Y %H:%M:%S")
    else:
        timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M%S')
    return timestamp

def nslookup_fwd(address):
    result=[]
    logging.info("checking dns on " + address)
    try:
        for rdata in dns.resolver.query(address):
            result.append(str(rdata))
        logging.info("Forward lookup results for " + address)
        logging.info(result)
        
    except dns.resolver.NXDOMAIN:
        logging.warn("Error resolving DNS - No such domain %s" % address)
    except dns.resolver.Timeout:
        logging.warn("Error resolving DNS - Timed out while resolving %s" % address)
    except dns.exception.DNSException:
        logging.warn("Error resolving DNS - Unhandled exception")
    
    return result

def nslookup_rev(ip):
    result=[]
    logging.info("checking reverse dns on " + ip)
    try:
        addr = dns.reversename.from_address(ip)
        for rdata in dns.resolver.query(addr, "PTR"):
            if str(rdata)[-1] == ".":
                result.append(str(rdata)[:-1])
            else:
                result.append(str(rdata))
        
        logging.info("Reverse lookup results for " + ip)
        logging.info(result)
        
    except dns.resolver.NXDOMAIN:
        logging.warn("Error resolving DNS - No reverse DNS record found for %s" % ip)
    except dns.resolver.Timeout:
        logging.warn("Error resolving DNS - Timed out while resolving %s" % ip)
    except dns.exception.DNSException:
        logging.warn("Error resolving DNS - Unhandled exception")
    return result

if __name__ == '__main__':
    #self test code goes here!!!
    pass