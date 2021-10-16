import os
import re
import argparse

def regularJavaComments(input_dir,analyse_file_name, output_name_file):
    with open(input_dir+analyse_file_name,'r') as f_read: #Открываем файл в котором будем искать как f_read
        pattern_java = re.compile(r'Какая-то регулярка') #Регулярное выражение для поиска комментариев для ЯП Java
        result_comments = pattern_java.findall(f_read.read()) #Ищем комментарии и пишем их в result_comments
        with open(output_name_file, 'a') as f_write:
            f_write.write(f"********{analyse_file_name}********\n{result_comments}") #Записываем что нашли в файл с названием,
                                                                                     #которое передали в качестве аргумента -o

#------Блок для аргументов коммандной строки-------
parser = argparse.ArgumentParser(description="Script for find comments in source code!")
parser.add_argument('-i', type=str, help="Input path to source code")
parser.add_argument('-o', type=str, help="Output name file for report")
args = parser.parse_args()
#--------------------------------------------------

path_list = os.listdir(args.i) #Из аргументов коммандной строки получаем путь до папки с исходниками
                               #и записываем в переменную path_list все файлы, которые находятся в этой директории

#В цикле ищем название файлов (file_Name) и их расширение (file_Extension), чтообы после искать в этих файлах комментарии
for file_in_dir in path_list:
    file_Name, file_Extension = os.path.splitext(file_in_dir)
    if file_Extension == ".java" and not (file_Name.startswith(".")): #ищем файлы с расширением .java и чтобы они не были системными/скрытыми
            regularJavaComments(args.i,file_in_dir,args.o) #передаем все это для поиска комментариев
    else:
        print("Пока не реализованно!")