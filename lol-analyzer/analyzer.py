"""
LOL 裝備分析系統
================
自動截圖 → 圖像識別 → AI 分析 → 即時建議
"""

import cv2
import numpy as np
import pyautogui
import pytesseract
import google.generativeai as genai
from PIL import Image
import base64
import io
import time
import os
import sys

# 載入設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import GEMINI_API_KEY

# ==========================================
# 初始化 Gemini AI
# ==========================================
def init_ai():
    if GEMINI_API_KEY == "你的API_KEY填這裡":
        print("❌ 請先在 config.py 填入你的 Gemini API Key！")
        print("   免費申請：https://aistudio.google.com/app/apikey")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ AI 引擎啟動成功！")
    return model

# ==========================================
# 截圖功能
# ==========================================
def take_screenshot(save_path="screenshot.png"):
    """截取遊戲畫面"""
    print("📸 正在截圖...")
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    print(f"✅ 截圖儲存至：{save_path}")
    return save_path

def load_image(image_path):
    """載入圖片"""
    img = Image.open(image_path)
    return img

# ==========================================
# 圖像轉 Base64 (給 AI 分析)
# ==========================================
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================
# OCR 文字識別 (識別螢幕上的文字)
# ==========================================
def extract_text_from_image(image_path):
    """從截圖中提取文字"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="chi_tra+eng")
        return text.strip()
    except Exception as e:
        print(f"⚠️  OCR 識別失敗：{e}")
        return ""

# ==========================================
# AI 分析主功能
# ==========================================
def analyze_with_ai(model, image_path):
    """用 Gemini AI 分析 LOL 截圖"""
    print("🤖 正在用 AI 分析戰況...")
    
    # 準備圖片
    img = Image.open(image_path)
    
    # 準備提示詞
    prompt = """
你係一個 League of Legends (英雄聯盟/LOL) 專業教練。
請分析呢張 LOL 遊戲截圖，用繁體中文回答以下問題：

1. 📦 **裝備識別**
   - 我方裝備係咩？
   - 對方裝備係咩？

2. 📊 **戰況分析**
   - 目前雙方補兵/KDA/金錢差距
   - 邊一方優勢？為什麼？

3. ⚔️ **傷害類型分析**
   - 我方係 AD / AP / 坦克？
   - 對方係 AD / AP / 坦克？

4. 💡 **即時建議**
   - 下一件應該買咩裝備？為什麼？
   - 依家應該打團？發育？推塔？
   - 有冇特別要注意嘅野？

請用簡單易明嘅廣東話回答，分點列出！
如果截圖唔係 LOL 畫面，請話我知。
"""
    
    try:
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"❌ AI 分析失敗：{e}"

# ==========================================
# 顯示分析結果
# ==========================================
def display_result(analysis_text):
    """美化顯示分析結果"""
    print("\n" + "="*60)
    print("🎮  LOL 戰況分析結果")
    print("="*60)
    print(analysis_text)
    print("="*60 + "\n")

# ==========================================
# 儲存分析記錄
# ==========================================
def save_analysis(analysis_text, filename=None):
    """儲存分析結果到文字檔"""
    if filename is None:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.txt"
    
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "records", filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"分析時間：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n")
        f.write(analysis_text)
    
    print(f"📝 分析結果已儲存至：{save_path}")

# ==========================================
# 主程式
# ==========================================
def main():
    print("="*60)
    print("🎮  LOL 裝備分析系統 啟動中...")
    print("="*60)
    
    # 初始化 AI
    model = init_ai()
    if model is None:
        return
    
    print("\n📋 操作說明：")
    print("  輸入 's' + Enter → 立即截圖並分析")
    print("  輸入 'f' + Enter → 分析現有圖片檔案")
    print("  輸入 'q' + Enter → 退出程式")
    print("  或直接按 Enter   → 倒數3秒後截圖")
    
    while True:
        print("\n" + "-"*40)
        choice = input("👉 請輸入指令：").strip().lower()
        
        if choice == 'q':
            print("👋 再見！GL HF！")
            break
        
        elif choice == 'f':
            # 分析現有圖片
            image_path = input("📁 請輸入圖片路徑：").strip()
            if not os.path.exists(image_path):
                print(f"❌ 找不到圖片：{image_path}")
                continue
        
        else:
            # 截圖模式
            if choice == 's':
                print("📸 準備截圖...")
            else:
                print("⏳ 3秒後截圖，請切換到 LOL 遊戲視窗！")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
            
            screenshot_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "screenshot.png"
            )
            image_path = take_screenshot(screenshot_path)
        
        # AI 分析
        analysis = analyze_with_ai(model, image_path)
        
        # 顯示結果
        display_result(analysis)
        
        # 詢問是否儲存
        save_choice = input("💾 要儲存呢次分析嗎？(y/n)：").strip().lower()
        if save_choice == 'y':
            save_analysis(analysis)

if __name__ == "__main__":
    main()
