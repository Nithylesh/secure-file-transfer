
# Secure File Transfer Program
This project consists of a secure file transfer application that includes an FTP client for transferring files, an FTP server for sharing directories, and a file encryption/decryption utility. The application is built using Python's tkinter library for the graphical user interface and the cryptography library for secure file handling.

## Features
## FTP Client
Connect to FTP Server: Connect to an FTP server by providing the server address and port.
Navigate Directories: Browse and navigate through directories on the FTP server.
Download Files: Download files from the FTP server to your local machine.
Upload Files: Upload files from your local machine to the FTP server.
## FTP Server
Share Directory: Share a directory on your local machine via an FTP server.
Anonymous Access: Allow anonymous access with full permissions to the specified directory.
## File Encryption/Decryption
Encrypt Files: Encrypt files using a password-based key derivation function and AES encryption.
Decrypt Files: Decrypt previously encrypted files using the correct password.

## Usage
## FTP Client
Run the FTP client script.
Enter the FTP server address and port.
Click "Connect" to establish a connection.
Use the interface to navigate directories, download, and upload files.
## FTP Server
Run the FTP server script.
Select a directory to share.
The server will start and share the selected directory on port 21.
File Encryption/Decryption
Run the file encryptor script.
Select a file to encrypt or decrypt.
Enter the password for encryption or decryption.
Click "Encrypt" or "Decrypt" to process the file.
## Dependencies
tkinter: For the graphical user interface.
ftplib: For FTP client functionality.
pyftpdlib: For FTP server functionality.
cryptography: For file encryption and decryption.
