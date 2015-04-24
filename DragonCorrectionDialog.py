import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
import easygui
import sys
import signal
from threading import Timer

#     # this file may be executed externally to Dragon
#     BASE_PATH = "C:/NatLink/NatLink/MacroSystem"
#     if BASE_PATH not in sys.path:
#         sys.path.append(BASE_PATH)
        
LISTENING_PORT = 1338
DIALOG_TITLE = "Correction Dialog"
def communicate():
    return xmlrpclib.ServerProxy("http://127.0.0.1:" + str(LISTENING_PORT))

class DragonCorrectionDialog():
    def __init__(self, heard):
        self.completed = False
        self.setup_XMLRPC_server()
        self.correction = easygui.enterbox(heard, "Correct with...", default=heard)
        print "correction is", self.correction
        self.completed = True        
        
        # start server, tk main loop
        def start_server():
            while not self.server_quit:
                self.server.handle_request()  
        Timer(1, start_server).start()
        # backup plan in case for whatever reason Dragon doesn't shut it down:
        Timer(60, self.xmlrpc_kill).start()
    
    def setup_XMLRPC_server(self): 
        self.server_quit = 0
        self.server = SimpleXMLRPCServer(("127.0.0.1", LISTENING_PORT), allow_none=True)
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        self.server.register_function(self.xmlrpc_kill, "kill")
    
    def xmlrpc_kill(self):
        self.server_quit = 1
        os.kill(os.getpid(), signal.SIGTERM)
        
    def xmlrpc_get_message(self):
        print "get message called"
        if self.completed:
            Timer(1, self.xmlrpc_kill).start()
            return self.correction
        else:
            return None

if __name__ == "__main__":
    heard = sys.argv[1]
    print heard
    DragonCorrectionDialog(heard)