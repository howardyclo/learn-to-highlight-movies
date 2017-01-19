# [Learn to Highlight Movies](https://signxer.xyz/bilibili/)

(Under Construction)

**Keywords**: `video shots retrieval`, `document classification`, `TF-IDF (solr)`, `word embeddings (Word2Vec)`, `document embeddings (Doc2Vec)`, `neural network (Keras)`

Learn-to-Highlight-Movies is a **movie highlights retrieval** project that uses several approaches to automatically highlight movies from [bilibili](https://www.bilibili.com/), which is one of the largest video sharing platforms in China with time-sync comments, also known as **bullet screen comments**. (We'll abbreviate "bullet screen comments" to "comments" in the following paragraphs.)

> Notes: This is a final project from **NTHU Data Science Fall 2016**. The datasets and code comments may appeared in Chinese, but hey! there's a [neural machine trainslation](https://translate.google.com.tw/?hl=zh-TW#zh-CN/en/Chinese) now! :joy:

## Problem Definition and Methods

Unlike the other image or speech based approaches, we mainly formalize our movie highlights retrieval task as a **document classification** problem. Each document represents all comments appeared within a movie clip of fixed time interval. We classify if the document is **POS** (highlights) or **NEG** (non-highlights) in a **supervised learning** manner.

We also explore the other two methods for comparing the performances and discuss their pros and cons in the end of the article, so here we'll focus on these three methods:
- **Count-based**
- **TF-IDF**
- **Supervised learning**

## Datasets
- **Bullet screen comments**: Steven Chou's famous movies and their corresponding bullet screen comments. See `data/<movie_name>.json`.
- **Temporal labels**: We took several days to watch the movies and manually labeled timestamps (start and end) of interesting movie clips as our highlights. See `label/<movie_name>.txt`

## Data Preprocessing
`preprocess.js`
- Cleaning: delete unwanted data attributes and only keep `time` and `content`.
- 根據每一部電影在 `../label/` 資料夾中對應的經典橋段時間的標籤資料，來標註彈幕，例如，如果某一時間的彈幕出現在經典橋段的時間內，就將該彈幕的資料欄位 `class` 標註為 `POS`，不是則 `NEG`。
- 為了之後訓練詞向量，因此也需要先使用 [jieba](https://github.com/fxsjy/jieba) 對每個彈幕的內容做斷詞、擷取關鍵詞，為了刪掉高頻率又沒有意義的詞，我們只保留關鍵詞的部分當作斷詞的結果，但是要保留詞出現在彈幕內容的次序。
- 標準化 `23333`, `66666`, `哈哈哈哈哈` 等這些同義但是不同長度的詞，我們把它們全部標準化成一個字 `哈`。
- 最後存入 `processed-data/<movie_name>.json`。

`split.py`
- 負責把某部電影經過 `preprocess.js` 處理好的彈幕，也就是 `processed-data/<movie_name>.json`，依照指定的時間間隔（30秒）切割為數個片段，將每個片段中的所有彈幕串成同一列（視為一個 document），片段中若包含任一條 `class` 為 `POS` 的彈幕，則將其寫入 `processed-data/<movie_name>_POS.txt`，反之則寫入 `processed-data/<movie_name>_NEG.txt`。

`merge.py`
- 負責將資料處理成訓練詞向量與機器學習模型所需的輸入格式，將所有 `<movie_name>_<label>.txt` 順序打亂後，寫進 `all_POS.txt`, `all_NEG.txt`, `train_POS.txt`, `train_POS.txt`, `test_POS.txt`, `test_POS.txt`。除此之外，還將低頻詞都標準化成 `UNK`，以提升詞向量的品質。

## Count-Based
每30秒做間隔，並用slide window的概念，使時間間隔變得比較smooth。
例 : (0~30), (15~45), (30~60)，並取大於一個標準差以上的時間間隔當作highlight，而選取此臨界值的依據，是由測試參數，並調整能得到最好的結果為基準，測試的結果如下，圖(一) 與 圖(二）為其中一部 “九品芝麻官” 統計的彈幕數量結果，我們再把這些比較高的時間段，當作精彩片段。

![](https://i.imgur.com/dMpwJ0p.png)

圖(一) 藍色與橘色分別表示不同標準差下的 accuracy，而亦區分成三種不同的 window size，分別是 15, 30, 45 秒，可得知一個標準差有較好的 accuracy，又以 30 秒作為 window size 會擁有最好的結果。

![](https://i.imgur.com/WIkOT8v.png)

圖(二) 九品芝麻官的彈幕趨勢，紅色線以上為平均加上一個標準差作為臨界值。

## Supervised Learning

### Text Representation using Word2Vec & Doc2Vec

我們都知道 Word2Vec 能夠將 word 表示成 vector，語法或語意上相似的 word 在 vector space 中具有相似的向量，像是：word_vec("man") - word_vec("woman") 近似於 word_vec("king") - word_vec("queen")。

Gensim 不只提供了 Word2Vec 套件來表示一個 word ，還提供了 Doc2Vec 套件來表示 sentence 或 document 的 vector，不過 Doc2Vec 內部也有訓練好 Word2Vec，所以我們依然可以拿 Doc2Vec 取得一個 word 的向量。

![](https://i.imgur.com/PeiFVHY.png)

### Classifier Model

我們將上述 train 好的 Doc2Vec model 當成 classifer 的 input，並且使用 Keras 來實作 feedforward neural net 來訓練模型，以下為 model 的參數與訓練 settings：
- 2 hidden layers, each contains 500 neurons
- Weight initialization using normal distribution
- ReLU activation function for each hidden layer
- Sigmoid activation function for output layer
- Use dropout for each hidden layer
- Adam optimizer
- Binary crossentropy loss function

### 三種 Text Representation 在 Classifer 的 Performance Experiment

我們實驗三種 document vector representation 當作輸入：
- 將文件中的每個詞向量相加 (Word2Vec)
- 將文件中每個詞向量乘上權重後再相加，權重為該字在該文件中出現字數 (Word2Vec + Weight)
- 使用 Doc2Vec



討論：從實驗結果得知在 Doc2Vec 會比 Word2Vec 的 approach 還要來得好，而 Word2Vec approach 中，不加上權重會比較好，可能是因為彈幕中會受到有許多稀有字 (normalize 成 "UNK") 的影響。

## TF-IDF

### 介紹

Solr 是一種全文檢索系統，而全文檢索系統是針對大量文件的內容，可輸入任意字詞的關鍵字及其邏輯運算 (AND、OR 、NOT) 等，進行快速內文查詢，並提供查詢結果，依其文件符合程度的評分排序或文件相關資訊分類，以便進一步進行統計、分析及彙整的系統。常見的全文檢索的資料對象有新聞、文件報告、期刋、書籍或是網站內容等。

對於全文檢索最簡單的方式，就是一個一個慢慢比對，也就是**循序搜尋** (Sequential Search) 的方法，但是對於大量的長篇文件搜尋，就會有效率不彰的問題。

Sorl的全文檢索系統採用**索引** (index) 的方法，也就是先將文件內容切割出字詞單元 (token)，再將這些字詞以「雜湊表」或「B+樹」等資料結構，建立索引檔，紀錄其文件編號及在文件中出現的位置。在進行查詢時，系統先將輸入的字串，進行字詞單元分析，再將這些字詞一一使用索引快速搜尋，接著將結果依輸入的條件進行邏輯運算，並依在文件中出現的次數等關係計算各結果的權重，最後排序輸出結果。

### 安裝教學

Solr 必須運行在 Java1.5 或更高版本的 Java 虛擬機中，運行標准Solr 服務只需要安裝JRE 即可，但如果需要擴展功能或編譯源碼則需要下載JDK 來完成。
到[官網](http://lucene.apache.org/solr/)下載最新的安裝包，解壓縮後就安裝完成啦(X)。

用 cmd 進入 `solr/bin` 資料夾，輸入:
```
$ solr.cmd start
```
看到下面這個就可以開始 happy searching 惹 ~
```
Archiving 1 old GC log files to D:\solr-6.3.0\solr-6.3.0\server\logs\archived
Archiving 1 console log files to D:\solr-6.3.0\solr-6.3.0\server\logs\archived
Rotating solr logs, keeping a max of 9 generations
Waiting up to 30 to see Solr running on port 8983
Started Solr server on port 8983. Happy searching!
```
之後打開瀏覽器，輸入 http://localhost:8983/solr/ ， 就可以看到Solr的管理介面。
![solr](https://i.imgur.com/pWVI5XB.png)

**[hint]**
在windows系統下執行，必須修改solr.cmd檔
在@echo off 下一行加入
```
$ set PATH=%WINDIR%\System32;%PATH%;
```

* [其他solr指令](https://cwiki.apache.org/confluence/display/solr/Running+Solr)

### 建立資料庫

一樣在solr/bin資料庫底下輸入:
```
$ solr create -c test
```
接著看solr管理頁面就可以看到test的Core出現啦 !
![](https://i.imgur.com/5syn0QB.png)

### 上傳資料

solr可以支援 josn、xml 等等檔案上傳，上傳利用solr/example/exampledocs資料夾內的post.jar上傳 ~~

```
$ java -Dtype=application/json -Dc=core_name -jar post.jar data_position
```
進入solr管理頁面，選定core後按下query就可以看到上傳資料惹~~
![](https://i.imgur.com/pDuj6et.png)

**[hint]**
查看 post 其他指令

```
$ java -jar post.jar -help
```

### 設定schema

在查詢前，要先設定斷詞的方法。
在solr/server/solr/ 找到core的資料夾進去， 打開conf/managed-schema

**修改斷詞方法**
* 找到:
```html
<field name="content" type="string" />
```
* 改成:
```html
<field name="content" type="text_ik" multiValued="false" indexed="true" required="false" stored="true" />
```
* 然後在最底下加入:
因為原本input資料就有先斷詞過了，所以在這邊就使用空白來斷詞
```html
<fieldType name="text_ik" class="solr.TextField">
    <analyzer type="index">
	  <tokenizer class="solr.PatternTokenizerFactory" pattern="\s* \s*"/>
    </analyzer>
    <analyzer type="query">
	  <tokenizer class="solr.PatternTokenizerFactory" pattern="\s* \s*"/>
    </analyzer>
</fieldType>
```

打完存檔後，將solr重啟
```
$ solr restart -p 8983
```

進入solr管理介面，選擇Analysis，在Field輸入今天 天氣 很好，按下Analyse Values就可以看看是否斷詞設定有成功。
![](https://i.imgur.com/6x9O0jK.png)

**[hint]**
* [其他斷詞方法](https://cwiki.apache.org/confluence/display/solr/Tokenizers)

### 開始 happy search

搞了這麼多步驟建環境，終於可以開始查詢惹 XDD
接下來我們使用python 的 pysolr package來進行查詢~
```
$ pip install pysolr
```
程式如下:
![](https://i.imgur.com/B7PIfdJ.png)

## “掰掰，谷阿莫” 網站搭建說明

### 1. 環境要求
- 一個Web伺服器(我用[XAMPP](https://www.apachefriends.org/))
- [PHP](https://www.php.net/)
- [MySQL](https://www.mysql.com/)
- [Python 3.6](https://www.python.org/)

### 2. Python套件需求
- [you-get](https://github.com/soimort/you-get)
- [pymysql](https://github.com/PyMySQL/PyMySQL)
- [moviepy](https://github.com/Zulko/moviepy)

#### 2.1 其中moviepy還需要
- [FFMPEG](https://ffmpeg.org/)
- [ImageMagick®](http://www.imagemagick.org/script/index.php)

### 3. 使用方法

#### 3.1 安裝環境
根據上述要求，搭建好所需環境。
如果是Windows系統，需要手動定義ImageMagick的位置。詳情參考moviepy的[文檔](http://zulko.github.io/moviepy/install.html)。

#### 3.2 放入Web伺服器
將所有內容放入Web伺服器的資料夾內。

#### 3.3 導入修改SQL
導入/sql資料夾內的bilibili.sql。
默認資料庫名稱為bilibili，資料表為processlist，賬戶為root，密碼為passwd。
如需修改，請修改mysql_connect.inc.php,updatedb.py,check.py中的內容。

#### 3.4 運行
執行資料夾內的run.cmd或者使用指令
```
$ python check.py
```

會把下載的影片以及彈幕放在/temp資料夾，處理完的影片放在/video資料夾。

### 4. SQL結構說明
- ID - 本網站的影片ID
- video - bilibili的av號
- progress - 影片處理進度(0-加入隊列，1-下載中，2-剪輯中，3-處理完畢，4-發生錯誤)
- title - 影片標題

### 5. 主要檔案功能說明
- check.py - 檢查MySQL是否變動
- countbase.py - 以彈幕數量為基準的精彩片段判斷
- coverdhl.py - 合併相近的精彩片段時間
- NewCut.py - 下載、剪輯影片
- removelast.py - 當彈幕時間超過影片時間時，把最後的時間變成影片的長度
- updatedb.py - Python連接資料庫，更新影片處理狀態
- xml2json.py - 把XML彈幕轉換為Json
- index.php - 主頁
- player.php - 播放器
- mysql_connect.inc.php - PHP連結資料庫
- addfinish.php - 新增影片記錄

## Final Results and Discussion
The following table combines experiment results of three different methods.

Methods | Precision | Recall | F-measure |
--------| --------- | ------ | --------- |
Count-based | 0.45 | 0.21 | 0.27 |
TF-IDF | 0.78 | **0.94** | 0.85
Word2Vec | 0.88 | 0.7 | 0.78 |
Word2Vec + Weight | 0.78 | 0.64 | 0.7 |
Doc2Vec | **0.93** | 0.85 | **0.89** |

### Count-Based
Pros: 各類型的影片都通用。
Cons: 開始和結尾會有高估。

### TF-IDF
Pros: 跟 Machine learning model 表現得差不多好。
Cons: 但同樣也無法適用於不同類別的影片。

### Supervised Learning
Pros: 預測的電影經典片段的結果較為良好。
Cons: 需要 training data，需要大量時間去標註是否為經典片段的時間，而且如果是預測與 training data 本身差很多的電影，其效果就會不如 count-based 的好。

## References
- [Gensim Word2Vec & Doc2Vec](https://radimrehurek.com/gensim/)
- [Sentiment Analysis Using Doc2Vec](http://linanqiu.github.io/2015/10/07/word2vec-sentiment/)
- [Keras for building deep learning model](https://keras.io/)
- [Solr Document](https://cwiki.apache.org/confluence/display/solr/Schema+API)
- [Pysolr Document](https://pypi.python.org/pypi/pysolr/3.1.0)
- [Reading the Videos: Temporal Labeling for Crowdsourced
Time-Sync Videos Based on Semantic Embedding [AAAI 2016]](http://staff.ustc.edu.cn/~cheneh/paper_pdf/2016/Guangyi-Lv-AAAI.pdf)

## Contributors
Thanks for our amazing team members for contributing this project:
- [Chiao-Wen Li](https://github.com/wen830722)
- [Chung-Yi Lin](https://github.com/chungyilin)
- [Min-Yen Wu](https://github.com/Wunoodles)
- [Shu-Heng Tsao](https://github.com/signxer)
