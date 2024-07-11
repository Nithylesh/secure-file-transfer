from tkinter import filedialog
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def run_ftp_server():
    # Prompt the user to select a directory
    shared_directory = filedialog.askdirectory(title="Select Directory to Share")

    # Create an authorizer
    authorizer = DummyAuthorizer()

    # Allow anonymous access with all permissions to the specified directory
    authorizer.add_anonymous(shared_directory, perm="elradfmw")

    # Instantiate an FTP handler and associate the authorizer
    handler = FTPHandler
    handler.authorizer = authorizer

    # Start the FTP server
    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    run_ftp_server()

