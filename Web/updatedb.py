import pymysql
def UpdateProgress(videoID,status,title):
	db = pymysql.connect("localhost","root","passwd","bilibili",charset="utf8")
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	#cursor.execute("SELECT progress FROM request WHERE videoID='123' ")
	if(title == '0'):
		cursor.execute("UPDATE processlist SET progress = '"+str(status)+"' WHERE video = '"+str(videoID)+"'")
	else:
		cursor.execute("UPDATE processlist SET progress = '"+str(status)+"' WHERE video = '"+str(videoID)+"'")
		db.commit()
		cursor.execute("UPDATE processlist SET title = '"+str(title)+"' WHERE video = '"+str(videoID)+"'")
	db.commit()
	db.close()
	# 关闭数据库连接