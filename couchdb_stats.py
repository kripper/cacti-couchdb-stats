#-*- coding: utf-8 -*-
from __future__ import print_function
from requests.auth import HTTPBasicAuth
import requests
from optparse import OptionParser

def subiterator(substats, master=False):
    if type(substats) is dict:
        for subkey, subvalue in substats.iteritems():
            subiterator(subvalue, (master + "_" + subkey) if master else subkey)
    else:
        try:
            print ("%s:%s " % (
                master, int(substats)),
                end=''
                )
        except:
            print

def iterator(options, stats):
    """ Iterate over the server response """
    if options.group == "couchdb":
        subiterator(stats)

    elif options.group:
        subiterator(stats[options.group])

    else:
        for master, subdict in stats.iteritems():
            subiterator(subdict, master)


def connToDb(options):
    """ Craft the db connection url based on options"""
    if options.username and options.password:
        r = requests.get(''.join(('http://', options.hostname,
                        ':', options.port, '/_node/_local/_stats/couchdb')),
                        auth=HTTPBasicAuth(options.username, options.password))
    else:
        r = requests.get(''.join(('http://', options.hostname,
                        ':', options.port, '/_node/_local/_stats/couchdb')))
    # check if the response was valid
    if r.status_code != 200:
        raise Exception("connection failed. response: %s" % r.text)

    return r

if __name__ == '__main__':

    parser = OptionParser(usage="usage: %prog [-h] [-H HOSTNAME] [-P PORT]")
    parser.add_option("-H", "--hostname",
                        dest="hostname",
                        action="store",
                        default="127.0.0.1",
                        help="default to localhost")
    parser.add_option("-P", "--port",
                        dest="port",
                        action="store",
                        default="5984",
                        help="default port [5984]")
    parser.add_option("-u", "--username",
                        dest="username",
                        action="store",
                        default=False,
                        help="Username [optional]")
    parser.add_option("-p", "--password",
                        dest="password",
                        action="store",
                        default=False,
                        help="Password [optional]")
    parser.add_option("-g", "--group",
                        dest="group",
                        action="store",
                        default=False,
                        help="group [couchd/httpd]")

    (options, args) = parser.parse_args()

    r = connToDb(options)

    iterator(options, r.json())
