import argparse
from datetime import datetime
import os
import sys
import shutil
import time
import hashlib


def sync_folders(source, replica, log_file, interval):
    try:
        # Create the source folder if it doesn't exist
        if not os.path.exists(source):
            os.makedirs(source)
            
        # Create the replica folder if it doesn't exist
        if not os.path.exists(replica):
            os.makedirs(replica)

        while True:
            try:
                # Synchronize files
                sync_files(source, replica, log_file)

                # Remove any extra files from the replica folder
                remove_extra_files(source, replica, log_file)

                # Wait for the next synchronization interval
                time.sleep(interval)  # Synchronize time in seconds
            except KeyboardInterrupt:
                print("Synchronization interrupted.")
                break
            except Exception as e:
                        error_message = f"An error occurred during synchronization: {str(e)}"
                        log(error_message, log_file)
                        print(error_message)
    except Exception as e:
        error_message = f"An error occurred while setting up synchronization: {str(e)}"
        log(error_message, log_file)
        print(error_message)

def sync_files(source, replica, log_file):
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_dir = os.path.join(replica, relative_path)
        os.makedirs(replica_dir, exist_ok=True)

        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_dir, file)

            if not os.path.exists(replica_file):
                # File doesn't exist in replica, so copy it
                shutil.copy2(source_file, replica_file)
                log_message = f"Copied: {source_file} to {replica_file}"
                log(log_message, log_file)
                print(log_message)

            else:
                if compare_files(source_file, replica_file):
                    # Files are identical, no need to update
                    continue

                # File has been modified in source, so update it in replica
                shutil.copy2(source_file, replica_file)
                log_message = f"Updated: {source_file} in {replica_file}"
                log(log_message, log_file)
                print(log_message)

def compare_files(file1, file2):
    # Compare files using checksums (SHA-256)
    hash1 = hashlib.sha256()
    hash2 = hashlib.sha256()
    BUFFER_SIZE = 4096
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        for chunk in iter(lambda: f1.read(BUFFER_SIZE), b''):
            hash1.update(chunk)

        for chunk in iter(lambda: f2.read(BUFFER_SIZE), b''):
            hash2.update(chunk)

    return hash1.hexdigest() == hash2.hexdigest()

def remove_extra_files(source, replica, log_file):
    for root, dirs, files in os.walk(replica):
        relative_path = os.path.relpath(root, replica)
        source_dir = os.path.join(source, relative_path)

        # Files
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_dir, file)

            if not os.path.exists(source_file):
                # File doesn't exist in source, so remove it from replica
                os.remove(replica_file)
                log_message = f"Removed: {replica_file}"
                log(log_message, log_file)
                print(log_message)
                
        # Directories        
        for dir in dirs:
                replica_dir = os.path.join(root, dir)
                source_dir = os.path.join(source, relative_path, dir)

                if not os.path.exists(source_dir):
                    # Directory doesn't exist in source, so remove it from replica
                    shutil.rmtree(replica_dir)
                    log_message = f"Removed directory: {replica_dir}"
                    log(log_message, log_file)
                    print(log_message)


def log(message, log_file):
    with open(log_file, "a") as f:
        timestamp = datetime.now()
        f.write(f"{timestamp}: {message}\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        sync_folders(args.source_folder, args.replica_folder, args.log_file, args.interval)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)
