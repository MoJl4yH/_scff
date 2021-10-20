import os
import re
import argparse
import extensions

# ------------------Блок для регулярных выражений------------------

# Регулярное выражение для *Java, JavaScript, css, С, С++, C#, PHP, Go, Rust вида /*  */
regular_expression = re.compile('/\*.*?\*/', re.DOTALL)
# regular_expression_one = re.compile('//.*?\n') #Регулярное выражение для *Java, JavaScript, css, С, С++, C#, PHP, Go, Rust вида //

# -----------------------------------------------------------------


def FindComments(path_to_file, output_dir_name, file_Extension, regular_expression):
    # Пишем все в папку, которая указана в опции -o
    output_name_file = output_dir_name+"/report_"+file_Extension[1:]
    with open(path_to_file, 'r') as f_read:  # Открываем файл в котором будем искать как f_read
        # Ищем комментарии и пишем их в result_comments
        result_comments = regular_expression.findall(f_read.read())
        with open(output_name_file, 'a') as f_write:
            f_write.write(f"********{path_to_file}********\n\n\n")
            for comment in result_comments:
                # Записываем что нашли в файл с названием,
                f_write.write(f"{str(comment)}\n\n\n")
                # которое передали в качестве аргумента -o


# ------Блок для аргументов коммандной строки-------
parser = argparse.ArgumentParser(
    description="Script for find comments in source code!")
parser.add_argument('-i', type=str, help="Input path to source code")
parser.add_argument('-o', type=str, help="Output name directory for reports")
args = parser.parse_args()
# --------------------------------------------------

# Из аргументов коммандной строки получаем путь до папки с исходниками
path_list = os.listdir(args.i)
# и записываем в переменную path_list все файлы, которые находятся в этой директории
os.mkdir(args.o+"/")  # Создаем папку в котором будут лежать отчеты о каждом ЯП

# В цикле ищем название файлов (file_Name) и их расширение (file_Extension), чтообы после искать в этих файлах комментарии
for file_in_dir in path_list:
    file_Name, file_Extension = os.path.splitext(file_in_dir)
    for extension in extensions.list_ex:
        # ищем файлы с поддерживаемым расширением и чтобы они не были системными/скрытыми
        if file_Extension == extension and not (file_Name.startswith(".")):
            path_to_file = args.i+file_in_dir  # путь до файла
            FindComments(path_to_file, args.o, file_Extension, regular_expression)  # передаем все это для поиска комментариев
        else:
            print("Пока не реализованно!")
