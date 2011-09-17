'''
Created on 05.09.2011

@author: moschlar
'''

import posixpath
from datetime import datetime

from noodle.lib.utils import ipToInt, intToIp, hasService, getHostAndAddr, urlSplit, urlUnsplit

import transaction
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

import noodle.model as model
from noodle.model.share import Host, Folder, File

class Crawler():
    
    def __init__(self, session, hostname, ip):
        self.session = session
        self.hostname = hostname
        self.ip = ip
    
    def path_split(self, path):
        return posixpath.split(path)
    
    def path_join(self,a,*p):
        return posixpath.join(a,*p)
    
    def path_splitext(self,file):
        return posixpath.splitext(file)
    
    def dblist(self, database_dir):
        folders = {}
        files = {}
        for child in database_dir.children:
            if isinstance(child, Folder):
                folders[child.name] = child
            elif isinstance(child, File):
                if child.extension:
                    files[child.name+"."+child.extension] = child
                else:
                    files[child.name] = child
            else
                continue
            
        return (folders, files)
    
    def run(self):
        host = self.session.query(Host).filter(Host.ip == ipToInt(self.ip)).first() or Host(self.ip, unicode(self.hostname))
        self.session.merge(host)
        host.name = unicode(self.hostname)
        host.last_crawled = datetime.now()
        database_dir = host
        host_dir = "/"
        self.walker(database_dir, host_dir)
    
    def walker(self, database_dir, host_dir):
        
        host_list = self.onewalk(host_dir)
        database_list = self.dblist(database_dir)
        
        for file in host_list[1]:
            stat = self.stat(self.path_join(host_dir,file))
            if database_list[file]:
                # File already crawled
                if database_list[file].size != stat[6] or database_list[file].date != datetime.fromtimestamp(stat[8]):
                    # Stats have changed
                    database_list[file].size = stat[6]
                    database_list[file].date = datetime.fromtimestamp(stat[8])
                    database_list[file].last_update = datetime.now()
            else:
                # New file
                myFile = File()
                name, extension = self.path_splitext(file)
                myFile.name
                myFile.extension
                myFile.size = stat[6]
                myFile.date = datetime.fromtimestamp(stat[8])
                myFile.last_update = datetime.now()
                database_dir.children.append(file)
        # TODO
    