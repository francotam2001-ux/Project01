"""
LOL 裝備分析系統
================
自動截圖 → 圖像識別 → AI 分析 → 即時建議
使用 Groq API (免費，香港可用)
"""

import pyautogui
import base64
import time
import os
import sys
import requests
from PIL import Image

# 載入設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import GROQ_API_KEY

# ==========================================
# 初始化 Groq AI
# ==========================================
def init_ai():
    if GROQ_API_KEY == '你的GROQ_API_KEY填這裡':
        print('❌ 請先在 config.py 填入你的 Groq API Key！')
        print('   免費申請：https://console.groq.com')
        return False
    print('✅ AI 引擎啟動成功！(Groq - 免費版)')
    return True

# ==========================================
# 截圖功能
# ==========================================
def take_screenshot(save_path='screenshot.png'):
    print('📸 正在截圖...')
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    print(f'✅ 截圖儲存至：{save_path}')
    return save_path

# ==========================================
# 圖片轉 Base64
# ==========================================
def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# ==========================================
# AI 分析主功能 (使用 Groq)
# ==========================================
def analyze_with_ai(image_path):
    print('🤖 正在用 AI 分析戰況，請稍等...')
    image_data = image_to_base64(image_path)
    prompt = '''你係一個 League of Legends (英雄聯盟/LOL) 專業教練。
請分析呢張 LOL 遊戲截圖，用繁體中文廣東話回答：

1. 📦 裝備識別
   - 我方裝備係咩？
   - 對方裝備係咩？

2. 📊 戰況分析
   - 目前雙方補兵/KDA/金錢差距
   - 邊一方有優勢？為什麼？

3. ⚔️ 傷害類型分析
   - 我方係 AD / AP / 坦克？
   - 對方係 AD / AP / 坦克？

4. 💡 即時建議
   - 下一件應該買咩裝備？
   - 依家應該打團？發育？推塔？
   - 有冇特別要注意嘅野？

請分點列出，用簡單易明嘅廣東話！
如果截圖唔係 LOL 畫面，請話我知。'''

    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/png;base64,{image_data}'}
                    },
                    {'type': 'text', 'text': prompt}
                ]
            }
        ],
        'max_tokens': 1500
    }
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        result = response.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            return f"❌ API 錯誤：{result.get('error', {}).get('message', '未知錯誤')}"
    except Exception as e:
        return f'❌ 連線失敗：{e}'

# ==========================================
# 顯示分析結果
# ==========================================
def display_result(analysis_text):
    print('\n' + '='*60)
    print('🎮  LOL 戰況分析結果')
    print('='*60)
    print(analysis_text)
    print('='*60 + '\n')

# ==========================================
# 儲存分析記錄
# ==========================================
def save_analysis(analysis_text):
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    records_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records')
    os.makedirs(records_dir, exist_ok=True)
    save_path = os.path.join(records_dir, f'analysis_{timestamp}.txt')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(f"分析時間：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write('='*60 + '\n')
        f.write(analysis_text)
    print(f'📝 分析結果已儲存至：{save_path}')

# ==========================================
# 主程式
# ==========================================
def main():
    print('='*60)
    print('🎮  LOL 裝備分析系統 啟動中...')
    print('='*60)
    if not init_ai():
        return
    print('\n📋 操作說明：')
    print('  直接按 Enter   → 倒數3秒後截圖並分析')
    print('  輸入 s         → 立即截圖並分析')
    print('  輸入 f         → 輸入圖片路徑分析')
    print('  輸入 q         → 退出程式')
    screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshot.png')
    while True:
        print('\n' + '-'*40)
        choice = input('👉 請輸入指令：').strip().lower()
        if choice == 'q':
            print('👋 再見！GL HF！')
            break
        elif choice == 'f':
            image_path = input('📁 請輸入圖片路徑：').strip()
            if not os.path.exists(image_path):
                print(f'❌ 找不到圖片：{image_path}')
                continue
        else:
            if choice != 's':
                print('⏳ 3秒後截圖，請立即切換到 LOL 遊戲視窗！')
                for i in range(3, 0, -1):
                    print(f'   {i}...')
                    time.sleep(1)
            image_path = take_screenshot(screenshot_path)
        analysis = analyze_with_ai(image_path)
        display_result(analysis)
        save_choice = input('💾 要儲存呢次分析嗎？(y/n)：').strip().lower()
        if save_choice == 'y':
            save_analysis(analysis)

if __name__ == '__main__':
    main()
