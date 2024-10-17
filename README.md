# NBA Stats + LineBot

鑑於 Fantasy Basketball 需要每天查詢當日表現較好球員的需求，我決定「自動化」這個過程，減少手動查詢的時間，也透過和 LineBot 串接來提升可用性。

## 功能

- 可以自動化推薦當日表現較好的球員
- 可以依照自己的喜好來排序球員順序
- 可以透過輸入「聯盟戰績」來查看即時的戰績資料
- 可以查看球員的投籃熱度圖片

## 使用技術

Python, Pandas, Matplotlib, LineBot

## 學習成果

- 學習使用 Python(Pandas) 來進行數據分析，將需要的資訊歸納出來
- 學習使用 Python(Matplotlib) 來進行數據的可視化
- 學習將專案部署到 Render，使其持續運作、自動更新數據
- 學習將專案想法邏輯和 LineBot 結合，提升可用性

## 實際頁面

- 加入我吧！ @458lcjbg（目前為免費方案，可能有使用限制）

## 球員投籃熱度圖片（範例）

![image](https://github.com/Alex900806/NBA-Stats-LineBot/blob/main/demo/Kawhi_Leonard_shot_chart_demo.png)

## 版本更新目錄

- Version 1.0：正式上線
- Version 1.1：解決 Line Token Hidden 問題
- Version 1.2：新增「聯盟戰績」功能
- Version 1.3：測試「球員投籃熱度圖片」功能（未來將持續開發客製化球員功能）
- Version 2.0：本專案進行重構，將核心功能與工具區分，去除重複程式碼
- Version 2.1：將專案從 Heroku 轉移至 Render，並整理程式碼
- Version 2.2：導入 Loading Animation 功能，最久持續 60 秒
- Version 2.3：新增客製化「球員投籃熱度圖片」功能（輸入投籃圖「球員名稱」），新增 Log 用於紀錄執行過程

## 檢討部分

- 過多的 commit history，應嘗試使用像是 ngrok 來進行本機測試
