# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 19:05:16 2020

@author:
    Chaix-Eichel Naomi
    Giraud Alexandra
    
We wanted to make a program which sorts photoshoot files (from an unsorted folder with a lot of photos) according to the day of shoot and type of file and 
puts automatically the files in sorted and named folders.
sorts by year, then by date for more clarity 

Then there is a second sort and the RAW files (DNG format) are put separately in a RAW folder so all the files can be easily be found and transferred to lightroom later

"""
import os 
import os.path
from PIL import Image 
#from PIL.ExifTags import TAGS
import time 
import shutil
from PIL import UnidentifiedImageError

# you can change here the path to the folder that you cant to sort
path_to_sorting_folder = r"C:\Users\sacho\Pictures\test"

def get_date(photoPath):
    '''
    returns the 
    the date the picture was taken or recorded. 
    The format is "YYYY_MM_DD" (string)
    if this data is unknown, exif file is filled with spaces
    '''
    try:
        with Image.open(photoPath) as im:
            exif_data = im._getexif()
            try: 
                completeDate = exif_data[36867]#YYYY:MM:DD HH:MM:SS, is a string 
                date = completeDate[:10]
                fileDate = date.replace(":","_")
                im.close()
                return(fileDate)
            except:
                return(-1) #if there is no date available in the ecif file 
    except FileNotFoundError:
        return(0) #if wrong path
    except UnidentifiedImageError:
        return(-2)


def create_folders(pathh,name):
    '''
    path is the path where you want to create the folder
    name is the wanted name for this folder , is a string 
    returns the path to the new folder
    
    if the folder does no exist, it creates a folder by the name give in the path given
    In our case, the path is the path of the unsorted batch of photos 
    and we want to create folders with the name of the date 
    
    '''
    newPath = os.path.join(pathh,name) # otherwise put back the path to sort folder
    if not os.path.isdir(os.path.abspath(newPath)):
        os.mkdir(os.path.abspath(newPath))
    #print(os.path.isdir(newPath))
    return newPath


def isRaw(filePath):
    '''
    the entry must be 
    filePath is the path to the file that is being processed
    with the extension
    '''
    #file = rfilePath
    try :
        if ("DNG" in filePath) or ("dng" in filePath ):
            return True
        else:
            return False        
    except SyntaxError:
        return(0)


def processFolder(in_folder_path):
    '''
    entry : initial folder file with all the images 
    must be with the form r"directory"
    
    '''
    try:
        images = [f for f in os.listdir(in_folder_path) if os.path.isfile(os.path.join(in_folder_path, f))]
        for image in images:
            imagePath = r"{}\{}".format(in_folder_path, image)
            # print(imagePath)
            # for now videos/otherf files are counted as images
            date = get_date(imagePath)
            if date != 0 and date != -1 and date !=-2: # now we have only images because they have exif data
                # path to the new folder names after the date of the current image
                year = str(date[:4])
                # print(year)
                path = create_folders(in_folder_path,year)
                # print(os.path.isdir(os.path.abspath(path)))
                # pathNewFolder_year = create_folder(in_folder_path,year)
                pathNewFolder_date = create_folders(path,date)
                # print(pathNewFolder_date)
                # print(os.path.isdir(os.path.abspath(os.path.join(in_folder_path,year,date))))
                # we move all the files in the year folder
                shutil.move(imagePath, pathNewFolder_date)
                
            if isRaw(imagePath):
                pathRawfolder = create_folders(in_folder_path,'RAW')
                shutil.move(imagePath,pathRawfolder)
    except FileNotFoundError:
        return 0
    
def size(path = 'C:\\Users\ADMIN\Documents\programs\Python'):
   
    # initialize the size
    total_size = 0
    
    # use the walk() method to navigate through directory tree
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            
            # use join to concatenate all the components of path
            f = os.path.join(dirpath, i)
            
            # use getsize to generate size in bytes and add it to the total size
            total_size += os.path.getsize(f)
    if total_size < 1000:
        return '%i' % total_size + 'B'
    elif 1000 <= total_size < 1000000:
        return '%.1f' % float(total_size/1000) + 'KB'
    elif 1000000 <= total_size < 1000000000:
        return '%.1f' % float(total_size/1000000) + 'MB'
    elif 1000000000 <= total_size < 1000000000000:
        return '%.1f' % float(total_size/1000000000) + 'GB'
    elif 1000000000000 <= total_size:
        return '%.1f' % float(total_size/1000000000000) + 'TB'


    
def main():
    # gets the size of the initial folder
    sizes = size(path_to_sorting_folder)
    print('the size of the folder to sort is')
    print(sizes)
    tic = time.perf_counter()
    processFolder(path_to_sorting_folder)
    toc = time.perf_counter()
    print(f"Time used: {toc - tic:0.4f} seconds")
    
if __name__ == "__main__":
    main()
    