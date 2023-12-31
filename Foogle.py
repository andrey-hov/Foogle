import Index
import re
import os

class Finder:
    def __init__(self, folder):
        a = os.listdir(path=folder)
        a.remove('stopwords-ru.txt')
        if 'index.txt' in a:
            a.remove('index.txt')
        os.chdir(folder)
        self.filenames = a
        self.index = Index.BuildIndex(self.filenames)
        self.invertedIndex = self.index.totalIndex
        self.regularIndex = self.index.regdex
        os.chdir(r"../")


    def one_word_query(self, word):
        pattern = re.compile('[\W_]+')
        word = pattern.sub(' ', word)
        if word in self.invertedIndex.keys():
            return self.rankResults([filename for filename in self.invertedIndex[word].keys()], word)
        else:
            return []

    def free_text_query(self, string):
        pattern = re.compile('[\W_]+')
        string = pattern.sub(' ', string)
        result = []
        for word in string.split():
            result += self.one_word_query(word)
        return self.rankResults(list(set(result)), string)

    def phrase_query(self, string, type_file):
        """
        Принимает фразу и выдает список файлов, в которых она находится
        [file1, file2, ...]
        """
        #pattern = re.compile('[\W_]+')
        #string = pattern.sub(' ', string)
        listOfLists, result = [],[]
        for word in string.split():
            listOfLists.append(self.one_word_query(word))
        setted = set(listOfLists[0]).intersection(*listOfLists)
        for filename in setted:
            temp = []
            if type_file != '0' and not (type_file in filename):
                continue
            for word in string.split():
                temp.append(self.invertedIndex[word][filename][:])
            for i in range(len(temp)):
                for ind in range(len(temp[i])):
                    temp[i][ind] -= i
            if set(temp[0]).intersection(*temp):
                result.append(filename)
        a = self.rankResults(result, string)
        if len(a) == 0:
            return ['Не найдено']
        return a

    def make_vectors(self, documents):
        vecs = {}
        for doc in documents:
            docVec = [0]*len(self.index.getUniques())
            for ind, term in enumerate(self.index.getUniques()):
                docVec[ind] = self.index.generateScore(term, doc)
            vecs[doc] = docVec
        return vecs


    def query_vec(self, query):
        pattern = re.compile('[\W_]+')
        query = pattern.sub(' ',query)
        queryls = query.split()
        queryVec = [0]*len(queryls)
        index = 0
        for ind, word in enumerate(queryls):
            queryVec[index] = self.queryFreq(word, query)
            index += 1
        queryidf = [self.index.idf[word] for word in self.index.getUniques()]
        magnitude = pow(sum(map(lambda x: x**2, queryVec)),.5)
        freq = self.termfreq(self.index.getUniques(), query)
        tf = [x/magnitude for x in freq]
        final = [tf[i]*queryidf[i] for i in range(len(self.index.getUniques()))]
        return final

    def find(self, phrases, type):
        result = []
        delete = []
        for phrase in phrases.split('|'):
            if phrase[0] == '-':
                a = self.phrase_query(phrase[1:], type)
                if (a is not None):
                    delete = [*delete, *a]
            else:
                a = self.phrase_query(phrase, type)
                if (a is not None):
                    result = [*result, *a]
        new = set()
        for i in range(len(result)):
            if result[i] != 'Не найдено':
                new.add(result[i])
        for d in delete:
            if d in new:
                new.remove(d)
        if len(new) == 0:
            new = 'Не найдено'
        return new

    def queryFreq(self, term, query):
        count = 0
        for word in query.split():
            if word == term:
                count += 1
        return count

    def termfreq(self, terms, query):
        temp = [0]*len(terms)
        for i,term in enumerate(terms):
            temp[i] = self.queryFreq(term, query)
        return temp

    def dotProduct(self, doc1, doc2):
        if len(doc1) != len(doc2):
            return 0
        return sum([x*y for x,y in zip(doc1, doc2)])

    def rankResults(self, resultDocs, query):
        vectors = self.make_vectors(resultDocs)
        queryVec = self.query_vec(query)
        results = [[self.dotProduct(vectors[result], queryVec), result] for result in resultDocs]
        results.sort(key=lambda x: x[0])
        results = [x[1] for x in results]
        return results

    def check_text(input_text, check_list):
        input_text = input_text.decode('utf-8')
        result = []
        
        for word in input_text.split(" "):
            wrd = {}
            for i in word:
                for n in check_list:
                    n = n.decode('utf-8')
                    for l in n:
                        if (i == l):
                            try: wrd[n].append(0)
                            except: wrd[n] = [0,]
            for key in wrd.keys():
                if (len(wrd[key]) > len(word)-2) and \
                    (len(wrd[key]) <= len(word)):
                    result.append([word, key])
                        
        return result