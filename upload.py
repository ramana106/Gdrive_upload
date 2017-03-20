from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import multiprocessing as mp
import os
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Pattern',
    'mimeType': "application/vnd.google-apps.folder"})
file1.Upload()

folder_id = file1['id']

def upload_img(filename,img_list):
    temp_len= len(img_list)
    for image in img_list:
        print "Remaining",temp_len
        temp_len=temp_len-1
        fd=open(filename,'a')
        fil=os.path.basename(image)

        file2 = drive.CreateFile({'title':fil,
                                  'mimeType':'image/jpeg',
                                  'parents': [{"kind": "drive#fileLink", "id": folder_id}]
                                  })
        file2.SetContentFile(image)
        file2.Upload()
        permission = file2.InsertPermission({
                                'type': 'anyone',
                                'value': 'anyone',
                                'role': 'reader'})
        link=file2['alternateLink']
        link=link.split('?')[0]
        link=link.split('/')[-2]
        link='https://docs.google.com/uc?export=download&id='+link
        fd.write(link+'\n')
        fd.close()

upload_img('Files.txt',img_list)
