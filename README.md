# 超音波模組配合影像偵測輔助光敏自走車

[![Demo Video](https://img.shields.io/badge/YouTube-Demo-red)](https://www.youtube.com/watch?v=3oqjmjdaAJs)

一個結合超音波測距、OpenCV 影像辨識與光敏電阻感測器的智慧型自走車系統，能夠自主循線、避障並辨識交通號誌。

## 📑 目錄

- [專題簡介](#-專題簡介)
- [主要功能](#-主要功能)
- [硬體需求](#-硬體需求)
- [軟體環境設置](#-軟體環境設置)
- [使用方法](#-使用方法)
- [專案結構](#-專案結構)
- [執行流程](#-執行流程)
- [調整參數](#-調整參數)
- [實驗結果](#-實驗結果)
- [注意事項](#️-注意事項)
- [未來改進方向](#-未來改進方向)
- [開發團隊與心得](#-開發團隊與心得)
- [參考資源](#-參考資源)

## 📋 專題簡介

本專題開發了一台具有多重感知能力的自走車,透過整合三種不同的感測技術,模擬真實世界中自動駕駛車輛的基本功能：

- **循線行駛**：使用雙光敏電阻追蹤黑色跑道
- **障礙物偵測**：透過超音波模組即時測距，遇到障礙物時自動停車並發出警報
- **交通號誌辨識**：運用 OpenCV 影像處理技術辨識紅燈，自動停車遵守交通規則

## ✨ 主要功能

### 1. 智慧循線系統
- 使用左右雙光敏電阻偵測道路邊界
- 自動判斷車體位置並進行方向修正
- 支援直角轉彎與小幅度轉彎
- 臨界值設定：左側 33、右側 43（可依環境調整）

**工作原理**：
- 兩側電阻值都在範圍內 → 直行
- 左側電阻值超過臨界值 → 右轉修正
- 右側電阻值超過臨界值 → 左轉修正
- 兩側電阻值都超過臨界值 → 執行大角度左轉後右側微調

### 2. 超音波避障系統
- 即時監測前方障礙物距離（有效範圍：8-10cm）
- 偵測到障礙物時立即停車
- 蜂鳴器警報功能（頻率：523Hz）
- 模擬行人突然出現或交通事故情境

### 3. 影像辨識系統
- 使用 OpenCV 進行即時影像處理
- 可辨識紅、藍、綠、黃四種顏色
- 專注於紅色物體辨識（模擬紅燈）
- 偵測到紅燈時自動停車

## 🛠 硬體需求

### 核心元件
- Raspberry Pi（主控板）
- HC-SR04 超音波測距模組
- USB 網路攝影機（支援 OpenCV）
- PCF8591 類比數位轉換器
- 光敏電阻 × 2
- 蜂鳴器
- 直流馬達 × 2
- L298N 馬達驅動模組
- 車體底盤
- 電源供應系統

### 接線說明

**超音波模組（HC-SR04）**
```
VCC  → 5V
GND  → GND
TRIG → GPIO 12 (BOARD)
ECHO → GPIO 15 (BOARD)
```

**馬達驅動（L298N）**
```
右馬達:
  IN1 → GPIO 16 (BOARD)
  IN2 → GPIO 18 (BOARD)
左馬達:
  IN3 → GPIO 11 (BOARD)
  IN4 → GPIO 13 (BOARD)
```

**蜂鳴器**
```
Signal → GPIO 22 (BOARD)
GND    → GND
```

**光敏電阻（透過 PCF8591）**
```
PCF8591 I2C Address: 0x48
AIN0 → 右側光敏電阻
AIN1 → 左側光敏電阻
```

### 硬體電路圖
![image](https://github.com/jasontsai890918/Ultrasonic_and_Vision_Assisted_Autonomous_Car/blob/main/Circuit_Diagram.png)

## 💻 軟體環境設置

### 系統需求
- Raspberry Pi OS (Raspbian)
- Python 3.x
- OpenCV 4.x

### 安裝步驟

1. **更新系統**
```bash
sudo apt-get update
sudo apt-get upgrade
```

2. **安裝必要套件**
```bash
# 安裝 OpenCV
sudo apt-get install python3-opencv

# 安裝 GPIO 相關套件
sudo apt-get install python3-rpi.gpio

# 安裝 I2C 工具
sudo apt-get install python3-smbus i2c-tools
```

3. **啟用 I2C 和攝影機**
```bash
sudo raspi-config
# 選擇 Interface Options
# 啟用 I2C 和 Camera
```

4. **驗證 I2C 設備**
```bash
sudo i2cdetect -y 1
# 應該會看到 0x48 (PCF8591)
```

## 🚀 使用方法

### 1. 準備實驗環境
- 準備白色塑膠板作為底板
- 使用黑色奇異筆繪製跑道（模擬柏油路）
- 確保光線充足且均勻

### 2. 執行程式
```bash
cd /path/to/project
python3 Two_Light_Move.py
```

### 3. 停止程式
- 按下 `Ctrl+C` 優雅地停止程式
- 系統會自動清理 GPIO 設定

## 📁 專案結構

```
.
├── Two_Light_Move.py      # 主程式（整合所有模組）
├── Moving_motor.py        # 馬達控制模組
├── audio.py               # 超音波與蜂鳴器控制
├── detect_red.py          # OpenCV 影像辨識模組
└── README.md              # 專案說明文件
```

### 模組說明

**Two_Light_Move.py** - 主控制程式
- 整合所有感測器與控制模組
- 實現主要邏輯判斷
- 協調各模組運作

**Moving_motor.py** - 馬達控制
- `forward()` - 前進
- `backward()` - 後退
- `turnLeft()` - 左轉
- `turnRight()` - 右轉
- `onlyleft()` - 原地左旋轉
- `onlyright()` - 原地右旋轉
- `stop()` - 停止
- `cleanup()` - 清理 GPIO

**audio.py** - 超音波與聲音控制
- `get_distance()` - 取得距離（cm）
- `play(pitch)` - 播放指定頻率
- `set()` - 初始化 PWM
- `stop()` - 停止播放

**detect_red.py** - 影像辨識
- `get_red()` - 偵測紅色物體
- 支援紅、藍、綠、黃四色 HSV 閾值設定
- 高斯模糊與中值濾波處理

## 🎯 執行流程

```
開始
  ↓
初始化感測器
  ↓
讀取光敏電阻值 ←─────┐
  ↓                   │
判斷車體位置           │
  ↓                   │
執行對應動作           │
(直行/左轉/右轉)       │
  ↓                   │
超音波偵測 ──→ 距離<15cm? ─→ 是 ─→ 停止並警報
  ↓ 否                │
影像辨識 ──→ 偵測到紅燈? ─→ 是 ─→ 停止
  ↓ 否                │
繼續循環 ─────────────┘
```

## 🔧 調整參數

### 光敏電阻臨界值（Two_Light_Move.py）
```python
L_monitor = 33  # 左側光敏電阻臨界值
R_monitor = 43  # 右側光敏電阻臨界值
```
- 數值越高，對白色越敏感
- 建議依實際環境光線調整

### 超音波偵測距離（Two_Light_Move.py）
```python
if(aud.get_distance() > 15):  # 15cm 為安全距離
```

### 馬達速度（Moving_motor.py）
```python
dc = 100  # 占空比 (0-100)
```

### 顏色辨識閾值（detect_red.py）
```python
red_lower = np.array([0,43,46])
red_upper = np.array([10,255,255])
```

## 📊 實驗結果

透過以上改進，專題達成以下成果：
- ✅ 成功實現循線功能，可完成包含直角轉彎的複雜路線
- ✅ 超音波避障反應靈敏，可在 15cm 內停車
- ✅ 影像辨識準確率高，可正確辨識紅色物體
- ✅ 系統整合良好，三大功能協同運作順暢

觀看完整實驗過程：[YouTube 影片連結](https://www.youtube.com/watch?v=3oqjmjdaAJs)

## ⚠️ 注意事項

1. **電源供應**：確保電池電量充足，電壓不穩會影響馬達性能
2. **環境光線**：保持實驗環境光線穩定，避免光敏電阻誤判
3. **攝影機角度**：確保攝影機視野覆蓋前方道路
4. **底板清潔**：保持塑膠板清潔，避免灰塵影響光敏電阻
5. **GPIO 清理**：程式結束後務必執行 cleanup() 避免 GPIO 警告

## 🔮 未來改進方向

- [ ] 加入 PID 控制器提升循線穩定性
- [ ] 實現更多交通號誌辨識（綠燈、黃燈）
- [ ] 增加速度控制，依路況自動調整
- [ ] 加入藍牙遙控功能
- [ ] 優化電池續航力
- [ ] 實現路徑記憶與重現

## 👥 開發團隊與心得

| 成員 | 學號 | 負責項目 |
|------|------|----------|
| 陳九龍 | 1080721 | 程式架構設計與參數調整 |
| 蔡宗儒 | 1080730 | 硬體電路實作 |
| 葉庭嘉 | 1080741 | 程式撰寫與硬體電路協助 |

### 主要挑戰與解決方案

1. **單一光敏電阻精準度不足**
   - 問題：無法精確判斷轉向方向
   - 解決：改用雙光敏電阻系統，分別偵測左右邊界

2. **後輪方向不穩定**
   - 問題：後輪轉動導致每次轉彎結果不一致
   - 解決：使用膠帶固定後輪方向，確保實驗可重複性

3. **地板材質影響**
   - 問題：不同地板導致輪胎打滑
   - 解決：統一使用白色塑膠板作為實驗平台

4. **參數調整困難**
   - 問題：環境變因多，參數不易調整
   - 解決：標準化實驗環境後再進行參數優化

## 📚 參考資源

### 光敏電阻與 ADC
- [PCF8591 文件](https://www.chipwaygo.com/doc/pcf8591.php)
- [PCF8591 應用範例](https://www.jianshu.com/p/9b03a2b891b6)
- [樹莓派 LCD 顯示](https://blairan121122885.pixnet.net/blog/post/119657991)

### 超音波測距
- [Raspberry Pi 超音波感測器](https://atceiling.blogspot.com/2014/03/raspberry-pi_18.html)

### OpenCV 影像處理
- [OpenCV 顏色辨識](https://www.gushiciku.cn/pl/pFEr/zh-tw)
- [OpenCV 基礎教學](https://www.codeleading.com/article/51593370469/)
- [HSV 顏色空間](https://zhuanlan.zhihu.com/p/128989164)
- [OpenCV 實戰範例](https://www.twblogs.net/a/5d7dcf7cbd9eee541c344b50)

---

**專題指導**：物聯網課程實驗專題  
**開發時間**：2024 年  
**平台**：Raspberry Pi + Python 3
