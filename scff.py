import os
import re
import argparse
import extensions
from argparse import RawTextHelpFormatter

# ------------------Блок для регулярных выражений------------------

# Регулярное выражение для |Java, JavaScript, css, С, С++, C#, PHP, Go, Rust| вида /*  */
regular_expression = re.compile('/\*.*?\*/', re.DOTALL)
# Регулярное выражение для |Java, JavaScript, css, С, С++, C#, PHP, Go, Rust| вида //
regular_expression_one = re.compile('//.*?\n')

# -----------------------------------------------------------------


# Функция для поиска комментариев
def FindComments(path_to_file, output_dir_name, file_Extension, regular_expression, regular_expression_one):
    # Пишем все в папку, которая указана в опции -o
    output_name_file = output_dir_name+"/report_"+file_Extension[1:]
    with open(path_to_file, 'r') as f_read:  # Открываем файл в котором будем искать как f_read
        # Ищем комментарии и пишем их в result_comments
        # Ищем и записываем комментарии вида /* */ в переменную
        result_comments = regular_expression.findall(f_read.read())
        f_read.seek(0)  # возвращаемся обратно в начало файла
        # добавляем в конец найденные комментарии //
        result_comments.append(regular_expression_one.findall(f_read.read()))
        # фильтруем от пустых строк
        result_comments = list(filter(None, result_comments))
        if len(result_comments) != 0:  # проверяем, нашлись ли в файле комментарии
            with open(output_name_file, 'a') as f_write:
                f_write.write(f"{path_to_file}\n\n")
                for comment in result_comments:
                    # Записываем что нашли в файл с названием,
                    # которое передали в качестве аргумента -o
                    f_write.write(f"{comment}\n\n")


# Фукнция выводящая колличество файлов по расширению
def CountFile(count_file_in_path, all_extension, count_analyse):
    print(f"Всего файлов в проекте = {count_file_in_path}. Проанализированно было {count_analyse}.")


# ------Блок для аргументов коммандной строки-------
parser = argparse.ArgumentParser(
    description="Script for find comments in source code!\n\
This script can find comments in next languages:\n\
1. Java\n2. JavaScript\n3. Css\n4. C\n5. C++\n6. C#\n7. PHP\n8. Go\n9. Rust\n", formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', type=str, help="Input path to source code")
parser.add_argument('-o', type=str, help="Output name directory for reports")
args = parser.parse_args()
# --------------------------------------------------

# Из аргументов коммандной строки получаем путь до папки с исходниками
path_list = os.listdir(args.i)
# и записываем в переменную path_list все файлы, которые находятся в этой директории
os.mkdir(args.o+"/")  # Создаем папку в котором будут лежать отчеты о каждом ЯП
count_analyse = 0  # для записи количества проанализированных файлов

# В цикле ищем название файлов (file_Name) и их расширение (file_Extension), чтообы после искать в этих файлах комментарии
for file_in_dir in path_list:
    file_Name, file_Extension = os.path.splitext(file_in_dir)
    all_extension = []
    all_extension.append(file_Extension)
    for extension in extensions.list_ex:
        # ищем файлы с поддерживаемым расширением и чтобы они не были системными/скрытыми
        if file_Extension == extension and not (file_Name.startswith(".")):
            path_to_file = args.i+file_in_dir  # путь до файла
            # передаем все это для поиска комментариев
            FindComments(path_to_file, args.o,
                         file_Extension, regular_expression, regular_expression_one)
            count_analyse = count_analyse+1
        else:
            pass

# Для вывода результата о колличестве проанилизованных файлов
CountFile(len(path_list), all_extension, count_analyse)
