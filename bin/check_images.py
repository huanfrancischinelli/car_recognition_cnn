from tkinter.filedialog import askdirectory
from tkinter import Tk
import os
import hashlib
import cv2
from pathlib import Path
from alive_progress import alive_bar

Tk().withdraw()
file_path = askdirectory(title="Select a folder")
unique_files = dict()
duplicated = 0
totalDir, totalFiles = 0, 0
for root, folders, files in os.walk(file_path):
    for directories in folders:
        totalDir += 1
    for Files in files:
        totalFiles += 1

with alive_bar(totalFiles, dual_line=True, title='Duplicated files') as bar:
    for root, folders, files in os.walk(file_path):
        for file in files:
            file_path2 = Path(os.path.join(root, file))
            Hash_file = hashlib.md5(open(file_path2, 'rb').read()).hexdigest()
            if Hash_file not in unique_files:
                unique_files[Hash_file] = file_path2
            else:
                duplicated += 1
                os.remove(file_path2)
                print(f"{file_path2} has been deleted")
            bar()
print(f'Duplicated files: {duplicated}')

#TODO: Unificar as duas verificações em uma passada

extensions=['jpg', 'png', 'jpeg', 'gif', 'bmp' ]
bad_images=[]
bad_ext=[]
invalid = 0
s_list= os.listdir(file_path)
with alive_bar(totalFiles-duplicated, dual_line=True, title='Invalid files') as bar:
    for klass in s_list:
        klass_path=os.path.join (file_path, klass)
        # print ('processing', klass)
        if os.path.isdir(klass_path):
            file_list=os.listdir(klass_path)
            for f in file_list:               
                f_path=os.path.join (klass_path,f)
                index=f.rfind('.')
                ext=f[index+1:].lower()
                if ext not in extensions:
                    print('file ', f_path, ' has an invalid extension ', ext)
                    bad_ext.append(f_path)
                if os.path.isfile(f_path):
                    try:
                        img=cv2.imread(f_path)
                        shape=img.shape
                    except:
                        invalid += 1
                        print('file ', f_path, ' is not a valid image file')
                        os.remove(f_path)
                        bad_images.append(f_path)
                else:
                    print('*** fatal error, you a sub directory ', f, ' in class directory ', klass)
                bar()
        else:
            print ('*** WARNING*** you have files in ', file_path, ' it should only contain sub directories')
print(f'Invalid files: {invalid}')