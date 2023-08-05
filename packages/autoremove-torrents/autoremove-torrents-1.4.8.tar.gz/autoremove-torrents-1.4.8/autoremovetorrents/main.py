#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import getopt
import traceback
import yaml
from . import logger
from .task import Task
from autoremovetorrents.version import __version__

def pre_processor(argv):
    # View Mode
    view_mode = False
    # The path of the configuration file
    conf_path = 'config.yml'
    # Task
    task = None

    # Set default logging path to current working directory
    logger.Logger.log_path = ''

    # Get arguments
    try:
        opts = getopt.getopt(argv, 'vc:t:l:', ['view', 'conf=', 'task=', 'log='])[0]
    except getopt.GetoptError:
        print('Invalid arguments.')
        sys.exit(255)
    for opt,arg in opts:
        if opt in ('-v', '--view'): # View mode (without deleting)
            view_mode = True
        elif opt in ('-c', '--conf'):
            conf_path = arg
        elif opt in ('-t', '--task'):
            task = arg
        elif opt in ('-l', '--log'):
            logger.Logger.log_path = arg

    # Logger
    lg = logger.Logger.register(__name__)

    # Run autoremove
    try:
        # Show version
        lg.info('Auto Remove Torrents %s' % __version__)
        # Load configurations
        lg.info('Loading configurations...')
        with open(conf_path, 'r') as stream:
            result = yaml.safe_load(stream)
        lg.info('Found %d task(s) in the file.' % len(result))

        # Run tasks
        if task == None: # Task name specified
            for task_name in result:
                try:
                    Task(task_name, result[task_name], not view_mode).execute()
                except Exception:
                    lg.error(traceback.format_exc().splitlines()[-1])
                    lg.error('Task %s fails. ' % task_name)
                    lg.debug('Exception Logged', exc_info=True)
        else:
            Task(task, result[task], not view_mode).execute()
    except Exception:
        lg.error(traceback.format_exc().splitlines()[-1])
        lg.debug('Exception Logged', exc_info=True)
        lg.critical('An error occured. If you think this is a bug or need help, you can submit an issue.')

def main():
    pre_processor(sys.argv[1:])

if __name__ == '__main__':
    main()