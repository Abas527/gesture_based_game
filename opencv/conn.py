import threading

class SharedData:
    def __init__(self):
        self.command = None
        self.lock = threading.Lock()
    
    def set_command(self, cmd):
        with self.lock:
            self.command = cmd
    
    def get_command(self):
        with self.lock:
            cmd = self.command
            self.command = None
            return cmd

shared = SharedData()