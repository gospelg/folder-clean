import os
from pathlib import Path
from SMWinservice import SMWinservice
from time import sleep

class import_service(SMWinservice):
    _svc_name_ = "File_Cleaner"
    _svc_display_name_ = "Old File Cleaner"
    _svc_description_ = "Deletes files from download folder that are older than 30 days."

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def delete_files(self, path, age):
        """ 
        age is number of days after which a file should be deleted. It is multiplied by 86400
        which is the number of seconds in a day. time.time() gets the current time in seconds
        since the turn of the epoch. You then subtract the age * 86400 to get what wouldve been 
        the amount of seconds since epoch 30 days ago, or whatever was defined in age.
        Reason it's done this way, is because when you get the file attributes from windows it
        gives them to you in seconds since epoch, so instead of converting everything I just left
        it to work this way. Also its nice doing simple math with floats instead of date time formats
        """
        cutoff = time.time() - (age * 86400)
        alldownloads = []
        #iter through all downloads and subfolders, add files with complete paths to list
        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                alldownloads.append(os.path.join(dirpath, file))
        for download in alldownloads:
            file_attr = os.stat(download)
            if file_attr.st_ctime < cutoff:
                os.remove(download)
                
    def main(self):
        #find the users downloads directory
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        delete_files(location, 30)
        sleep(3600)        

if __name__ == '__main__':
import_service.parse_command_line()
