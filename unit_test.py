import unittest
import os
from tempfile import TemporaryDirectory
from folder_sync import sync_files, log
import shutil


class SyncFilesTestCase(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.source_dir = TemporaryDirectory()
        self.replica_dir = TemporaryDirectory()

        # Create sample files in the source directory
        self.create_sample_files()
        self.create_sample_folder()

    def tearDown(self):
        # Clean up temporary directories
        self.source_dir.cleanup()
        self.replica_dir.cleanup()

    def create_sample_files(self):
        # Create sample files in the source directory
        self.file1 = os.path.join(self.source_dir.name, 'file1.txt')
        
        self.file2 = os.path.join(self.source_dir.name, 'file2.txt')
        self.file3 = os.path.join(self.source_dir.name, 'file3.txt')  # Non-existing file

        with open(self.file1, 'w') as f:
            f.write('This is file 1.')

        with open(self.file2, 'w') as f:
            f.write('This is file 2.')

    def test_sync_files(self):
        # Synchronize files
        sync_files(self.source_dir.name, self.replica_dir.name, 'test.log')

        # Assert that files are copied to the replica directory
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir.name, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir.name, 'file2.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.replica_dir.name, 'file3.txt')))  # Non-existing file

        # Modify file1 in the source directory
        with open(self.file1, 'a') as f:
            f.write(' Additional content.')

        # Synchronize files again
        sync_files(self.source_dir.name, self.replica_dir.name, 'test.log')

        # Assert that file1 is updated in the replica directory
        with open(os.path.join(self.replica_dir.name, 'file1.txt'), 'r') as f:
            content = f.read()
            self.assertEqual(content, 'This is file 1. Additional content.')

    def test_sync_files_missing_source_file(self):
        # Remove file1 from the source directory
        os.remove(self.file1)

        # Synchronize files
        sync_files(self.source_dir.name, self.replica_dir.name, 'test.log')

        # Assert that file1 is removed from the replica directory
        self.assertFalse(os.path.exists(os.path.join(self.replica_dir.name, 'file1.txt')))

    def create_sample_folder(self):
        # Create a sample folder in the source directory
        self.folder1 = os.path.join(self.source_dir.name, 'folder1')
        os.makedirs(self.folder1)

    def test_sync_files_folder_deletion(self):
        # Remove folder1 from the source directory
        shutil.rmtree(self.folder1)

        # Synchronize files
        sync_files(self.source_dir.name, self.replica_dir.name, 'test.log')

        # Assert that folder1 is removed from the replica directory
        self.assertFalse(os.path.exists(os.path.join(self.replica_dir.name, 'folder1')))


if __name__ == '__main__':
    unittest.main()