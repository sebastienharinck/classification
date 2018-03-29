# Pull in hostname-based changes.
import socket
HOSTNAME = socket.gethostname().lower().split('.')[0].replace('-','')

try:
    exec("from classification.settings.host_{} import *".format(HOSTNAME))
except ImportError:
    pass

# Pull in the local changes.
try:
    from classification.settings.local import *
except ImportError:
    pass
