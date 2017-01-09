#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import json
import argparse
import numpy as np

from collections import defaultdict
from gensim.models import Doc2Vec
from keras.models import load_model

""" 載入前面訓練好的 models """
d2v = Doc2Vec.load('model/doc2vec_model.d2v')

print 'Loading classifier model ...'
classifier = load_model('model/classifier_model.h5')
print 'Load classifier model success.'

parser = argparse.ArgumentParser(description='doc2vec nn classifier')
parser.add_argument('--filename', dest='filename', default='', help='要 highlight 的新電影彈幕資料')
parser.add_argument('--preprocess_script_dirname', dest='preprocess_script_dirname', default='./preprocess-script/', help='放前處理程式(preprocess.js)的資料夾路徑')
parser.add_argument('--processed_data_dirname', dest='processed_data_dirname', default='./processed-data/', help='放前處理完後的彈幕資料後的資料夾路徑')

args = parser.parse_args()

def convert_words_to_vector(words):
    word_count = defaultdict(lambda: 0)
    for word in words:
        word_count[word] += 1
    doc_vec = np.zeros(d2v.vector_size)
    for word in words:
        try:
            doc_vec += d2v[word] * (word_count[word]/len(words))
        except KeyError:
            doc_vec += d2v[u'UNK'] * (word_count[word]/len(words))
    return doc_vec

def toClips(filename):
    """
    使用 './processed-script/split.py' 的 'toClip()'
    依照指定的時間間隔（30秒）將處理完的彈幕切割為數個片段，將每個片段中的所有彈幕串成同一列（視為一個 document）
    """

    interval = 30
    overlap = 15
    res = defaultdict(lambda: [])

    try:
        with open(filename) as f:
            data = json.load(f)
            for comment in data['comments']:
                time = int(comment['time'])
                # 0~30, 31~60, 61~90, ...
                if time%interval == 0 and time != 0:
                    res[time].append(comment)
                else:
                    res[(time//interval+1)*interval].append(comment)
                # 15~45, 46~75, 76~105, ...
                if time > 15:
                    if (time-overlap)%interval == 0:
                        res[time].append(comment)
                    else:
                        res[(time//interval+1)*interval + overlap].append(comment)
            # Merge words to document for every comment
            document_dict = {}
            for time, comments in sorted(res.items()):
                document = ' '.join([' '.join(comment['words']) for comment in comments])
                document_dict[time] = document
            return document_dict

    except FileNotFoundError:
        print('Error. Missing {}.'.format(filename))
        return None

def predict(filename, preprocess_script_dirname='./preprocess-script/', processed_data_dirname='./processed-data/'):
    """
    給定未處理過的電影的彈幕資料(格式比照'data/'內的json)，輸出經典橋段的時間
    """

    # 剛下載未處理過的彈幕(.json)必須放在 './data/' 中。
    # 使用 os.system 執行系統指令執行彈幕的前處理後，會把處理完的彈幕存到 <processed_data_dirname> 中。
    os.system('cd {} && node preprocess.js -f {}'.format(preprocess_script_dirname, filename))

    # 處理完資料，接下來就是要把 document 的內容轉成 vector 後，丟到 classifer 判斷是不是經典橋段
    document = toClips('{}{}'.format(processed_data_dirname, filename))

    # 把 clipped 過的資料 (每個row: <time> <document>) 存起來給別的 model 用
    fout = open('{}time-document-{}'.format(args.processed_data_dirname, filename.replace('json', 'txt')), 'w')
    for time, doc in sorted(document.items()):
        fout.write('{}\t{}\n'.format(time, doc.encode('utf8')))
    print 'Clipped {} to time-document format. Save to {}time-document-{}.'.format(filename, args.processed_data_dirname, filename)
    fout.close()

    # 預測經典橋段的時間
    highlight_time_ranges = []
    for time, doc in sorted(document.items()):
        # reload the d2v model to solve different prediction output when input the same document.
        d2v = Doc2Vec.load('model/doc2vec_model.d2v')
        doc_vec = d2v.infer_vector(doc.split())
        predict = classifier.predict(np.array([doc_vec]))[0][0]
        if int(round(predict)) == 1:
            highlight_time_ranges.append((time-30, time))
    return highlight_time_ranges

if __name__ == '__main__':
    if not args.filename:
        print 'Please specify --filename <movie_name>.json'
        exit(0)
    if not os.path.exists(args.processed_data_dirname):
        os.makedirs(args.processed_data_dirname)

    highlight_time_ranges = predict(args.filename, args.preprocess_script_dirname, args.processed_data_dirname)
    print highlight_time_ranges
