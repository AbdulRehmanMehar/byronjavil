
import sys
path = '/home/javlib/PAMS'
if path not in sys.path:
   sys.path.insert(0, path)

from run import server
app = server.app

