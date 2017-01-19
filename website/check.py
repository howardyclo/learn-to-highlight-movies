import pymysql
import time
import NewCut
# 打开数据库连接
db = pymysql.connect("localhost","root","passwd","bilibili" )
cursor = db.cursor()
cursor.execute("SELECT count(*) FROM processlist WHERE progress < 3")
data = cursor.fetchone()
NotThree = data[0]
db.close()
if(NotThree > 0):
	db = pymysql.connect("localhost","root","passwd","bilibili" )
	cursor = db.cursor()
	cursor.execute("SELECT video FROM processlist WHERE progress < 3")
	data = cursor.fetchone()
	LastInt = data[0]
	db.close()
	print("Last Interrupt!Now restart with video "+str(LastInt))
	NewCut.AutoEditMovie(str(LastInt))
else:
	print("No interrupt!")
db = pymysql.connect("localhost","root","passwd","bilibili" )
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM processlist")
data = cursor.fetchone()
db.close()
NowValue = data[0]
print("Listening Start!Now have "+str(NowValue)+" videos")
while True:
	db = pymysql.connect("localhost","root","passwd","bilibili" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	#cursor.execute("SELECT progress FROM request WHERE videoID='123' ")
	cursor.execute("SELECT COUNT(*) FROM processlist")
	# 使用 fetchone() 方法获取一条数据库。
	print("Listening!Now have "+str(NowValue)+" videos")
	data = cursor.fetchone()
	if(data[0]!=NowValue):
		print("Changed!") #有新的影片
		NowValue = data[0]
		cursor.execute("SELECT MAX(ID) FROM processlist")
		data = cursor.fetchone()
		MAXID = data[0]
		cursor.execute("SELECT video FROM processlist WHERE ID = '"+str(MAXID)+"'")
		data = cursor.fetchone()
		NewestVideo = str(data[0])
		NewCut.AutoEditMovie(NewestVideo)
	db.close()
	time.sleep(5)

# 关闭数据库连接
