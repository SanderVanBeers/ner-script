import re
import nltk
from nltk import ngrams
from string import punctuation
import os
from time import time

def main():
    path_inputfile_source = '/home/sander/Desktop/sander.vanbeers/Continental-en-de/en_de-CONMT/btxt_2dir_de-XX-en-YY_News__27341-german-news-1996-2000-r2-detok.en'
    path_inputfile_target = '/home/sander/Desktop/sander.vanbeers/Continental-en-de/en_de-CONMT/btxt_2dir_de-XX-en-YY_News__27341-german-news-1996-2000-r2-detok.de'
    directory_input = os.path.dirname(path_inputfile_source)

    path_outputfile_source = '/home/sander/Desktop/sander.vanbeers/Continental-en-de/testing-ner.en'
    path_outputfile_target = '/home/sander/Desktop/sander.vanbeers/Continental-en-de/testing-ner.de'

    extension_source = '.en'
    extenstion_target = '.de'

    global placeholder
    placeholder = '###1000###'

    files = list_all_filenames(path_inputfile_source, path_inputfile_target)

    for filename in files:
        path_inputfile_source = os.path.join(directory_input, (filename + extension_source))
        path_inputfile_target = os.path.join(directory_input, (filename + extenstion_target))
        print('Processing %i of %i filepairs: %s' %((files.index(filename)+1), len(files), filename))
        
        with open(path_inputfile_source, mode='r') as inputfile_source, open(path_inputfile_target, mode='r') as inputfile_target, open(path_outputfile_source, mode ='a') as outputfile_source, open(path_outputfile_target, mode='a') as outputfile_target:

            source_text = inputfile_source.read().splitlines()
            target_text = inputfile_target.read().splitlines()

            for i in range(len(source_text)):
                printProgressBar (i, len(source_text), prefix = 'Progress current file:', suffix = 'Complete', decimals = 1, length = 100, fill = '█', printEnd = "\r")
                if source_text[i] != target_text[i]:
                    result = ngram_source_target(source_text[i], target_text[i], 20)
                    if result:
                        source = result[0]
                        target = result[1]

                        print(source, file=outputfile_source)
                        print(target, file=outputfile_target)

def preprocessngram(sent, n):

    bigrams = ngrams(sent.split(), n)
    return bigrams

def list_all_filenames(inputfile_source, inputfile_target): 
    split_path_source = os.path.splitext(inputfile_source)
    split_path_target = os.path.splitext(inputfile_target)
    extension_source = split_path_source[1]
    extension_target = split_path_target[1]
    filename = split_path_source[0]
    directory = os.path.dirname(inputfile_source)
    allfilenames = os.listdir(directory)
    singlefilenames = []
    for file_path in allfilenames:
        if file_path.endswith(extension_source):
            filename = os.path.splitext(file_path)
            singlefilenames.append(filename[0])
    return singlefilenames
    
def ngram_source_target(source, target, n):

    source_finished = ''
    target_finished = ''
    for c in range(n,0, -1):

        ngrams_source = list(preprocessngram(source, c))
        ngrams_target = list(preprocessngram(target, c))

        if common(ngrams_source, ngrams_target):
            for gram in common(ngrams_source, ngrams_target):
                if placeholder not in gram:
                    stringgram = convert_tuple(gram)
                    if stringgram:
                        pattern = re.compile('[^a-z]'+re.escape(stringgram)+'[^a-z]')
                        if not re.match(pattern, source) and not re.match(pattern, target):
                            source = source.replace(stringgram , placeholder)
                            target = target.replace(stringgram , placeholder)
                            print(source, stringgram, file = open('/home/sander/Desktop/sander.vanbeers/Continental-en-de/allreplacedstringssource.txt', mode = 'a'))#DEBUG
                            print(target, stringgram, file = open('/home/sander/Desktop/sander.vanbeers/Continental-en-de/allreplacedstringstarget.txt', mode = 'a'))
                            source_finished = source
                            target_finished = target

    if source_finished:
        result = (source_finished, target_finished)
        return result       

        
def common(list1, list2):
    return list(set(list1).intersection(list2))

def convert_tuple(gram):
    blacklist = ['in', 'IN', 'In', 'so', 'an']
    if gram[0] not in blacklist: #this would be an excellent place to insert a blacklist with other prepositions common between the two languages
        if len(gram) > 1:
            if re.match('\w', gram[0]) and re.match('\w', gram[-1]):
                if re.search("""[,.":;?!\]\)]""",gram[-1][-1]):
                    gramlist = list(gram)
                    gramlist[-1] = remove_punctuation(gramlist[-1])
                    if gramlist[-1]:
                        string = (' '.join(gramlist))
                        return string
                else:
                    string = (' '.join(gram))
                    return string
        if len(gram) == 1:
            if gram[0] != placeholder and re.match('\w\w\w+', gram[0]):
                string = (''.join(gram[0]))
                if not re.search('-', string[-1]):
                    if re.search("""[,.":;?!\]\)]""" , string[-1]):
                        string = remove_punctuation(string)
                        return string
                    else:
                        return string



def remove_punctuation(word):
    blacklist = ['Mrs.', 'Mr.', 'Ms.', 'Dr.', 'OK.']
    if word not in blacklist:
        if not re.search('\.', word[-1]):
            if not re.search("[(]", word):
                result = word.strip(r""",":;?!\]\)""")
                return result
            else:
                result = word.strip(r""".,;:""")
                return result
        else:
            result = word.strip(r""",":.;?!\]\)""")
            return result
    else:
        return word
        

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


main()
