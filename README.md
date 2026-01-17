# 太空捕手：星際探險 (Space Catcher: Galaxy)

這是一個刺激的太空閃避與收集遊戲。駕駛你的太空船，在星際間穿梭，收集補給包並躲避危險的星球！

## 🎮 遊戲玩法與規則 (Gameplay)

### 核心機制
*   **目標**：盡可能獲得高分！
*   **操作**：使用鍵盤方向鍵 `←` (左) 和 `→` (右) 控制太空船移動。
*   **生命值**：遊戲採 **一擊必殺 (Sudden Death)** 機制！只要撞到任何一顆星球，遊戲立即結束。

### 遊戲元素
*   **補給包 (Supplies)**：
    *   🟢 小型 (綠色)：+10 分
    *   🔵 中型 (青色)：+20 分
    *   🟡 大型 (黃色)：+30 分 (且帶有光暈效果)
*   **危險星球 (Planets)**：
    *   🔴 隨機大小與顏色的星球，邊緣帶有紅色警告光圈。
    *   ❌ **千萬不要撞到！** 撞擊會導致飛船爆炸並結束遊戲。

### 難度選擇
遊戲開始時可選擇三種難度，難度越高，飛船移動速度越快，星球數量與速度也會增加：
1.  **TRAINEE (Easy)**：新手訓練
2.  **PILOT (Normal)**：標準飛行員
3.  **COMMANDER (Hard)**：指揮官挑戰

---

## 🚀 啟動方式 (Launch Methods)

本遊戲提供兩種遊玩版本，你可以選擇最適合的方式。

### 1. Python 版本 (本機版)
經典的 Pygame 版本，擁有最穩定的效能與體驗。

**需求**：
*   Python 3.x
*   已安裝 Pygame 函式庫 (專案內附 `venv`)

**如何執行**：
1.  開啟終端機 (Terminal) 並進入專案資料夾：
    ```bash
    cd /.../space_catcher
    ```
2.  啟動虛擬環境 (如果尚未啟動)：
    ```bash
    source venv/bin/activate
    ```
3.  執行遊戲：
    ```bash
    python3 space_catcher.py
    ```

### 2. Web 版本 (網頁版)
無需安裝任何軟體(除了Python作伺服器)，直接在瀏覽器上遊玩，擁有精美的霓虹介面與粒子特效。

**如何執行**：
由於瀏覽器安全性限制，**請勿直接雙擊 html 檔案開啟**，必須透過 Local Server 執行才能正常載入圖片與音效。

1.  在終端機中，確保位於專案根目錄 (`/.../space_catcher`)。
2.  啟動 Python 內建的 HTTP 伺服器：
    ```bash
    python3 -m http.server --directory web
    ```
3.  開啟瀏覽器 (推薦 Chrome 或 Safari)，輸入網址：
    *   [http://localhost:8000](http://localhost:8000)

---

## 📂 檔案結構
*   `space_catcher.py`: Python 版遊戲主程式
*   `web/`: 網頁版相關檔案 (`index.html`, `style.css`, `game.js`)
*   `assets/`: 遊戲音效與資源
*   `venv/`: Python 虛擬環境

Enjoy your space flight! ✨
