<?php
error_reporting(0);
include("mysql_connect.inc.php");
$namec = $_POST['namec'];
//判斷帳號密碼是否為空值
//搜尋資料庫資料
$sql = "SELECT max(`ID`) FROM processlist";
$result = mysql_query($sql);
$row = @mysql_fetch_row($result);
$count =  $row[0] + 1;

$ctsql = "SELECT count(*) FROM processlist WHERE progress < 3";
$ctresult = mysql_query($ctsql);
$ctrow = @mysql_fetch_row($ctresult);

$idsql = "SELECT count(*) FROM processlist WHERE video = ".$namec;
$idresult = mysql_query($idsql);
$idrow = @mysql_fetch_row($idresult);

//確認密碼輸入的正確性
if(is_numeric($namec))
{
        if((int)$ctrow[0]>0)
        {
                echo '目前尚有影片處理中';
        }
        else
        {
                if((int)$idrow[0]>0)
                {
                echo '存在相同影片';
                }
                else
               {
                        $sql = "insert into processlist (ID,video,progress) values ('$count', '$namec', '0')";
                        if(mysql_query($sql))
                        {
                                echo '新增成功!';
                        }
                        else
                        {
                                echo '新增失敗!';
                        }
               }
        }
}
else
{
        echo '請輸入正確的格式';
}
?>