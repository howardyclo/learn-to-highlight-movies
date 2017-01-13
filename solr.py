import codecs 
import re
import os
import json
import pysolr

delete_replace = u'[’!"#$%&\'()*+,-./:;‧<=>?@[\\]^_`{|}~、，．。！★◆◤◢↘↑↓→↗《》【】▼＆／◎，『』※（）「」╭╯│？～]+'

f = codecs.open(u'training-data/train_POS.txt',"r", "utf-8")

line = f.read().split('\n')
array = []

# 將所有資料加index
def data_prepossing():
	c = 0
	for i in line:
		dic={}
		dic["id"] = c
		content = re.sub(delete_replace, '', i)
		content = content.replace("  "," ")
		dic["content"] = content
		dic["label"] = "1"
		array += [dic]
		c += 1

	f = codecs.open(u'training-data/train_NEG.txt',"r", "utf-8")
	line = f.read().split('\n')

	for i in line:
		dic={}
		dic["id"] = c
		content = re.sub(delete_replace, '', i)
		content = content.replace("  "," ")
		dic["content"] = content
		dic["label"] = "0"
		array += [dic]
		c += 1


	r = json.dumps(array)
	with codecs.open("input.json", "w", "utf-8") as f: 
		f.write(r)
	
#input data to solr
def solr_input():
	coll = "project2"
	data = "E:\python\data_scient_project\input.json"
	command = "java -Dtype=application/json -Dc="+coll+" -jar post.jar "+data
	os.system(command)

def comput_precision(test_pos):
	'''parameter
		test_pos : 輸入要測試的資料
	'''
	f = codecs.open(test_url,"r", "utf-8")
	line = f.read().split('\n')
	check = 0
	for i in line:
		content = re.sub(delete_replace, '', i)
		content = content.replace("  "," ")
		results = solr.search(content, rows=1)
		for r in results:
			if(r['label'][0] == 0):
				check += 1
		
	return check

def search(content):
	'''parameter
		content : 輸入要查詢的內容
	'''
	content = "前方 高能"
	solr = pysolr.Solr('http://localhost:8983/solr/project2',timeout=10)
	results = solr.search(content, rows=1)
	for i in results:
		print i

def serch_output_time(data_url):
	'''parameter
		data_url : 輸入一部影片斷詞後的data position
	'''
    output = []
    f = codecs.open(data_url,"r", "utf-8")
    line = f.read().split('\n')
    for i in line:
        time,content = i.split('	')
        results = solr.search(content, rows=1)
        for r in results:
            label = (r['label'][0])
            if(label == 1):
                output += [(int(time)-30,int(time))]
    return output
	
if __name__ == "__main__":
    #data_prepossing()
	#solr_input()
	#check = couput_precision(u"test_NEG.txt")
	