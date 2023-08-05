'''
base.py: credentials base class
'''

from appdirs import user_config_dir
import os
from   os import path

import handprint
from handprint.debug import log
from handprint.files import make_dir, copy_file

from .credentials_files import credentials_filename


# Main class.
# .............................................................................

class Credentials(object):
    creds_dir = user_config_dir('Handprint', 'CaltechLibrary')

    def __init__(self):
        self.credentials = None


    def creds(self):
        return self.credentials


    @classmethod
    def credentials_dir(self):
        return Credentials.creds_dir


    @classmethod
    def save_credentials(self, service, supplied_file):
        if not path.isdir(Credentials.creds_dir):
            if __debug__: log('creating credentials dir: {}.', Credentials.creds_dir)
            make_dir(Credentials.creds_dir)
        dest_file = path.join(Credentials.creds_dir, credentials_filename(service))
        copy_file(supplied_file, dest_file)
