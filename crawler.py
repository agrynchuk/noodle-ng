#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This it the Noodle NG file crawler main module.

It is executable and will read it's configuration file and then
begin working based on the information it finds there.

"""

import sys, os, socket as sk
import logging
import multiprocessing
from ConfigParser import SafeConfigParser
from datetime import datetime

from noodle.lib.utils import ipToInt, intToIp, hasService, getHostAndAddr, urlSplit, urlUnsplit
from noodle.lib.iptools import IpRange, IpRangeList

import transaction
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

import noodle.model as model
from noodle.model.share import Host

from crawlerclass import CrawlerSMB, CrawlerFTP
crawler_type = {"smb": CrawlerSMB, "ftp": CrawlerFTP}


fs = {'smb': False, 'ftp': False}
try:
    import crawler.fs_ftp as fs_ftp
    fs['ftp'] = True
except ImportError:
    pass
try:
    import crawler.fs_smb as fs_smb
    fs['smb'] = True
except ImportError:
    pass


# Some constant values
config_file = "crawler.ini"

# Parsing the overall configuration

config = SafeConfigParser({'here': sys.path[0]})
try:
    config.read(os.path.join(sys.path[0], config_file))
except:
    sys.exit("Could not read %s" % config_file)

debug = config.getboolean('main', 'debug')
if debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)
processes = config.getint('main', 'processes')

sqlalchemy_url = config.get('main', 'sqlalchemy.url')
sqlalchemy_echo = config.getboolean('main', 'sqlalchemy.echo')

def setup_worker():
    """Sets up a worker process"""
    logging.debug("Setting up worker %s" % multiprocessing.current_process().name)
    engine = sqlalchemy.create_engine(sqlalchemy_url, echo=sqlalchemy_echo)
    model.init_model(engine)
    #model.metadata.create_all(engine)
    return

def crawl(host, type, credentials=None, initializer=None):
    """Starts the crawling process for one host"""
    if initializer:
        initializer()
    
    hostname, ip = getHostAndAddr(host)
    
    logging.debug("Crawling host %s (%s)" % (hostname, ip))
    
    session = model.DBSession()
    
    for (username, password) in credentials:
        try:
            crawler = crawler_type[type](session, host, unicode(username), unicode(password))
            crawler.run()
        except Exception, e:
            logging.warn(e)
            raise
    
    return

def main():
    """Runs the crawler"""
    global debug
    logging.info("Supported filesystems: %s" % fs)
    
    locations = []
    
    if len(sys.argv) > 1:
        debug = True
        # Parsing location configuration from argv
        for i in range(1, len(sys.argv)):
            url = urlSplit(sys.argv[i])
            location = {'name': "arg%d" % i, 'type': url.scheme, 
                        'hosts': [url.hostname], 
                        'credentials': [(url.username, url.password)]}
            locations.append(location)
    else:
        # Parsing location configuration from config file
        for name in [section for section in config.sections() if section != 'main']:
            
            location = {}
            location['name'] = name
            location['type'] = config.get(name, 'type')
            if not fs[location['type']]:
                logging.info("Type %s is not supported, skipping section %s" % (location['type'], name))
                continue
            hosts = []
            for element in config.get(name, 'hosts').split(','):
                element = element.strip()
                if element.find('-') != -1:
                    # IP range
                    start, stop = element.split('-', 1)
                    hosts.append((start.strip(), stop.strip()))
                else:
                    # CIDR range or single IP
                    hosts.append(element)
            location['hosts'] = IpRangeList(*hosts)
            location['credentials'] = []
            if config.has_option(name, 'anonymous'):
                if config.getboolean(name, 'anonymous'):
                    location['credentials'].append((None, None))
            for cred in config.get(name, 'credentials').split(','):
                location['credentials'].append(tuple(cred.strip().split(':', 1)))
            locations.append(location)
    
    logging.debug(locations)
    
    for location in locations:
        logging.debug("Crawling location %s" % location['name'])
        if debug:
            for host in location['hosts']:
                crawl(host, location['type'], location['credentials'], setup_worker)
        else:
            # Get minimum that we don't have to have more workers than jobs
            pool = multiprocessing.Pool(min(processes,len(location['hosts'])*len(location['credentials'])), setup_worker)
            
            for host in location['hosts']:
                pool.apply_async(crawl, (host, location['type'], location['credentials']))
            
            pool.close()
            pool.join()
    
    return

if __name__ == '__main__':
    main()
