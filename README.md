# 🕷️ Assignment 01：動態網頁爬蟲實作 - Mangaz 漫畫圖書館

## 📖 專案簡介

本專案是 Python 網路爬蟲課程作業，使用 Selenium 模擬瀏覽器操作，進入 Mangaz 漫畫圖書館指定漫畫頁面，點擊免費閱讀入口，切換閱讀視窗後自動翻頁，並將漫畫頁面截圖儲存到本機資料夾。

目標網站：

https://www.mangaz.com/book/detail/157901

## ✨ 專案功能

- 🌐 使用 Selenium 開啟 Chrome 瀏覽器
- 📚 自動進入 Mangaz 指定漫畫頁面
- 🖱️ 點擊免費閱讀按鈕
- 🪟 切換到新開啟的閱讀視窗
- 🚀 點擊「すぐに読む」進入閱讀器
- 🖼️ 自動擷取目前顯示的漫畫圖片
- 🔁 自動點擊下一頁並重複截圖
- 📁 將圖片儲存到 `downloaded_manga` 資料夾
- ✅ 爬取完成後自動關閉 WebDriver

## 📂 專案結構

```text
AIPE03_PythonWebScraping作業_42_吳哲安/
│
├── assignment01_scraper.py
├── Assignment01_動態爬蟲案例_mangaz_練習版.ipynb
├── ReadMe_by_Teacher.md
├── README.md
├── project_gutenberg/
└── downloaded_manga/
```

## 🧰 環境需求

- 🐍 Python 3
- 🌐 Google Chrome
- 🧪 Selenium
- ⚙️ ChromeDriver 或 Selenium Manager 支援的 Chrome 環境

## 📦 安裝套件

如果尚未安裝 Selenium，請執行：

```bash
pip install selenium
```

如果有 `requirements.txt`，也可以使用：

```bash
pip install -r requirements.txt
```

## ▶️ 執行方式

在專案資料夾中執行：

```bash
python assignment01_scraper.py
```

也可以指定輸出資料夾：

```bash
python assignment01_scraper.py --output-dir downloaded_manga
```

或指定目標網址：

```bash
python assignment01_scraper.py --url https://www.mangaz.com/book/detail/157901
```

## 🖼️ 輸出結果

程式執行後，會自動建立 `downloaded_manga` 資料夾，並將截圖後的漫畫頁面依序儲存，例如：

```text
downloaded_manga/
├── manga_page_000.png
├── manga_page_001.png
├── manga_page_002.png
└── ...
```

## 🔄 程式流程

1. 建立 Chrome WebDriver 與瀏覽器設定
2. 開啟 Mangaz 指定漫畫頁面
3. 等待並點擊免費閱讀按鈕
4. 切換到新開啟的閱讀視窗
5. 點擊「すぐに読む」進入閱讀器
6. 使用 CSS Selector 找到漫畫圖片元素
7. 對可見圖片進行截圖並儲存
8. 點擊下一頁繼續擷取
9. 找不到下一頁時結束程式
10. 關閉 WebDriver

## 🛠️ 使用技術

- 🐍 Python
- 🌐 Selenium WebDriver
- ⏳ WebDriverWait
- ✅ Expected Conditions
- 🎯 CSS Selector
- 🔗 PARTIAL_LINK_TEXT
- 📁 pathlib

## ⚠️ 注意事項

本專案僅作為課程作業與學習 Selenium 動態爬蟲技術使用。請遵守網站規範與著作權相關規定，不得將下載內容用於非法散布或商業用途。

## 🏆 作業成果

- GitHub Repository：https://github.com/wuchean1004/AIPE03-PythonWebScraping-Homework
- 執行成果影片：https://reurl.cc/A9WeNQ
