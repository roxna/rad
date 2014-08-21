from distutils.spawn import find_executable
import os
import re
import slate
import subprocess

__author__ = 'roxnairani'


def parse_data(pdf, password):

    # pdf = pdf.read()
    path = '/Users/tmp/' + pdf.name
    with open(path.encode('utf-8'), 'r') as f:
        print 'hi'
        subprocess.call(['qpdf, --password=' + password, ' --decrypt ', f.name, ' Unencrypted_'+f.name])
        print 'Unencrypted_'
