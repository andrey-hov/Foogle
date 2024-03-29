# input = [file1, file2, ...]
# res = {filename: [word1, word2]}

import re
import math


class BuildIndex:
    """
        Принимает список файлов и строит индекс
        input = [file1, file2, ...]
    """

    def __init__(self, files):
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.filenames = files
        self.file_to_terms = self.process_files()
        self.regdex = self.regIndex()
        self.totalIndex = self.execute()
        self.vectors = self.vectorize()
        self.mags = self.magnitudes(self.filenames)
        self.populateScores()

    def process_files(self):
        """
            Принимает файл и возвращает словарь слов с позициями в файле
            input = filenames
            output = {file1: [word1, word2], file2: [word1, word2], ...}
        """
        file_to_terms = {}
        with open('stopwords-ru.txt') as file:
            stopwords = file.read()
            file.close
        for file in self.filenames:
            pattern = re.compile('[\W_]+')
            file_to_terms[file] = open(file, 'r', encoding='utf-8').read().lower()
            file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
            re.sub(r'[\W_]+','', file_to_terms[file])
            file_to_terms[file] = file_to_terms[file].split()
            file_to_terms[file] = [w for w in file_to_terms[file] if w not in stopwords]
        return file_to_terms

    @staticmethod
    def index_file(termlist):
        """
            Принимает список слов и возвращает словарь слов с позициями в файле
            input = [word1, word2, ...]
            output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
        """
        index_file = {}
        for index, word in enumerate(termlist):
            if word in index_file.keys():
                index_file[word].append(index)
            else:
                index_file[word] = [index]
        return index_file


    def make_indices(self, termlists):
        """
            Возвращает словарь файлов со словарем слов и их позициями в файле
            input = {filename: [word1, word2, ...], ...}
            output = {filename: {word: [pos1, pos2, ...]}, ...}
        """
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_file(termlists[filename])
        return total


    def fullIndex(self):
        """
            Возвращает индекс (словарь слов с файлами и позициями)
            input = {filename: {word: [pos1, pos2, ...], ... }}
            output = {word: {filename: [pos1, pos2]}, ...}, ...}
        """
        total_index = {}
        indie_indices = self.regdex
        for filename in indie_indices.keys():
            self.tf[filename] = {}
            for word in indie_indices[filename].keys():
                self.tf[filename][word] = len(indie_indices[filename][word])
                if word in self.df.keys():
                    self.df[word] += 1
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {filename: indie_indices[filename][word]}
        return total_index

    def vectorize(self):
        vectors = {}
        for filename in self.filenames:
            vectors[filename] = [len(self.regdex[filename][word]) for word in self.regdex[filename].keys()]
        return vectors


    def document_frequency(self, term):
        """
            Возвращает частоту слова в документах
            input = word
            output = number
        """
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys()) 
        else:
            return 0

    def collection_size(self):
        """
            Возвращает количество документов
            output = number
        """
        return len(self.filenames)

    def magnitudes(self, documents):
        mags = {}
        for document in documents:
            mags[document] = pow(sum(map(lambda x: x**2, self.vectors[document])),.5)
        return mags

    def term_frequency(self, term, document):
        return self.tf[document][term]/self.mags[document] if term in self.tf[document].keys() else 0

    def populateScores(self):
        for filename in self.filenames:
            for term in self.getUniques():
                self.tf[filename][term] = self.term_frequency(term, filename)
                if term in self.df.keys():
                    self.idf[term] = self.idf_func(self.collection_size(), self.df[term]) 
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    def idf_func(self, N, N_t):
        if N_t != 0:
            return math.log(N/N_t)
        else:
            return 0

    def generateScore(self, term, document):
        return self.tf[document][term] * self.idf[term]

    def execute(self):
        index = self.fullIndex()
        with open('index.txt', 'w+', encoding='utf-8') as file:
            for word in index:
                file.write(word + '\n')
                for filename in index[word]:
                    file.write(filename + ' ')
                    for i in index[word][filename]:
                        file.write(str(i) + ' ')
                    file.write('\n')
                file.write("\n")
        return index

    def regIndex(self):
        return self.make_indices(self.file_to_terms)

    def getUniques(self):
        return self.totalIndex.keys()