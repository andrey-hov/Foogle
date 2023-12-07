import Foogle
import argparse

parser = argparse.ArgumentParser(description='Foogle')
parser.add_argument('phrase', type=str, help='Фраза для поиска')
parser.add_argument('files_path', type=str, help='Пути до файлов через пробел')
args = parser.parse_args()

if __name__ == "__main__":
    print(Foogle.Finder(args.files_path.split('_')).phrase_query(args.phrase.replace('_', ' ')))
