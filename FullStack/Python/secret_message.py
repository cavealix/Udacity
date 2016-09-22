import os

def rename_files():
    #1 get file names from folder
    file_list = os.listdir(r"/Users/Alix/Desktop/prank")
    print (file_list)

    saved_path = os.getcwd() #save the current working directory location

    #2 for each file, rename file
    os.chdir(r"/Users/Alix/Desktop/prank") #go to proper directory
    for file_name in file_list:
        os.rename(file_name, file_name.translate("1234567890"))

    print (file_list)
    os.chdir(saved_path) #go back to original directory

rename_files()
