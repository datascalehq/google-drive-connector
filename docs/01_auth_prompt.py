"""
Note: To use this script you have to copy client_sercrets.json in this folder first
"""
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from typing import List


class GoogleDriveConnector:
    def __init__(self):
        self.gauth = None
        self.drive = None

    def allow_access(self):
        """Authenticate with OAuth to google drive"""
        if self.gauth is None:
            self.gauth = GoogleAuth()
            self.gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(self.gauth)

    def list_files_and_folders(self) -> List[object]:
        """Get files and folders in root path
        Return
            - items (List[object]): items can be both file and folder
        """
        # TODO: should we implement list from speicific path
        if self.drive is None:
            self.allow_access()
        items = self.drive.ListFile(
            {"q": "'root' in parents and trashed=false"}
        ).GetList()
        return items

    def read_file_content(self, file_id: str):
        """TODO: docstring

        Args:
            file_id (str): _description_

        Returns:
            _type_: _description_
        """
        # TODO: handle file that cant read
        if self.drive is None:
            self.allow_access()
        file = self.drive.CreateFile(metadata={"id": file_id})
        file.GetContentFile(filename=file_id)
        file_bytes = file.content
        file_string = file_bytes.read().decode("utf-8")
        return file_string

    def list_files_in_folder(self, folder_id: str):
        print(f"{folder_id=}")
        query = "'{}' in parents and trashed = false".format(folder_id)
        file_list = self.drive.ListFile({"q": query}).GetList()
        files = []
        for file in file_list:
            if file["mimeType"] == "application/vnd.google-apps.folder":
                # If the file is a folder, recursively call the function to list files in it
                x = self.list_files_in_folder(file["id"])
                files.extend(x)
            else:
                # If the file is not a folder, add its ID to the list
                files.append(file)
        return files


if __name__ == "__main__":
    gdrive_connector = GoogleDriveConnector()
    gdrive_connector.allow_access()

    files = gdrive_connector.list_files_in_folder(folder_id="root")
    for file in files:
        print("title: %s, id: %s" % (file["title"], file["id"]))
