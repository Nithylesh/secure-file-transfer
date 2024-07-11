import tkinter as tk
from tkinter import ttk, filedialog
from ftplib import FTP, error_perm
import os

class FTPClientApp:
    def __init__(self, master):
        self.master = master
        master.title("FTP Client")

        # FTP Configuration
        self.server_label = ttk.Label(master, text="Server:")
        self.server_entry = ttk.Entry(master)

        # Port Configuration
        self.port_label = ttk.Label(master, text="Port:")
        self.port_entry = ttk.Entry(master)

        # Connect Button
        self.connect_button = ttk.Button(master, text="Connect", command=self.connect_to_ftp)

        # Back Button
        self.back_button = ttk.Button(master, text="Back", command=self.navigate_back, state=tk.DISABLED)

        # Directory Tree
        self.tree = ttk.Treeview(master, selectmode="browse")
        self.tree.heading('#0', text='Files and Folders')
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        # Download Button
        self.download_button = ttk.Button(master, text="Download", command=self.download_file, state=tk.DISABLED)

        # Upload Button
        self.upload_button = ttk.Button(master, text="Upload", command=self.upload_file, state=tk.DISABLED)

        # Layout
        self.server_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.server_entry.grid(row=0, column=1, padx=5, pady=5)

        self.port_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)

        self.connect_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_button.grid(row=3, column=0, pady=5, sticky=tk.W)
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.download_button.grid(row=5, column=0, pady=10)
        self.upload_button.grid(row=5, column=1, pady=10)

        # Variables to store selected file information
        self.selected_file = ""
        self.selected_file_path = ""

        # Variables to store current working directory and selected directory
        self.current_directory = "/"
        self.selected_directory = ""

    def connect_to_ftp(self):
        server = self.server_entry.get()
        port = int(self.port_entry.get())  # Convert port to integer

        try:
            self.ftp = FTP()
            self.ftp.connect(server, port)
            self.ftp.login()

            # Initialize the tree with the root directory content
            self.update_tree(self.current_directory)

            # Enable the upload button
            self.upload_button['state'] = tk.NORMAL
            self.download_button['state'] = tk.NORMAL

        except error_perm as e_perm:
            print(f"FTP Permission Error: {e_perm}")
        except Exception as e:
            print(f"Error connecting to FTP server: {e}")

    def update_tree(self, directory):
        try:
            self.tree.delete(*self.tree.get_children())  # Clear the treeview

            # Change the working directory on the FTP server
            self.ftp.cwd(directory)
            self.current_directory = directory

            # Get the list of files and folders in the current directory
            file_list = self.ftp.nlst()

            # Populate the treeview with files and folders
            for item in file_list:
                self.tree.insert('', 'end', text=item, values=(item,))

            # Enable/disable back button based on the root directory
            if self.current_directory == "/":
                self.back_button['state'] = tk.DISABLED
            else:
                self.back_button['state'] = tk.NORMAL

        except error_perm as e_perm:
            print(f"FTP Permission Error: {e_perm}")
        except Exception as e:
            print(f"Error updating tree: {e}")

    def on_tree_double_click(self, event):
        # Get the selected item
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "text")

        # Check if it's a directory
        if self.is_directory(item_text):
            # Concatenate the current directory and selected directory
            new_directory = os.path.join(self.current_directory, item_text)
            self.update_tree(new_directory)

    def navigate_back(self):
        # Get the parent directory
        parent_directory = os.path.dirname(self.current_directory)

        # Update the tree with the parent directory
        self.update_tree(parent_directory)

    def is_directory(self, item_text):
        # Check if the item is a directory
        try:
            # Use the SIZE command to determine if it's a directory (throws an error if it's a file)
            self.ftp.size(item_text)
            return False
        except:
            return True

    def download_file(self):
        try:
            # Get the selected item
            item = self.tree.selection()[0]
            self.selected_file = self.tree.item(item, "text")
            self.selected_file_path = self.ftp.pwd() + '/' + self.selected_file

            # Ask the user where to save the file (selecting a directory)
            download_directory = filedialog.askdirectory()
            
            # Print the download_directory for debugging
            print(f"Download Directory: {download_directory}")

            # Ensure download_directory is not empty before attempting to download
            if not download_directory:
                print("Download canceled.")
                return

            # Construct the local file path
            local_path = os.path.join(download_directory, self.selected_file)

            # Download the file from the FTP server using retrbinary
            with open(local_path, 'wb') as local_file:
                self.ftp.retrbinary(f"RETR {self.selected_file_path}", local_file.write)

            print(f"Downloaded file: {self.selected_file} to {local_path}")

        except Exception as e:
            print(f"Error downloading file: {e}")


    def upload_file(self):
        try:
            # Ask the user to select a file to upload
            local_path = filedialog.askopenfilename()

            # Check if the file exists
            if not os.path.isfile(local_path):
                print(f"Error: File does not exist at {local_path}")
                return

            # Upload the file to the FTP server
            with open(local_path, 'rb') as local_file:
                # Extract the filename from the path
                filename = os.path.basename(local_path)

                # Attempt to upload the file
                try:
                    self.ftp.storbinary(f"STOR {filename}", local_file)
                    print(f"Uploaded file: {local_path} to FTP server")
                except Exception as upload_error:
                    print(f"Error uploading file: {upload_error}")
                    return

        except Exception as e:
            print(f"Error selecting file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()
