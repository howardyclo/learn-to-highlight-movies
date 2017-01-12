# -*- coding=utf-8 -*-
import re 
import json 
import os
import sys
import codecs

def xml2json(filename):
	infile = open(filename+".xml", "r",encoding="utf-8")  #打开文件

	regex = r"\d+(?=\W\W[chatid]{6})"
	regex_time = r"(?<=[p][=]\W)\d*\W\d*(?=[,])"
	lineNum = 0

	output = {'information': [], 'comments': []}
	for line in infile:
		match1 = re.search('\d+(?=[<]\W[chatid]{6})', line)
		match2 = re.search('(?<=[p][=]\W).*(?=\W[>])', line)
		match3 = re.search('(?<=["][>]).*(?=[<][/][d])', line)

		if match1:
			output['information'].append({'CID': match1.group()})
		if match2 and match3:
			cstr = match2.group()
			u1, u2, u3, u4, u5, u6, u7, u8 = cstr.split(',', 7)
			comment = {'time': float(u1),
						'mode': int(u2),
						'fontsize': int(u3),
						'fontcolor': int(u4),
						'sendtime': int(u5),
						'pool': int(u6),
						'hash': u7,
						'dbid': u8,
						'content': match3.group().replace('"', '').replace('\\', '')}
			output['comments'].append(comment)

	infile.close()    #文件关闭

	with open(filename+".json", 'w',encoding="utf-8") as outfile:
		json.dump(output, outfile, ensure_ascii=False, indent=4)
	print('Done!')