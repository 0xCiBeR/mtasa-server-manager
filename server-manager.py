#!/usr/bin/env python2.7
import xml.etree.ElementTree as ET
import sys, os.path
from pprint import pformat

#Edit anything here to your liking/needs
mtaconfig = 'mods/deathmatch/mtaserver.conf'
#Stop editing

#Check for the existence of the configuration file
if not os.path.isfile(mtaconfig):
    print('Could not find the MTA configuration file, expecting it at %s'%(mtaconfig))

#Load the configuration file and parse it
tree = ET.parse(mtaconfig)
root = tree.getroot()
settings = {'resources':{}, 'modules':[], 'client_files':{}}
for child in root:
    if child.tag == 'resource':
        settings['resources'][child.attrib['src']] = {'protected': child.attrib['protected'], 'startup': child.attrib['startup']}
    elif child.tag == 'client_file':
        settings['client_files'][child.attrib['name']] = {'verify': child.attrib['verify']}
    elif child.tag == 'module':
        settings['modules'].append(child.attrib['src'])
    else:
        settings[child.tag] = child.text

#Basic globals
scriptname = 'MTA:SA Server Manager CLI'
version = '0.1'
commands = {
    'help': {
        'help': 'Display help for this script.',
        'triggers': [
            '-h',
            '--help',
            '?',
            'help'
        ]
    },
    'configpath': {
        'help': 'Display the configuration path, read from server-manager.ini',
        'triggers': [
            '-cp',
            '--configpath',
            'configpath'
        ],
        'data': 'mtaconfig'
    },
    'config': {
        'help': 'Display the contents of your server\'s configuration.',
        'data': 'pformat(settings)',
        'triggers': [
            '-c',
            '--config',
            'config'
        ]
    }
}

#Printing stuff
print('%s ver %s\n---------'%(scriptname, version))
if len(sys.argv) > 1:
#help
    if sys.argv[1] in commands['help']['triggers']:
        if len(sys.argv) == 2:
            print(commands['help']['help'])
        elif len(sys.argv) == 3:
            if sys.argv[2] in commands:
                print(commands[sys.argv[2]]['help'])
            else:
                print('Command `%s` was not found, no help available. Try `help commands` for a listing of all commands.'%(sys.argv[2]))
        else:
            print(commands['help']['help'])
#config
    elif sys.argv[1] in commands['config']['triggers']:
        if len(sys.argv) == 2:
            print(eval(commands['config']['data']))
        elif len(sys.argv) == 5:
            if sys.argv[2] == 'update':
                if sys.argv[3] in settings:
                    child = tree.find(sys.argv[3])
                    print("Updating configuration file setting %s\nCurrent value: %s\nNew value: %s"%(sys.argv[3], child.text, sys.argv[4]))
                    child.text = sys.argv[4]
                    tree.write(mtaconfig)
        elif len(sys.argv) == 4:
            if sys.argv[2] == 'list':
                if sys.argv[3] in settings:
                    print(settings[sys.argv[2]])
#configpath
    elif sys.argv[1] in commands['configpath']['triggers']:
        if len(sys.argv) == 2:
            print(eval(commands['configpath']['data']))
else:
    print('No command provided, try passing one of the following for help:\n%s'%(', '.join(commands['help']['triggers'])))
