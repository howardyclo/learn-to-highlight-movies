#coding:utf-8
import os 
import urllib.request
import json
import updatedb
import xml2json
import countbase
import coverdhl
import removelast
from moviepy.editor import *
import moviepy.video.fx.all as vfx
def AutoEditMovie(avNumber):
	#獲取Title
	#方法1
	try:
		InfoCommand ='you-get -i -c ./cookies.txt http://www.bilibili.com/video/av'+avNumber+'/'
		InfoData = os.popen(InfoCommand)
		Videoinfo = InfoData.readlines()  #读取命令行的输出到一个list
		InfoList = []
		for line in Videoinfo:  #按行遍历
		    line = line.strip('\r\n')
		    InfoList.append(line)
		TitleOne = (InfoList[1].split(':      ', 1 ))[1]
	except:
		TitleOne = ""
		print("Can't get title1.")

	#方法2
	try:
		InfoUrl = 'http://www.bilibilijj.com/Api/AvToCid/'+avNumber+'/1'
		with urllib.request.urlopen(InfoUrl) as response:
   			html = response.read()
		def html_decode(s):
		    htmlCodes = (
		            ("'", '&#39;'),
		            ('"', '&quot;'),
		            ('>', '&gt;'),
		            ('<', '&lt;'),
		            ('&', '&amp;')
		        )
		    for code in htmlCodes:
		        s = s.replace(code[1], code[0])
		    return s
		htmldecode = html_decode(html.decode("utf-8"))
		InfoData = json.loads(htmldecode)
		TitleTwo = InfoData['title']
	except:
		TitleTwo = ""
		print("Can't get title2.")

	print(TitleOne,TitleTwo)
	if(TitleTwo != ""):
		Title = TitleTwo
	else:
		Title = TitleOne

	if(Title == ""):
		updatedb.UpdateProgress(avNumber,4,"發生錯誤或影片不存在") #1=下載
		return

	#下載
	try:
		updatedb.UpdateProgress(avNumber,1,Title) #1=下載
		DownCommand ='you-get -o temp -y proxy.uku.im:443 -c ./cookies.txt http://www.bilibili.com/video/av'+avNumber+'/'
		DoDownload = os.system(DownCommand)
	except:
		updatedb.UpdateProgress(avNumber,4,"下載失敗") #1=下載
		return
	
	

	#判斷是否下載完畢
	#if(os.path.isfile('./temp/'+TitleOne+'.flv')):
	#	print("FLV Download Complete!")
	#	VideoFileName = TitleOne+'.flv'
	#if(os.path.isfile('./temp/'+TitleTwo+'.flv')):
	#	print("FLV Download Complete!")
	#	VideoFileName = TitleTwo+'.flv'
	#if(os.path.isfile('./temp/'+TitleOne+'.mp4')):
	#	print("MP4 Download Complete!")
	#	VideoFileName = TitleOne+'.mp4'
	#if(os.path.isfile('./temp/'+TitleTwo+'.mp4')):
	#	print("MP4 Download Complete!")
	#	VideoFileName = TitleTwo+'.mp4'
	if(os.path.isfile('./temp/'+Title+'.flv')):
		print("FLV Download Complete!")
		VideoFileName = Title+'.flv'
	if(os.path.isfile('./temp/'+Title+'.mp4')):
		print("MP4 Download Complete!")
		VideoFileName = Title+'.mp4'

	try:
		if(os.path.isfile('./temp/'+Title+'.cmt.xml')):
			print("Found Danmuku!")
			xml2json.xml2json('./temp/'+Title+'.cmt')
			if(os.path.isfile('./temp/'+Title+'.cmt.json')):
				Highlights = countbase.HightLight('./temp/'+Title+'.cmt')
				print("Found HighLight!")
				print(Highlights)
		ResVideoFileName = './temp/'+VideoFileName
		updatedb.UpdateProgress(avNumber,2,"0") #2=剪輯
		Highlights = coverdhl.CoverHLS(Highlights)
		print(Highlights)
	except:
		updatedb.UpdateProgress(avNumber,4,"精彩片段分析出錯") #1=下載
		return

	def CutVideo(Highlights,VideoFileName,avNumber):
		HighlightList = []
		for HighlightsTime in Highlights:
			HighlighClip = VideoFileClip(ResVideoFileName).subclip(HighlightsTime[0],HighlightsTime[1])
			HighlightList.append(HighlighClip)
		# 音量×0.8
		Merge_clip = concatenate_videoclips(HighlightList)
		clip = Merge_clip.volumex(0.8)
		# 加标题
		txt_clip = TextClip(VideoFileName[:-4]+"\n精彩片段",font="font.otf",fontsize=40,color='white')
		# 标题持续5秒
		txt_clip = txt_clip.set_pos('center').set_duration(5)
		# 合并标题和影片
		video = CompositeVideoClip([clip, txt_clip])
		# 输出影片
		#video.write_videofile(VideoFileName[:-4]+"_edited.mp4")
		#video.write_videofile("videos/"+avNumber.decode('utf-8')+".mp4")
		video.write_videofile("videos/"+avNumber+".mp4")
	
	
	try:
		CutVideo(Highlights,VideoFileName,avNumber)
		updatedb.UpdateProgress(avNumber,3,"0") #3=完成
		return
	except:
		removelast.RemoveLastHL(Highlights)
		print(Highlights)
		try:
			CutVideo(Highlights,VideoFileName,avNumber)
			updatedb.UpdateProgress(avNumber,3,"0") #3=完成
			return
		except:
			updatedb.UpdateProgress(avNumber,4,"剪輯發生錯誤") #1=下載
			return
	else:
		updatedb.UpdateProgress(avNumber,3,"0") #3=完成
		return
