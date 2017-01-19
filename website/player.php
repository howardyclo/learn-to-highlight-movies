<?php echo'
<!DOCTYPE HTML>
<html>
<head>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Bye-Bye 谷阿莫</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
    <link rel="icon" href="img/favicon.png">
	<link href="css/grayscale.css" rel="stylesheet">
	<link href="./css/video-js.css" rel="stylesheet">

    <title>'.$_GET["av"].'精彩片段</title>
    ';
    echo '
  </head>

  <body id="page-top" data-spy="scroll" data-target=".navbar-fixed-top">
	<!-- Navigation -->
    <nav class="navbar navbar-custom navbar-fixed-top" role="navigation">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-main-collapse">
                    Menu <i class="fa fa-bars"></i>
                </button>
                <a class="navbar-brand page-scroll" href="index.php">
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
                        <a class="page-scroll" href="index.php#about"><i class="fa fa-info-circle" aria-hidden="true"></i> 項目介紹</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="index.php#now"><i class="fa fa-tasks" aria-hidden="true"></i> 處理進度</a>
                    </li>
                    <li>
                        <a class="page-scroll" href="index.php#history"><i class="fa fa-history" aria-hidden="true"></i> 失業經歷</a>
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
            <div class="container">
                <div class="row">
                        <video  id="my-video" style="border:#35a5e5 1px solid;box-shadow: 0 0 30px rgba(81, 203, 238, 1);-webkit-box-shadow: 0 0 30px rgba(81, 203, 238, 1);-moz-box-shadow: 0 0 30px rgba(81, 203, 238, 1);" class="video-js vjs-big-play-centered vjs-16-9" controls preload="auto" width="640" height="360" data-setup="{}"><source src="./videos/';
   							echo $_GET["av"];
   								echo '.mp4" type="video/mp4">
						</video>
                        <a href="index.php#history" class="btn btn-circle page-scroll"><i class="fa fa-angle-left animated"></i></a>
                </div>
            </div>
        </div>
    </header>
        <footer>
        <div class="container text-center">
            <p>Copyright &copy; 2017 NTHU  <a href="http://make.cs.nthu.edu.tw/">Make Lab</a> & <a href="http://www.nlplab.cc/">NLP Lab</a></p>
        </div>
    </footer>
<script src="https://code.jquery.com/jquery-3.1.1.min.js" integrity="sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.3/jquery.easing.min.js"></script>
<script src="js/grayscale.min.js"></script>
<script src="js/video.js"></script>
</body>
</html>';?>

