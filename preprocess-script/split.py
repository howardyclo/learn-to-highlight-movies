import json
import sys
from collections import defaultdict

def toClips(filename):
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
            return res
    except FileNotFoundError:
        print('Error. Missing {}.'.format(filename))
        return None

IN_FOLDER_PATH = '../processed-data/'
OUT_FOLDER_PATH = '../processed-data/'

fname = sys.argv[1]
data = toClips(IN_FOLDER_PATH + fname)

if data == None:
    sys.exit(0)

f_POS = open(OUT_FOLDER_PATH + fname.replace('.json', '') + '_POS.txt', 'w')
f_NEG = open(OUT_FOLDER_PATH + fname.replace('.json', '') + '_NEG.txt', 'w')

POS_count = 0
NEG_count = 0

for time, comments in data.items():
    if any(comment['class']=='POS' for comment in comments):
        f_POS.write('%s\n' % (' '.join([' '.join(comment['words']) for comment in comments])))
    else:
        f_NEG.write('%s\n' % (' '.join([' '.join(comment['words']) for comment in comments])))

print('Process success: {}'.format(fname))

f_POS.close()
f_NEG.close()
