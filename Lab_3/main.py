import os
import time
from datetime import datetime
import sqlite3
import shutil

def connect_database():
    connection = sqlite3.connect("rep.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        commit_id INTEGER,
        filename TEXT NOT NULL,
        extension TEXT NOT NULL,
        created_at REAL NOT NULL,
        modified_at REAL NOT NULL,
        content BLOB,
        FOREIGN KEY (commit_id) REFERENCES commits(id)
    );
    """)
    connection.commit()
    return connection, cursor


class MiniGit:
    def __init__(self, folder_path,backup_folder):
        self.folder_path = folder_path
        self.snapshot_time = time.time()
        self.file_mod_times = {}
        self.current_commit_id = None
        self.original_commit_id = None
        self.update_file_mod_times()
        self.connection, self.cursor = connect_database()
        self.backup_folder = backup_folder

        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder) 

    def update_file_mod_times(self):
        self.file_mod_times = {
            file: os.path.getmtime(os.path.join(self.folder_path, file))
            for file in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, file))
        }

    def commit(self):
        """Save a snapshot of the current state of files to the database."""
        self.cursor.execute("INSERT INTO commits (timestamp) VALUES (?)", (self.snapshot_time,))
        commit_id = self.cursor.lastrowid
        self.current_commit_id = commit_id 

        for filename, mod_time in self.file_mod_times.items():
            file_path = os.path.join(self.folder_path, filename)
            with open(file_path, 'rb') as file:
                content = file.read()
            extension = os.path.splitext(filename)[1]
            created_at = os.path.getctime(file_path)
            self.cursor.execute("""
            INSERT INTO file_versions (commit_id, filename, extension, created_at, modified_at, content)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (commit_id, filename, extension, created_at, mod_time, content))

        self.connection.commit()
        self.snapshot_time = time.time() 
        self.update_file_mod_times()
        print("Snapshot committed at:", datetime.fromtimestamp(self.snapshot_time))

    def backup_files(self):
        """Backup the current files to the backup folder."""
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                backup_path = os.path.join(self.backup_folder, filename)
                shutil.copy(file_path, backup_path)

    def restore_backup(self):
        """Restore files from the backup folder."""
        for filename in os.listdir(self.backup_folder):
            backup_path = os.path.join(self.backup_folder, filename)
            if os.path.isfile(backup_path):
                restore_path = os.path.join(self.folder_path, filename)
                shutil.copy(backup_path, restore_path)

    def rollback(self, commit_id):
        if self.current_commit_id is not None and self.original_commit_id is None:
            print("Creating backup of the current state...")
            self.backup_files()
            self.original_commit_id = self.current_commit_id  # Salveaza comitul actual

        # Ia fisierele de la un anumit commit
        self.cursor.execute("SELECT filename, content FROM file_versions WHERE commit_id = ?", (commit_id,))
        files = self.cursor.fetchall()

        for filename, content in files:
            file_path = os.path.join(self.folder_path, filename)
            with open(file_path, 'wb') as file:
                file.write(content)

        print(f"Rolled back to commit {commit_id}")
        self.current_commit_id = commit_id  

    def restore_to_original(self):
        """Restore to the state of the original commit if a rollback was performed."""
        if self.original_commit_id is not None:
            print("Restoring to the original commit state...")
            self.restore_backup()  # face restore din backup
            self.current_commit_id = self.original_commit_id 
            self.original_commit_id = None 
            print(f"Restored to commit {self.current_commit_id}.")
        else:
            print("No previous state to restore to.")

    def info(self, filename):
        file_path = os.path.join(self.folder_path, filename)
        if not os.path.isfile(file_path):
            print("File not found.")
            return

        print(f"File Name: {filename}")
        print(f"Extension: {os.path.splitext(filename)[1]}")
        print("Created:", datetime.fromtimestamp(os.path.getctime(file_path)))
        print("Last Modified:", datetime.fromtimestamp(os.path.getmtime(file_path)))

    def status(self):
        current_files = {
            file: os.path.getmtime(os.path.join(self.folder_path, file))
            for file in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, file))
        }

        added_files = set(current_files.keys()) - set(self.file_mod_times.keys())
        deleted_files = set(self.file_mod_times.keys()) - set(current_files.keys())

        modified_files = []
        unmodified_files = []
        for file, mod_time in current_files.items():
            if file not in added_files:
                if mod_time > self.file_mod_times.get(file, 0):
                    modified_files.append(file)
                else:
                    unmodified_files.append(file)

        print("Status:")
        if added_files:
            print("Added Files:", added_files)
        if deleted_files:
            print("Deleted Files:", deleted_files)
        if modified_files:
            print("Modified Files:", modified_files)
        if unmodified_files:
            print("Unmodified Files:", unmodified_files)

    def run(self):
        """Run the interactive command loop."""
        while True:
            command = input("Enter command (commit, info <filename>, status, rollback <commit_id>, restore, exit): ").strip()
            if command == "exit":
                print("Exiting program.")
                break
            elif command == "commit":
                self.commit()
            elif command.startswith("info "):
                filename = command.split(" ", 1)[1]
                self.info(filename)
            elif command == "status":
                self.status()
            elif command.startswith("rollback "):
                try:
                    commit_id = int(command.split(" ", 1)[1])
                    self.rollback(commit_id)
                except ValueError:
                    print("Invalid commit ID. Please enter a numeric commit ID.")
            elif command == "restore":
                self.restore_to_original()
            else:
                print("Unknown command.")

folder_path = "D:/Universitate anul 2/Lab_3_OOP"
backup_folder="D:/Universitate anul 2/Lab_3_OOP/backup"
mini_git = MiniGit(folder_path,backup_folder)
mini_git.run()





