import os
import time
import csv
import logging
import socket
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, csv_file, log_file):
        self.csv_file = csv_file
        self.log_file = log_file

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            change_time = time.ctime()
            change_type = self.get_change_type(event.event_type)

            # Get file information before the change
            size_before = self.get_file_size(file_path)
            permissions_before = self.get_file_permissions(file_path)

            # Perform the file change action here...
            # Replace this with your custom code to handle the file change event
            print(f"File modified: {file_path}")

            # Get file information after the change
            size_after = self.get_file_size(file_path)
            permissions_after = self.get_file_permissions(file_path)

            # Get the IP address and source port associated with the file change
            ip_address, source_port = self.get_ip_address_and_source_port()

            # Log the IP address, source port, and file change information to the log file
            logging.info(f"IP: {ip_address}, Source Port: {source_port}, File: {file_path}, Time: {change_time}, Type: {change_type}")

            # Append the file change information to the CSV file
            with open(self.csv_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [file_path, change_time, change_type, size_before, size_after, permissions_before, permissions_after,
                     ip_address, source_port])

    @staticmethod
    def get_change_type(event_type):
        if event_type == 'created':
            return 'Created'
        elif event_type == 'modified':
            return 'Modified'
        elif event_type == 'deleted':
            return 'Deleted'
        else:
            return 'Unknown'

    @staticmethod
    def get_file_size(file_path):
        return os.path.getsize(file_path)

    @staticmethod
    def get_file_permissions(file_path):
        permissions = os.stat(file_path).st_mode & 0o777
        return oct(permissions)

    @staticmethod
    def get_ip_address_and_source_port():
        # Get the IP address and source port of the remote connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        ip_address = sock.getsockname()[0]
        source_port = sock.getsockname()[1]
        sock.close()

        return ip_address, source_port


def monitor_files(directory, csv_file, log_file):
    event_handler = FileChangeHandler(csv_file, log_file)
    observer = PollingObserver()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            observer.schedule(event_handler, file_path, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    current_directory = os.getcwd()
    monitored_directory = current_directory
    changewatch_directory = os.path.join(current_directory, 'changewatch')

    # Create the changewatch directory
    os.makedirs(changewatch_directory, exist_ok=True)

    # Create the .htaccess file to restrict directory access
    htaccess_file_path = os.path.join(changewatch_directory, '.htaccess')
    with open(htaccess_file_path, 'w') as htaccess_file:
        htaccess_file.write("Options -Indexes\n")

    csv_file_path = os.path.join(changewatch_directory, 'changes.csv')
    log_file_path = os.path.join(changewatch_directory, 'file_changes.log')

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Path', 'Change Time', 'Change Type', 'Size Before', 'Size After', 'Permissions Before',
                         'Permissions After', 'IP Address', 'Source Port'])

    # Configure logging to write IP addresses, source ports, and file change information to the log file
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s')

    monitor_files(monitored_directory, csv_file_path, log_file_path)
