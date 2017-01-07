# 資料前處理

這個資料夾的程式會將 `../data/` 資料夾中中每一部電影的彈幕做前處理：

如果你有要使用自己的電影彈幕資料的話，就要將資料準備好，格式要按照 `../data/<movie_name>.json` 與對應標註資料 `../label/<movie_name>.json`，並執行這邊的程式。

## 程式說明

### `preprocess.js`
負責以下資料前處理的任務：
- 刪除彈幕不需要的資料欄位。
- 根據每一部電影在 `../label/` 資料夾中對應的經典橋段時間的標籤資料，來標註彈幕，例如，如果某一時間的彈幕出現在經典橋段的時間內，就將該彈幕的資料欄位 `class` 標註為 `POS`，不是則 `NEG`。
- 為了之後訓練詞向量，因此也需要先使用 [jieba](https://github.com/fxsjy/jieba) 對每個彈幕的內容做斷詞、擷取關鍵詞，為了刪掉高頻率又沒有意義的詞，我們只保留關鍵詞的部分當作斷詞的結果，但是要保留詞出現在彈幕內容的次序。
- 標準化 `23333`, `66666`, `哈哈哈哈哈` 等這些同義但是不同長度的詞，我們把它們全部標準化成一個字 `哈`。
- 最後存入 `processed-data/<movie_name>.json`。

### `split.py`
負責把某部電影經過 `preprocess.js` 處理好的彈幕，也就是 `processed-data/<movie_name>.json`，依照指定的時間間隔（30秒）切割為數個片段，將每個片段中的所有彈幕串成同一列（視為一個 document），片段中若包含任一條 `class` 為 `POS` 的彈幕，則將其寫入 `processed-data/<movie_name>_POS.txt`，反之則寫入 `processed-data/<movie_name>_NEG.txt`。

### `merge.py`
負責將資料處理成訓練詞向量與機器學習模型所需的輸入格式，將所有 `<movie_name>_<label>.txt` 順序打亂後，寫進 `all_POS.txt`, `all_NEG.txt`, `train_POS.txt`, `train_POS.txt`, `test_POS.txt`, `test_POS.txt`。除此之外，還將低頻詞都標準化成 `UNK`，以提升詞向量的品質。

## 如何跑程式
我們利用 `npm (nodejs package manager)` 來自動化整個資料處理的 pipeline，因此你需要先安裝好 `nodejs` 與 `npm`。本程式使用 `node v6.2.2` 與 `npm 3.9.5` 版本，同常在安裝新版的 `nodejs` 會連同 `npm` 一起幫你安裝好。

安裝好之後，請在終端機輸入 `npm install`，它會幫你安裝好 `preprocess.js` 需要的 dependencies。

在 `package.json` 中可以自定義 `npm` 指令，`npm` 可以自行定義簡單的指令，取代一大串指令，讓我能夠節省在終端機手動輸入參數的時間，例如，如果有十部電影要處理，就要手動執行十次，但是如果使用 `npm`，你只要在終端機輸入 `npm start`，就會依序執行 `preprocess.js`, `split.py`, `merge.py`，把所有放在`../data/<movie_name>.json` 及其對應的 `../label/<movie_name>.txt` 都處理好。

註：如果有新電影的彈幕 `<movie_name>.json` 放到 `../data/` 中，請在 `package.json` 中的 `preprocess` 指令後面累加 `&& node preprocess.js -f <movie_name>.json`。
