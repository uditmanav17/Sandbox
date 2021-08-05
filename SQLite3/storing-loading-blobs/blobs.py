import sqlite3


class EmpData:
    def __init__(self) -> None:
        self.db_name = "employees.db"
        self._create_db()

    def _create_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS new_employee (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, photo BLOB NOT NULL, resume BLOB NOT NULL);
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def _convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, "rb") as file:
            blobData = file.read()
        return blobData

    def _writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, "wb") as file:
            file.write(data)
        print("Stored blob data into: ", filename)

    def insertBLOB(self, empId, name, photo, resumeFile):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            sqlite_insert_blob_query = """INSERT INTO new_employee (id, name, photo, resume) VALUES (?, ?, ?, ?)"""
            # fmt: off
            # sqlite_insert_blob_query = "INSERT INTO new_employee (name, photo, resume) VALUES (?, ?, ?)"
            # fmt: on

            empPhoto = self._convertToBinaryData(photo)
            resume = self._convertToBinaryData(resumeFile)
            # Convert data into tuple format
            data_tuple = (empId, name, empPhoto, resume)
            # data_tuple = (name, empPhoto, resume)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            conn.commit()
            print("Image and file inserted successfully as a BLOB into a table")

    def readBlobData(self, empId):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            print("Connected to SQLite")

            sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
            cursor.execute(sql_fetch_blob_query, (empId,))
            record = cursor.fetchall()
            for row in record:
                print(f"Id = {row[0]}\tName = {row[1]}")
                name = row[1]
                photo = row[2]
                resumeFile = row[3]

                print("Storing employee image and resume on disk")
                photoPath = f"./write_data/{name}.png"
                resumePath = f"./write_data/{name}_resume.pdf"
                self._writeTofile(photo, photoPath)
                self._writeTofile(resumeFile, resumePath)
            cursor.close()


blob_testing = EmpData()
blob_testing.insertBLOB(1, "john_doe", "./read_data/pic.png", "./read_data/ex1.pdf")
blob_testing.readBlobData(1)

