"""
LOL 即時數據分析器 (Live Client Data + Gemini)
================================================
唔使截圖、唔使登入帳號！
直接讀取 LOL 本機即時數據 → 交俾 Gemini 分析

需要：① 遊戲進行中  ② 喺打機嗰部電腦運行
"""
import requests, json, time, os, sys, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import GEMINI_API_KEY, GEMINI_MODEL

LIVE_URL = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')


def init_ai():
    if GEMINI_API_KEY == '你的GEMINI_API_KEY填這裡':
        print('❌ 請先在 config.py 填入你的 Gemini API Key!')
        return False
    print(f'✅ AI 引擎啟動! (Gemini - {GEMINI_MODEL})')
    return True


# ---------- 下載裝備 / 英雄中文名 (會快取) ----------
def _cache_path(name):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, name)


def load_ddragon():
    item_file = _cache_path('items_zh_TW.json')
    champ_file = _cache_path('champions_zh_TW.json')

    if os.path.exists(item_file) and os.path.exists(champ_file):
        try:
            item_map = json.load(open(item_file, encoding='utf-8'))
            champ_map = json.load(open(champ_file, encoding='utf-8'))
            print(f'✅ 已載入中文名稱 (裝備 {len(item_map)} 件 / 英雄 {len(champ_map)} 個)')
            return item_map, champ_map
        except Exception:
            pass

    item_map, champ_map = {}, {}
    try:
        ver = requests.get('https://ddragon.leagueoflegends.com/api/versions.json', timeout=10).json()[0]
        it = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{ver}/data/zh_TW/item.json', timeout=20).json()
        for iid, info in it['data'].items():
            item_map[iid] = info['name']
        ch = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{ver}/data/zh_TW/champion.json', timeout=20).json()
        for key, info in ch['data'].items():
            champ_map[key] = info['name']
        json.dump(item_map, open(item_file, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump(champ_map, open(champ_file, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f'✅ 已下載中文名稱 (版本 {ver})')
    except Exception as e:
        print(f'⚠️  下載中文名稱失敗: {e}')
    return item_map, champ_map


# ---------- 讀取即時遊戲數據 ----------
def fetch_live():
    try:
        r = requests.get(LIVE_URL, verify=False, timeout=5)
        return r.json()
    except Exception:
        return None


def item_names(items, item_map):
    names = []
    for it in items:
        iid = str(it.get('itemID', 0))
        if iid == '0':
            continue
        name = item_map.get(iid) or it.get('displayName') or f'裝備{iid}'
        cnt = it.get('count', 1)
        names.append(name + (f' x{cnt}' if cnt > 1 else ''))
    return names


def build_summary(data, item_map, champ_map):
    gd = data.get('gameData', {})
    players = data.get('allPlayers', [])
    active = data.get('activePlayer', {})
    my_name = active.get('summonerName', '')

    my_team = None
    for p in players:
        if p.get('summonerName') == my_name:
            my_team = p.get('team')

    allies, enemies = [], []
    for p in players:
        (allies if p.get('team') == my_team else enemies).append(p)

    def fmt(plist):
        lines = []
        for p in plist:
            key = p.get('championName', '?')
            champ = champ_map.get(key, key)
            s = p.get('scores', {})
            items = item_names(p.get('items', []), item_map)
            items_txt = '、'.join(items) if items else '(無裝備)'
            lines.append(
                f"  • {champ}（{p.get('summonerName','?')}）Lv{p.get('level','?')} "
                f"KDA {s.get('kills',0)}/{s.get('deaths',0)}/{s.get('assists',0)} "
                f"補兵 {s.get('creepScore',0)}\n    裝備：{items_txt}"
            )
        return '\n'.join(lines)

    gt = gd.get('gameTime', 0)
    minutes, seconds = int(gt // 60), int(gt % 60)
    my_champ = champ_map.get(active.get('championName', ''), active.get('championName', ''))

    return (
        f"遊戲模式：{gd.get('gameMode','?')}\n"
        f"遊戲時間：{minutes}分{seconds}秒\n"
        f"你嘅英雄：{my_champ}\n\n"
        f"【我方隊伍】\n{fmt(allies)}\n\n"
        f"【敵方隊伍】\n{fmt(enemies)}\n"
    )


def ask_gemini(summary):
    prompt = (
        '你係一個 League of Legends 專業教練。以下係一場進行中嘅遊戲即時數據：\n\n'
        + summary +
        '\n請用繁體中文廣東話分析：\n'
        '1. 📊 戰況分析：邊一方優勢？為什麼？\n'
        '2. ⚔️ 雙方係 AD / AP / 坦克 嘅比例？\n'
        '3. 💡 即時建議：我下一件買咩？而家應該打團 / 發育 / 推塔？有咩危險？\n'
        '4. 🎯 針對敵方裝備，我有咩要注意？\n'
        '請簡短、分點、實際。'
    )
    url = (f'https://generativelanguage.googleapis.com/v1beta/models/'
           f'{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}')
    payload = {'contents': [{'parts': [{'text': prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=60)
        res = r.json()
        if 'candidates' in res:
            return res['candidates'][0]['content']['parts'][0]['text']
        return '❌ API 錯誤: ' + str(res.get('error', {}).get('message', '未知錯誤'))
    except Exception as e:
        return f'❌ 連線失敗: {e}'


# ---------- 主程式 ----------
def wait_for_game():
    print('⏳ 等待進入遊戲...（請喺 LOL 開一場）')
    while True:
        data = fetch_live()
        if data:
            print('\n✅ 偵測到遊戲進行中！')
            return data
        time.sleep(5)
        sys.stdout.write('.')
        sys.stdout.flush()


def analyze_once(item_map, champ_map):
    data = fetch_live()
    if not data:
        print('❌ 未偵測到遊戲數據。請確認：')
        print('   ① 遊戲進行中（唔係選角/大廳）')
        print('   ② 喺打機嗰部電腦運行')
        return
    summary = build_summary(data, item_map, champ_map)
    print('\n📋 讀取到嘅即時數據：')
    print('-' * 60)
    print(summary)
    print('-' * 60)
    print('🤖 Gemini 分析中...')
    print('\n' + '=' * 60)
    print(ask_gemini(summary))
    print('=' * 60)


def main():
    print('=' * 60)
    print('🎮  LOL 即時數據分析器 (Live Client Data + Gemini)')
    print('=' * 60)
    if not init_ai():
        return
    print('📥 載入裝備/英雄中文名稱...')
    item_map, champ_map = load_ddragon()

    while True:
        print('\n' + '-' * 40)
        print('  1 → 等入 game 後自動分析')
        print('  2 → 分析一次（現在）')
        print('  3 → 自動模式（每隔 N 秒分析）')
        print('  q → 退出')
        c = input('👉 請選擇: ').strip().lower()

        if c == 'q':
            print('👋 再見! GL HF!')
            break

        if c == '1':
            wait_for_game()
            analyze_once(item_map, champ_map)
            continue

        if c == '3':
            try:
                n = int(input('每隔幾秒分析一次？(建議 60): ').strip() or '60')
            except ValueError:
                n = 60
            print(f'🔁 自動模式啟動，每 {n} 秒分析一次。按 Ctrl+C 停止。')
            try:
                while True:
                    data = fetch_live()
                    if data:
                        summary = build_summary(data, item_map, champ_map)
                        print('\n' + '=' * 60)
                        print(f'⏱️  {time.strftime("%H:%M:%S")}')
                        print('=' * 60)
                        print(ask_gemini(summary))
                    else:
                        print('⚠️  未偵測到遊戲（可能已結束）')
                    time.sleep(n)
            except KeyboardInterrupt:
                print('\n⏹️  已停止自動模式')
            continue

        analyze_once(item_map, champ_map)


if __name__ == '__main__':
    main()
