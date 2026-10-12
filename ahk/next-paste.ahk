#Requires AutoHotkey v2.0
#SingleInstance Force
; ============================================================
;  出入口標記 — 下一個自動輸入
;  用途：你只需要撳一個熱鍵，佢就自動幫你打「下一個」地址/座標
;        落去搜尋框，然後按 Enter。唔使自己打字、唔使返 Excel 搵。
;
;  安裝：去 https://www.autohotkey.com 下載 AutoHotkey v2 並安裝
;  用法：1) 喺同一資料夾開一個 points.txt（UTF-8）
;           一行一個出入口，次序 = 你想做嘅次序
;        2) 雙擊執行本檔案
;        3) 用滑鼠點一下 system 嘅搜尋框，然後撳 Ctrl+Alt+N
;
;  熱鍵：
;    Ctrl+Alt+N  輸入下一個，並按 Enter
;    Ctrl+Alt+B  返上一個（重新輸入）
;    Ctrl+Alt+R  重設返做第 1 個
;    Ctrl+Alt+H  顯示說明
; ============================================================

; ---------- 可以改嘅設定 ----------
SendEnter   := true    ; 貼完之後自動按 Enter（如果搜尋框要 Enter 先搜）
EnterDelay  := 200     ; 貼完等幾多毫秒先按 Enter（系統慢就加大）
ShowTooltip := true    ; 喺畫面角落顯示 (3/12) 之類嘅進度
; ----------------------------------

pointsFile := A_ScriptDir "\points.txt"
points := LoadPoints()
idx := 1                      ; idx = 下一個要輸入嘅項目編號

LoadPoints() {
    global pointsFile
    if !FileExist(pointsFile)
        return []
    txt := ""
    try txt := FileRead(pointsFile, "UTF-8")
    catch
        return []
    txt := StrReplace(txt, "`r`n", "`n")
    txt := StrReplace(txt, "`r", "`n")
    out := []
    for line in StrSplit(txt, "`n") {
        line := Trim(line)
        if (line != "" && SubStr(line, 1, 1) != ";")
            out.Push(line)
    }
    return out
}

ShowTip(msg) {
    global ShowTooltip
    if (!ShowTooltip)
        return
    ToolTip msg
    SetTimer () => ToolTip(), -1600
}

SendToFocused(txt) {
    global SendEnter, EnterDelay
    SendText txt
    if (SendEnter) {
        Sleep EnterDelay
        Send "{Enter}"
    }
}

NextPoint() {
    global idx, points
    if (points.Length = 0) {
        ShowTip "搵唔到 points.txt（要同本 script 放喺同一資料夾）"
        return
    }
    if (idx > points.Length) {
        ShowTip "已經到尾（共 " points.Length " 個）"
        return
    }
    txt := points[idx]
    SendToFocused(txt)
    ShowTip "(" idx "/" points.Length ")  " txt
    idx += 1
}

PrevPoint() {
    global idx, points
    if (points.Length = 0)
        return
    cur := idx - 1                    ; 上一個已輸入嘅
    if (cur - 1 < 1) {
        ShowTip "已經係第一個"
        return
    }
    target := cur - 1
    txt := points[target]
    SendToFocused(txt)
    ShowTip "(" target "/" points.Length ")  " txt
    idx := target + 1
}

ResetPoint() {
    global idx
    idx := 1
    ShowTip "已重設到第 1 個"
}

ShowHelp() {
    global pointsFile, points
    MsgBox "
    (
    出入口標記 — 下一個自動輸入

    熱鍵：
      Ctrl+Alt+N   輸入下一個（並按 Enter）
      Ctrl+Alt+B   返上一個
      Ctrl+Alt+R   重設返做第 1 個
      Ctrl+Alt+H   呢個說明

    清單檔案：
      " pointsFile "
      已載入 " points.Length " 個項目

    用法：
      1. 用滑鼠點一下 system 嘅搜尋框（令游標喺嗰度）
      2. 撳 Ctrl+Alt+N
      3. 落點、存檔，然後再撳 Ctrl+Alt+N

    小提示：開頭以 ; 嘅行會被當成註解略過。
    )", "出入口標記助手"
}

^!n::NextPoint()
^!b::PrevPoint()
^!r::ResetPoint()
^!h::ShowHelp()

; 開機提示
if (points.Length = 0)
    ShowTip "未載入到 points.txt —— 撳 Ctrl+Alt+H 睇說明"
else
    ShowTip "已載入 " points.Length " 個項目，撳 Ctrl+Alt+N 開始"
