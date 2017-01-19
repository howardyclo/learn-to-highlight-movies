# 資料前處理

這個資料夾的程式會將 `../data/` 資料夾中每一部電影的彈幕做前處理：

如果你有要使用自己的電影彈幕資料的話，就要將資料準備好，格式要按照 `../data/<movie_name>.json` 與對應標註資料 `../label/<movie_name>.txt`，並執行這邊的程式。

## 如何跑程式
我們利用 `npm (nodejs package manager)` 來自動化整個資料處理的 pipeline，因此你需要先安裝好 `nodejs` 與 `npm`。本程式使用 `node v6.2.2` 與 `npm 3.9.5` 版本，同常在安裝新版的 `nodejs` 會連同 `npm` 一起幫你安裝好。

安裝好之後，請在終端機輸入 `npm install`，它會幫你安裝好 `preprocess.js` 需要的 dependencies。

在 `package.json` 中可以自定義 `npm` 指令，`npm` 可以自行定義簡單的指令，取代一大串指令，讓我能夠節省在終端機手動輸入參數的時間，例如，如果有十部電影要處理，就要手動執行十次，但是如果使用 `npm`，你只要在終端機輸入 `npm start`，就會依序執行 `preprocess.js`, `split.py`, `merge.py`，把所有放在`../data/<movie_name>.json` 及其對應的 `../label/<movie_name>.txt` 都處理好。

註：如果有新電影的彈幕 `<movie_name>.json` 放到 `../data/` 中，請在 `package.json` 中的 `preprocess` 指令後面累加 `&& node preprocess.js -f <movie_name>.json`。
