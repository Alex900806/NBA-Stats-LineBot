# NBA Stats + LineBot

因為自己有在玩 NBA Fantasy Basketball，所以會有需要每天查詢當日表現較好球員的需求，因此我就思考或許能「自動化」這件事，降低自己手動查詢的時間，也透過和 LineBot 串接來提升可用性。

## 功能

- 可以自動化推薦當日表現較好的球員
- 可以依照自己的喜好來排序球員順序
- 可以透過輸入「聯盟戰績」來查看即時的戰績資料
- 可以查看球員的投籃熱度圖片

## 使用技術

Python, LineBot, Heroku

## 學習成果

- 學習使用 Python(Pandas) 來進行數據分析，將需要的資訊歸納出來
- 學習使用 Python(Matplotlib) 來進行數據的可視化
- 學習將此專案部署在 Heroku，以持續運作此專案
- 學習將專案想法和 LineBot 結合

## 實際頁面

- 加入我吧！ @458lcjbg

## 球員投籃熱度圖片（範例）

![image](https://github.com/Alex900806/NBA-Stats-LineBot/blob/main/shot_data/Kawhi_Leonard_shot_chart.png)

## 版本更新目錄

- Version 1.0：正式上線
- Version 1.1：解決 Line Token Hidden 問題
- Version 1.2：新增「聯盟戰績」功能
- Version 1.3：測試「球員投籃熱度圖片」功能（未來將持續開發客製化球員功能，目前只能顯示 Stephen Curry 的圖片）

## 檢討部分

- 過多的 commit history，應嘗試使用像是 ngrok 來進行本機測試
