# Folder Synchronization Application

The Folder Synchronization Application is a Python program that synchronizes two folders, maintaining an identical copy of the source folder in the replica folder. It provides one-way synchronization where the content of the replica folder is modified to exactly match the content of the source folder.

## Features

- Periodic synchronization of folders at a specified interval.
- File creation, copying, and removal operations are logged to a file and displayed in the console output.
- Command-line arguments for folder paths, synchronization interval, and log file path.
- One-way synchronization from source to replica.

## Requirements

- Python 3.x

## Usage

1. Clone the repository or download the source code.

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application with the following command-line arguments:
```
python3 folder_sync.py source_folder replica_folder log_file interval
```
- `source_folder`: Path to the source folder to be synchronized.
- `replica_folder`: Path to the replica folder to store the synchronized content.
- `log_file`: Path to the log file to record the synchronization operations. Creates it if it does not exist.
- `interval`: Synchronization interval in seconds.

4. The application will start synchronizing the folders based on the provided interval. Any file creations, modifications, or deletions in the source folder will be reflected in the replica folder.

5. The synchronization operations will be logged to the specified log file and displayed in the console output.

## Example

pytho3n folder_sync.py /path/to/source /path/to/replica sync.log 60


This command will synchronize the `/path/to/source` folder with the `/path/to/replica` folder every 60 seconds. The synchronization operations will be logged to `sync.log`.

## Improvements and Customization

The application can be further enhanced and customized based on specific requirements. Some potential improvements include:

- Resumable synchronization to resume from the last synchronized state.
- User feedback and progress indicators during synchronization.
- Configuration file support for specifying settings.
- Conflict resolution mechanisms for handling modifications in both source and replica folders.

## License

This application is licensed under the [MIT License](LICENSE).
