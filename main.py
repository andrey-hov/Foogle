import Foogle
import argparse

parser = argparse.ArgumentParser(description='Foogle')
parser.add_argument('phrase', type=str, help='Фраза для поиска в кавычках')
parser.add_argument('folder_path', type=str, help='Путь до папки')
parser.add_argument('type_file', type=str, default="0", help='Тип файла в формате .* или 0, если формат неважен')
args = parser.parse_args()

if __name__ == "__main__":
    print(Foogle.Finder(args.folder_path).find(args.phrase.replace("\"\"", "").replace('_', ' '), args.type_file))
