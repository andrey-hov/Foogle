import Foogle
import argparse

parser = argparse.ArgumentParser(description='Foogle')
parser.add_argument('phrase', type=str, help='Фраза для поиска')
parser.add_argument('files_path', type=str, help='Пути до файлов через пробел')
parser.add_argument('type_file', type=str, help='Тип файла в формате .* или 0, если формат неважен')
parser.add_argument('exact', type=str, help='Точный запрос - 1, неточный - 0')
args = parser.parse_args()

if __name__ == "__main__":
    print(Foogle.Finder(args.files_path.split('_')).phrase_query(args.phrase.replace('_', ' '), args.type_file, args.exact))
