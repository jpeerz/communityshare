import logging
import os
import sys

from community_share import config, app

logger = logging.getLogger(__name__)

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('192.168.65.1', 5001))
sock.close()
if result == 0:
    logger.info('Connecting to remote PyCharm debugger')
    sys.path.append(os.path.join(os.path.dirname(__file__), 'pycharm-debug-py3k.egg'))

    import pydevd
    pydevd.settrace(
        '192.168.65.1',
        port=5001,
        stdoutToServer=True,
        stderrToServer=True,
    )
else:
    logger.info('Could not find a debugger to connect to')

logger.info('Loading settings from environment')
config.load_from_file()
logger.info('Making application')
app = app.make_app()
app.debug = True
logger.info('Debug={0}'.format(app.debug))
app.run(
    host='0.0.0.0',
    port=5000,
    debug=True,
    use_debugger=False,
    use_reloader=False
)
