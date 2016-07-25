import requests
import json
import csv
from ConfigParser import SafeConfigParser
import sys, getopt

__author__ = "george@georgestarcher.com (George Starcher)"

def loadConfig(filename):

    global splunk_server
    global splunk_server_port
    global splunk_server_verify

    parser = SafeConfigParser()
    parser.read(filename)

    splunk_server = parser.get('splunk', 'splunk_server')
    splunk_server_port = parser.get('splunk', 'splunk_server_port')
    splunk_server_verify = parser.getboolean('splunk', 'splunk_server_verify')

def loadCSV(filename):

    # CSV should be in format: ip, description

    csvList = []
    with open(filename) as csvfile:
        badReader = csv.DictReader(csvfile)
        for row in badReader:
            csvList.append(row)

    csvfile.close()

    return csvList

def createKVStore(app,data):

    print json.dumps(data)
    splunk_url = ''.join(['https://',splunk_server,':',splunk_server_port,'/servicesNS/nobody/',app,'/storage/collections/config'])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(splunk_url,auth=(splunk_user,splunk_password),verify=splunk_server_verify,headers=headers,data=data)
    print r.text

def configureKVStore(app,collection,data):
    splunk_url = ''.join(['https://',splunk_server,':',splunk_server_port,'/servicesNS/nobody/',app,'/storage/collections/config/',collection])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(splunk_url,auth=(splunk_user,splunk_password),verify=splunk_server_verify,headers=headers,data=data)
    print r.text


if __name__ == "__main__":

    config_file = 'kvstore.conf'
    template = 'template.csv'
    app = ''
    collection = ''
    argv = sys.argv[1:]

    global splunk_user  
    global splunk_password 

    try:
        opts, args = getopt.getopt(argv,"a:c:",["app=","collection="])
        if args: 
            app = args[0]
            collection = args[1]
        else:
            print 'makekvstore.py <app> <collection>'
            sys.exit(2)
    except getopt.GetoptError as err:
        print 'makekvstore.py <app> <collection>'
        sys.exit(2)
    
    try:
        loadConfig(config_file)
    except Exception, e:
        print "Config File Error: %s" % e
        sys.exit(2)

    splunk_user = raw_input('enter Splunk user:')
    splunk_password = raw_input('enter Splunk password:')

    data = {'name':collection}
    print app, data
    createKVStore(app,data)

    data = {'field.'+k:v for k,v in loadCSV(template)[0].items()}
    print data
    configureKVStore(app,collection,data)

