import pyautogui, base64, time, os, sys, requests
import pytesseract
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DEEPSEEK_API_KEY

def init_ai():
    if DEEPSEEK_API_KEY == '你的DEEPSEEK_API_KEY填這裡':
        print('❌ 請先在 config.py 填入你的 DeepSeek API Key!')
        print('   申請: https://platform.deepseek.com')
        return False
    print('✅ AI 引擎啟動成功! (DeepSeek)')
    return True

def take_screenshot(save_path='screenshot.png'):
    print('📸 正在截圖...')
    pyautogui.screenshot().save(save_path)
    print(f'✅ 截圖儲存至: {save_path}')
    return save_path

def extract_text(image_path):
    """OCR 識別截圖中的文字"""
    print('🔍 正在識別畫面內容...')
    try:
        img = Image.open(image_path)
        # 先試中文+英文，如果失敗就用英文
        try:
            text = pytesseract.image_to_string(img, lang='chi_tra+eng')
        except:
            text = pytesseract.image_to_string(img, lang='eng')
        return text.strip()
    except Exception as e:
        print(f'⚠️ OCR 失敗: {e}')
        return ''

def analyze_with_ai(image_path):
    print('🤖 正在用 DeepSeek 分析戰況，請稍等...')
    
    # 用 OCR 識別文字
    ocr_text = extract_text(image_path)
    
    if ocr_text:
        context = f"以下係從 LOL 截圖識別到的文字資訊:\n{ocr_text}"
    else:
        context = "截圖 OCR 未能識別到文字，請基於一般 LOL 遊戲結構作分析。"

    prompt = f"""你係一個 League of Legends (英雄聯盟) 專業教練。

{context}

請分析上面的資訊，用繁體中文廣東話回答：

1. 📦 裝備識別
   - 我方裝備係咩？
   - 對方裝備係咩？

2. 📊 戰況分析
   - 目前雙方補兵/KDA/金錢差距
   - 邊一方有優勢？為什麼？

3. ⚔️ 傷害類型分析
   - 我方係 AD/AP/坦克？
   - 對方係 AD/AP/坦克？

4. 💡 即時建議
   - 下一件應該買咩裝備？
   - 依家應該打團？發育？推塔？
   - 有冇特別要注意嘅野？

請分點列出，用簡單易明嘅廣東話！"""

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1500
    }
    try:
        r = requests.post('https://api.deepseek.com/chat/completions',
                          headers=headers, json=payload, timeout=30)
        result = r.json()
        if 'choices' in result:
            return result['choices'][0]['message']['content']
        else:
            return f"❌ API 錯誤: {result.get('error', {}).get('message', '未知錯誤')}"
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
    print('🎮  LOL 裝備分析系統 (DeepSeek 版)')
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
            img = input('📁 圖片路徑: ').strip()
            if not os.path.exists(img):
                print(f'❌ 找不到: {img}')
                continue
        else:
            if c != 's':
                print('⏳ 3秒後截圖，請切換到 LOL!')
                for i in range(3,0,-1):
                    print(f'   {i}...')
                    time.sleep(1)
            img = take_screenshot(ss_path)
        result = analyze_with_ai(img)
        display_result(result)
        if input('💾 儲存分析嗎? (y/n): ').strip().lower() == 'y':
            save_analysis(result)

if __name__ == '__main__':
    main()
