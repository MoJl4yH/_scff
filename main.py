import os
import regex

def regularJavaComments(name_file):
    f = open(name_file, 'r')
    print(f,'\n',f.read())

path_list = os.listdir('df-2.0.2-source/')
os.chdir('df-2.0.2-source/')
for i in path_list:
    file_Name, file_Extension = os.path.splitext(i)
    if file_Extension == ".java" and not(file_Name.startswith(".")):
            regularJavaComments(i)
    else:
        print("Error!")
