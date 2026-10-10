"""
LOL 裝備分析系統 (Gemini 版)
================================
自動截圖 → Gemini 視覺識別 → AI 分析 → 即時建議
Gemini 識睇圖，所以直接認到裝備圖標！
"""

import pyautogui
import base64, time, os, sys, requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import GEMINI_API_KEY, GEMINI_MODEL


def init_ai():
    if GEMINI_API_KEY == '你的GEMINI_API_KEY填這裡':
        print('❌ 請先在 config.py 填入你的 Gemini API Key!')
        print('   申請: https://aistudio.google.com/app/apikey')
        return False
    print(f'✅ AI 引擎啟動成功! (Gemini - {GEMINI_MODEL})')
    return True


def take_screenshot(save_path='screenshot.png'):
    print('📸 正在截圖...')
    pyautogui.screenshot().save(save_path)
    print(f'✅ 截圖儲存至: {save_path}')
    return save_path


def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def analyze_with_ai(image_path):
    print('🤖 正在用 Gemini 分析戰況，請稍等...')

    image_data = image_to_base64(image_path)

    prompt = '''你係一個 League of Legends (英雄聯盟) 專業教練。
請仔細睇呢張 LOL 遊戲截圖，用繁體中文廣東話回答：

1. 📦 裝備識別
   - 我方每個英雄嘅裝備係咩？
   - 對方每個英雄嘅裝備係咩？

2. 📊 戰況分析
   - 目前雙方補兵 / KDA / 經濟差距
   - 邊一方有優勢？為什麼？

3. ⚔️ 傷害類型分析
   - 我方主要係 AD / AP / 坦克？
   - 對方主要係 AD / AP / 坦克？

4. 💡 即時建議
   - 下一件應該買咩裝備？為什麼？
   - 依家應該打團？發育？推塔？
   - 有冇特別要注意嘅危險？

請分點列出，用簡單易明嘅廣東話！
如果截圖唔係 LOL 遊戲畫面，請直接話我知。'''

    url = (f'https://generativelanguage.googleapis.com/v1beta/models/'
           f'{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}')

    payload = {
        'contents': [{
            'parts': [
                {'text': prompt},
                {'inline_data': {'mime_type': 'image/png', 'data': image_data}}
            ]
        }]
    }

    try:
        r = requests.post(url, json=payload, timeout=60)
        result = r.json()

        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            err = result.get('error', {}).get('message', '未知錯誤')
            return f'❌ API 錯誤: {err}\n\n(提示: 如果話模型唔存在, 試下改 config.py 嘅 GEMINI_MODEL)'
    except Exception as e:
        return f'❌ 連線失敗: {e}'


def display_result(text):
    print('\n' + '='*60)
    print('🎮  LOL 戰況分析結果')
    print('='*60)
    print(text)
    print('='*60 + '\n')


def save_analysis(text):
    ts = time.strftime('%Y%m%d_%H%M%S')
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'records')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f'analysis_{ts}.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"分析時間: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*60}\n{text}")
    print(f'📝 儲存至: {path}')


def main():
    print('='*60)
    print('🎮  LOL 裝備分析系統 (Gemini 版)')
    print('='*60)
    if not init_ai():
        return
    print('\n📋 操作說明:')
    print('  Enter → 倒數3秒後截圖分析')
    print('  s     → 立即截圖分析')
    print('  f     → 分析圖片檔')
    print('  q     → 退出')
    ss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshot.png')
    while True:
        print('\n' + '-'*40)
        c = input('👉 請輸入指令: ').strip().lower()
        if c == 'q':
            print('👋 再見! GL HF!')
            break
        elif c == 'f':
            img = input('📁 圖片路徑: ').strip().strip('"')
            if not os.path.exists(img):
                print(f'❌ 找不到: {img}')
                continue
        else:
            if c != 's':
                print('⏳ 3秒後截圖，請切換到 LOL!')
                for i in range(3, 0, -1):
                    print(f'   {i}...')
                    time.sleep(1)
            img = take_screenshot(ss_path)
        result = analyze_with_ai(img)
        display_result(result)
        if input('💾 儲存分析嗎? (y/n): ').strip().lower() == 'y':
            save_analysis(result)


if __name__ == '__main__':
    main()
