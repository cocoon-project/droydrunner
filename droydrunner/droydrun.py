#!/usr/bin/env python
"""
droydrun.py  tools to test automating on android

        droydrun phone hub server start , to start a phone hub server


Usage:
    droydrun --version
    droydrun  phone hub server start [ --host <host> --port <port> --debug ]


Options:
    -H <host>, --host <host>           [default: 0.0.0.0]
    --port <port>                      [default: 5000]
    --debug

"""

import os
import sys
from copy import copy
from docopt import docopt

from droydrunner.__init__ import __version__ as version



#conditional imports
try:
    import uiautomator
except ImportError:
    uiautomator = None


try:
    import flask
except ImportError:
    flask = None


try:
    import requests
except ImportError:
    requests = None


if uiautomator and flask:
    from droydrunner.phone.hub.server.first import app as phone_hub_app
else:
    phone_hub_app = None



import logging
log=logging.getLogger(__name__)


defaults={
    '--host' : '0.0.0.0',
    '--port' : 5000

}



# init logging
logging.basicConfig(datefmt='%H:%M:%S',format='[%(levelname)s %(asctime)s] %(message)s', level=logging.DEBUG)




def main():
    """
        main function
    """
    opts = docopt(__doc__,version=version)

    # decode command line
    options= copy(defaults)

    options.update(opts)


    if options['phone']:
        if options['hub']:
            if options['server']:
                if options['start']:
                    log.info('starting a phone hub server')
                    # needs uiautomator + flask
                    if uiautomator and flask:
                        log.info('starting hub')
                        #
                        phone_hub_app.run( host=options['--host'] , port = int(options['--port']) , debug=options['--debug'])
                    else:
                        if not uiautomator:
                            log.error('need uiautomator module')
                        if not flask:
                            log.error('need flask module')
                        exit(1)

                    exit(0)

    else:
        raise NotImplementedError







# start script
if __name__=="__main__":
    main()
    sys.exit(0)










