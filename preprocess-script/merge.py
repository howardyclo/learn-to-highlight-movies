# Merge all POS txt to a single POS txt, same as NEG.
import glob
import random
import numpy as np
from collections import defaultdict

def writeLines(path, lines):
    fout = open(path, 'w')
    for line in lines:
        fout.write('%s\n' % line)
    print 'Merged {} number of lines. Save to {}.'.format(len(lines), path)
    fout.close()

def buildVocab(lines):
    words = []
    for line in lines:
        words += line.split()

    vocab = defaultdict(lambda: 0)
    for word in words:
        vocab[word] += 1
    return vocab

def normalizeLowFreqWords(vocab, lines, min_count):
    normalized_lines = []
    for line in lines:
        words = line.split()
        normalized_words = map(lambda word: word if vocab[word] >= min_count else 'UNK', words)
        normalized_lines.append(' '.join(normalized_words))
    return normalized_lines

if __name__ == '__main__':

    # Parameters
    IN_FOLDER_PATH = '../processed-data/'
    OUT_FOLDER_PATH = '../training-data/'

    fin_POS_paths = glob.glob(IN_FOLDER_PATH + '*_POS.txt')
    fin_NEG_paths = glob.glob(IN_FOLDER_PATH + '*_NEG.txt')

    fout_train_POS_path = OUT_FOLDER_PATH + 'train_POS.txt'
    fout_train_NEG_path = OUT_FOLDER_PATH + 'train_NEG.txt'
    fout_test_POS_path = OUT_FOLDER_PATH + 'test_POS.txt'
    fout_test_NEG_path = OUT_FOLDER_PATH + 'test_NEG.txt'

    POS_lines = []
    NEG_lines = []

    # Merge all lines from different sources of POS, NEG txt
    for path in fin_POS_paths:
        print 'Merging {} ...'.format(path)
        with open(path) as f:
            for line in f:
                POS_lines.append(line)
        f.close()

    for path in fin_NEG_paths:
        print 'Merging {} ...'.format(path)
        with open(path) as f:
            for line in f:
                NEG_lines.append(line)
        f.close()

    vocab = buildVocab(POS_lines + NEG_lines)
    POS_lines = normalizeLowFreqWords(vocab, POS_lines, 10)
    NEG_lines = normalizeLowFreqWords(vocab, NEG_lines, 10)

    # Shuffle data and split data to training and testing set
    data_size = len(POS_lines)
    train_size = int(data_size * 0.8)
    test_size = data_size - train_size

    random.shuffle(POS_lines)
    train_POS_lines = POS_lines[:train_size]
    test_POS_lines = POS_lines[train_size:train_size + test_size]

    random.shuffle(NEG_lines)
    train_NEG_lines = NEG_lines[:train_size]
    test_NEG_lines = NEG_lines[train_size:train_size + test_size]

    # Save training and testing data to file
    writeLines(OUT_FOLDER_PATH + 'all_POS.txt', POS_lines)
    writeLines(OUT_FOLDER_PATH + 'all_NEG.txt', NEG_lines)
    writeLines(fout_train_POS_path, train_POS_lines)
    writeLines(fout_test_POS_path, test_POS_lines)
    writeLines(fout_train_NEG_path, train_NEG_lines)
    writeLines(fout_test_NEG_path, test_NEG_lines)
