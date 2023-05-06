import logging, os, signal

from representations.Representation import Representation
from server.server import start_joern_server
class Main:
    
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        # Start joern server
        self.joern_server, self.joern_client = start_joern_server()
        for r in self.representations:
            logging.info(f'[{self.__class__.__name__.upper()}] Representation: {r.name} LOADED')
        
    def interpret(self):
        for r in self.representations:
            r.create(self.joern_client)
        # Shutdown server
        logging.info("Shutting down joern server")
        os.kill(self.joern_server.pid, signal.SIGSTOP)
        