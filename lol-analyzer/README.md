# 🎮 LOL 裝備分析系統

自動截圖 → AI 識別裝備 → 即時戰況建議

本項目有 **兩個版本**：

| 版本 | 檔案 | 適合 |
|------|------|------|
| 🖥️ 電腦版 | `analyzer.py` | Windows 電腦自動截圖 |
| 📱 網頁版 | `web/index.html` | 手機 / 平板 / 電腦，任何瀏覽器 |

---

## 📱 網頁版（推薦：任何裝置都用得）

### 最快用法
1. 下載 `web/index.html`
2. **雙擊用瀏覽器打開**（Chrome / Edge / Safari 都得）
3. 首次使用：展開「⚙️ 設定」→ 填入你嘅 Gemini API Key → 儲存
4. 點「📷 上傳圖片」→ 揀相或拍照
5. 點「🔍 開始分析」

**特點：**
- ✅ API Key 只存喺你部裝置（localStorage），唔會上傳
- ✅ 支援手機即場**拍照**
- ✅ 支援電腦 **Ctrl+V 貼上**截圖
- ✅ 自動縮圖，慳流量

### 喺手機用？三個方法
| 方法 | 做法 | 好處 |
|------|------|------|
| **A. 放上網（推薦）** | 用 GitHub Pages 免費寄存 | 任何裝置開網址就得 |
| **B. 區域網絡** | 電腦跑 `python -m http.server 8000`，手機開 `http://電腦IP:8000/web/` | 唔使上網 |
| **C. 傳檔案** | 將 index.html 傳去手機，用瀏覽器開 | 最簡單 |

---

## 📋 安裝步驟

### 第一步：安裝 Python
去 https://www.python.org/downloads/ 下載安裝

### 第二步：安裝所需工具
打開 CMD (命令提示字元)，輸入：
```
pip install opencv-python pillow pytesseract pyautogui google-generativeai
```

### 第三步：安裝 Tesseract OCR
去 https://github.com/UB-Mannheim/tesseract/wiki 下載安裝
安裝時記得勾選「中文語言包」

### 第四步：取得免費 Gemini API Key
1. 去 https://aistudio.google.com/app/apikey
2. 登入 Google 帳號
3. 點擊「Create API Key」
4. 複製你的 API Key

### 第五步：填入 API Key
打開 `config.py`，將你的 API Key 填入：
```python
GEMINI_API_KEY = "你的API_KEY填這裡"
```

---

## 🚀 使用方法

```
python analyzer.py
```

然後按照提示操作：
- 按 Enter → 倒數3秒截圖（期間切換到LOL）
- 輸入 s → 立即截圖
- 輸入 f → 分析已有圖片
- 輸入 q → 退出

---

## 💡 使用技巧

1. 在補兵/裝備頁面截圖效果最好
2. 記分板 (Tab 鍵) 打開時截圖，能看到雙方完整裝備
3. 分析結果可以選擇儲存，方便賽後複習

---

## ❓ 常見問題

**Q: 截圖是全螢幕還是只有遊戲？**
A: 全螢幕，所以截圖時要確保 LOL 是全螢幕模式

**Q: 分析需要多長時間？**
A: 通常 3-8 秒

**Q: 免費 API 有限制嗎？**
A: Gemini 免費版每分鐘15次，每天1500次，正常使用完全夠用
