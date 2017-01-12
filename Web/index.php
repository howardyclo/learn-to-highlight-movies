<!DOCTYPE HTML>
<html>
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Bye-Bye 谷阿莫</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

	<link rel="icon" href="img/favicon.png">
	<link href="css/animate.min.css" rel="stylesheet">
	<link href="css/grayscale.css" rel="stylesheet">
	<link href="css/font-awesome.min.css" rel="stylesheet">

	</head>
<body id="page-top" data-spy="scroll" data-target=".navbar-fixed-top">
	<!-- Navigation -->
    <nav class="navbar navbar-custom navbar-fixed-top" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-main-collapse">
                    Menu <i class="fa fa-bars"></i>
                </button>
                <a class="navbar-brand page-scroll" href="#page-top">
                    <i class="fa fa-play-circle"></i> <span class="light">Bye-Bye</span> 谷阿莫
                </a>
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse navbar-right navbar-main-collapse">
                <ul class="nav navbar-nav">
                    <!-- Hidden li included to remove active class from about link when scrolled up past about section -->
                    <li class="hidden">
                        <a href="#page-top"></a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#about"><i class="fa fa-info-circle" aria-hidden="true"></i> 項目介紹</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#now"><i class="fa fa-tasks" aria-hidden="true"></i> 處理進度</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="#history"><i class="fa fa-history" aria-hidden="true"></i> 失業經歷</a>
                    </li>
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Intro Header -->
    <header class="intro">
        <div class="intro-body">
            <div class="container animated zoomInUp">
                <div class="row">
                    <div class="col-md-8 col-md-offset-2">
                        <h1 class="brand-heading">“掰掰，谷阿莫”</h1>
                        <p class="intro-text">我是谷阿莫<br>今天要說一個讓我失業的故事QQ</p>
                         <?php
							include("mysql_connect.inc.php");
							$sql = "SELECT count(*) FROM processlist WHERE progress < 3"; //在test資料表中選擇所有欄位
							$result = mysql_query($sql);
							while($row = mysql_fetch_row($result))
							{
								if($row[0] == 0){
									echo '
							<form id="avform" name="form" method="post" onsubmit="return PostData()" class="form-inline" role="form" target="id_iframe">
                        		<div class="form-group">
								<input type="text" name="namec" class="form-control input-lg av-input" style="border-radius:50px;" placeholder="請輸入av號,例如:84649"> 
								<input type="submit" name="button" value="讓他失業" class="btn btn-default btn-lg av-btn" style="border-radius:50px;">
								</div>
							</form>
									';
								}		
								else
								{
									echo '<h3>目前尚有正在影片處理中</h3><h3><a href="#now" class="page-scroll btn btn-default btn-lg animated">查看進度</a></h3>';
								}
							}
							?>
                        	
                        <a href="#about" class="btn btn-circle page-scroll">
                            <i class="fa fa-angle-double-down animated"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- About Section -->
    <section id="about" class="container content-section text-center">
        <div class="row">
            <div class="col-lg-8 col-lg-offset-2">
                <h2><i class="fa fa-info-circle" aria-hidden="true"></i> 項目介紹</h2>
                <p>“掰掰，谷阿莫”——是一個分析<a href='http://www.bilibili.com'>嗶哩嗶哩彈幕視頻網</a>(Bilibili)影片的一個項目。</p>
                <p>本項目從<a href='http://www.bilibili.com'>嗶哩嗶哩彈幕視頻網</a>(Bilibili)獲取影片彈幕內容與數量，從而進行Word2Vector等處理，分析出影片的精彩時刻。</p>
                <p>最終自動生成一個精彩片段的合集影片。如果不好看，你來打我呀~</p>
            </div>
        </div>
    </section>

    <section id="now" class="container content-section text-center">
       <div class="download-section">
            <div class="col-lg-8 col-lg-offset-2">
                <h2><i class="fa fa-tasks" aria-hidden="true"></i> 處理進度</h2>
                <?php
					include("mysql_connect.inc.php");
					$sql = "SELECT * FROM processlist WHERE ID = (select max(id)from processlist)"; //在test資料表中選擇所有欄位
					$result = mysql_query($sql);
					while($row = mysql_fetch_row($result))
					{
						$newavid = $row[1];
						echo '<h3>'.$row[3].'</h3>';
						if($row[2] == '0'){
							$status = "加入隊列";
							$nowper = 10;
							$pgbstyle = '';
						}
						if($row[2] == '1'){
							$status = "下載中";
							$nowper = 50;
							$pgbstyle = '';
						}
						if($row[2] == '2'){
							$status = "剪輯中";
							$nowper = 70;
							$pgbstyle = '';
						}
						if($row[2] == '3'){
							$status = "處理完畢";
							$nowper = 100;
							$pgbstyle = 'progress-bar-success ';
						}
						if($row[2] == '4'){
							$status = "發生錯誤";
							$nowper = 100;
							$pgbstyle = 'progress-bar-danger ';
						}	
					}
                echo '<hr><h4>'.$status.'</h4>

                <div class="progress">
  					<div class="progress-bar '.$pgbstyle.'progress-bar-striped active" role="progressbar" aria-valuenow="'.$nowper.'" aria-valuemin="0" aria-valuemax="100" style="width: '.$nowper.'%">
    				<span class="sr-only">'.$status.'</span>
  					</div>
				</div>';
				if($status == "處理完畢"){
					echo '
						<button class="btn btn-default btn-lg" data-toggle="modal" data-target="#myModal" onclick="document.getElementById(';
										echo "'video'";
										echo ').play()"><i class="fa fa-play-circle aria-hidden="true"></i> 播放</button>
						<!-- 模态框（Modal） -->
						<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
							<div class="modal-dialog" style="background-color: #000000;display: inline-block; width: 80%;">
								<div class="modal-content" style="background-color: #000000;">
									<div class="modal-header">
										<button type="button" class="close" data-dismiss="modal" aria-hidden="true">
											&times;
										</button>
										<h4 class="modal-title" id="myModalLabel">
											精彩片段
										</h4>
									</div>
									<div class="modal-body">
										<video id="video" width=80% height=80% controls loop><source src="./videos/'.$newavid.'.mp4" type="video/mp4">
										</video>
									</div>
									<div class="modal-footer">
									<center>
										<button type="button" class="btn btn-default btn-lg" data-dismiss="modal" onclick="document.getElementById(';
										echo "'video'";
										echo ').pause()"><i class="fa fa-times-circle-o" aria-hidden="true"></i> 關閉</button>
									</center>
									</div>
								</div><!-- /.modal-content -->
							</div><!-- /.modal -->
					';
				}
				elseif($status != "發生錯誤"){
					echo "<script>function myrefresh() 
							{ 
							       window.location.reload(); 
							}
							setTimeout('myrefresh()',10000); //指定5秒刷新一次 
							</script>"; 
				}
				?>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="history" class="container content-section text-center">
        <div class="row">
            <div class="col-md-10 col-md-offset-1">
            <h2><i class="fa fa-history" aria-hidden="true"></i> 失業經歷</h2>
                <?php
					include("mysql_connect.inc.php");
					$sql = "SELECT * FROM processlist"; //在test資料表中選擇所有欄位
					$result = mysql_query($sql);
					echo '
					<table class="table">
					<thead>
					<tr>
					<td>AV號</td>
					<td>標題</td>
					<td>精彩片段</td>
					</tr>
					</thead>
					';
					while($row = mysql_fetch_row($result))
					{
						if($row[2] == '0')
							$status = "加入隊列";
						if($row[2] == '1')
							$status = "下載中";
						if($row[2] == '2')
							$status = "剪輯中";
						if($row[2] == '3')
							$status = "處理完畢";
						echo '<tr><td>'.$row[1].'</td><td>'.$row[3].'</td><td>';
						if($row[2] == '3'){echo'<a class="btn btn-default" href=player.php?av='.$row[1].'><i class="fa fa-play-circle aria-hidden="true"></i> 播放</a>';}
						echo '</td></tr>';
					}
					echo'</table>';
					?>
            </div>
        </div>
    </section>

    <footer>
        <div class="container text-center">
            <p>Copyright &copy; 2017 NTHU  <a href="http://make.cs.nthu.edu.tw/">Make Lab</a> & <a href="http://www.nlplab.cc/">NLP Lab</a></p>
        </div>
    </footer>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js" integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.3/jquery.easing.min.js"></script>
    <script src="js/grayscale.min.js"></script>
    <script type="text/javascript">
    function PostData() {
        $.ajax({
            type: "POST",
            url: "addfinish.php",
            data : $('#avform').serialize(),
            success: function(msg) {
            	alert(msg);
            	window.location.href='index.php#now';
            	location.reload();
            }
        });
        return false;
    }
</script>

</body>
</html>