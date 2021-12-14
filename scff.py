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
def FindComments(list_with_path_files, output_dir_name, regular_expression, regular_expression_one):
    for path_file in list_with_path_files:
        file_Name, file_Extension = os.path.splitext(path_file)
        # Пишем все в папку, которая указана в опции -o
        output_name_file = output_dir_name+"/report_"+file_Extension[1:]
        with open(path_file, 'r') as f_read:  # Открываем файл в котором будем искать комментарии
            # Ищем комментарии и пишем их в result_comments
            # Ищем и записываем комментарии вида /* */ в переменную
            result_comments = regular_expression.findall(f_read.read())
            f_read.seek(0)  # возвращаемся обратно в начало файла
            # добавляем в конец найденные комментарии //
            result_comments.append(
                regular_expression_one.findall(f_read.read()))
            # фильтруем от пустых строк
            result_comments = list(filter(None, result_comments))
            if len(result_comments) != 0:  # проверяем, нашлись ли в файле комментарии
                with open(output_name_file, 'a') as f_write:
                    f_write.write(f"{path_file}\n\n")
                    for comment in result_comments:
                        # Записываем что нашли в файл с названием,
                        # которое передали в качестве аргумента -o
                        f_write.write(f"{comment}\n\n")


# Фукнция выводящая колличество файлов по расширению
def CountFile(count_file_in_path, count_analyse):
    print(
        f"Всего файлов в проекте = {count_file_in_path}. Проанализированно было {count_analyse}.")


# Функция осуществляющая поиск всех файлов в директории и в поддиректориях
def FindFilesInPath(path):
    files_in_path = []  # заводим список куда будем писать все файлы
    all_files_count = 0  # переменная для хранения колличества всех файлов
    # цикл поиска файлов в директории и поддиректории
    for folder, subfolders, files in os.walk(path):
        for f in files:
            all_files_count = all_files_count+1
            file_Name, file_Extension = os.path.splitext(f)  # разбиваем файл на имя и расширение
            for extension in extensions.list_ex:  # цикл, который ищет все файлы с расширением в list_ex
                if file_Extension == extension and not (file_Name.startswith(".")):
                    # если файл не системный (не начинается с .) и подходит под расширение то добавляем его в спискок
                    files_in_path.append(folder+"/"+f) #Добабвляем в конец списка путь до файла
    return [files_in_path, all_files_count] #Возвращаем список с файлами и колличество всех файлов


# ------Блок для аргументов коммандной строки-------
parser = argparse.ArgumentParser(
    description="Script for find comments in source code!\n\
This script can find comments in next languages:\n\
1. Java\n2. JavaScript\n3. Css\n4. C\n5. C++\n6. C#\n7. PHP\n8. Go\n9. Rust\n", formatter_class=RawTextHelpFormatter)
parser.add_argument('-i', type=str, help="Input path to source code")
parser.add_argument('-o', type=str, help="Output name directory for reports")
args = parser.parse_args()
# --------------------------------------------------

os.mkdir(args.o)  # Создаем папку в котором будут лежать отчеты о каждом ЯП

# В ListWithPathFile лежат все найденные файлы с расширением из extensions.list_ex. В CountFileInPath колличество всех файлов в папке.
ListWithPathFiles, CountFilesInPath = FindFilesInPath(os.path.abspath(args.i))


FindComments(ListWithPathFiles, args.o,
             regular_expression, regular_expression_one) #Функция для поиска комментариев и записи их в файл
CountFile(CountFilesInPath, len(ListWithPathFiles)) #Функция для вывода различной информации
