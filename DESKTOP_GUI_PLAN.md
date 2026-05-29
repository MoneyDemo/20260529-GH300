# GUI Desktop BMI Calculator - Project Plan

## Overview
將現有的 Python Console BMI 計算機轉換為美化的桌面應用程式，提供直觀的使用者介面與優良的視覺設計。

## Objectives
- 轉換 Console 應用為桌面 GUI 應用
- 實現美化的使用者界面
- 保留原有的 BMI 計算邏輯與單元測試
- 支援 Windows、macOS、Linux 平台

## Requirements

### Functional Requirements
1. **BMI 計算功能**
   - 保留現有 calculate_bmi_value() 邏輯
   - 保留 classify_bmi() 分類邏輯
   - 支援 kg + inches / cm 輸入

2. **使用者介面**
   - 體重輸入欄（支援 kg 與 lbs 切換）
   - 身高輸入欄（支援 cm 與 inches 切換）
   - 即時 BMI 值顯示
   - 分類結果與建議訊息
   - 清除 / 重置功能

3. **視覺設計**
   - 現代化 UI 設計
   - 根據 BMI 分類顯示不同顏色
   - 響應式版面配置
   - 友善的字體與間距

### Non-Functional Requirements
- 應用啟動時間 < 2 秒
- 保持測試覆蓋率 >= 70%
- 跨平台相容性
- 可執行檔大小 < 100MB

## Technical Stack

### Options Evaluated
1. **PyQt6** (推薦)
   - 優點：功能完整、跨平台、易於美化
   - 缺點：檔案較大
   
2. **Tkinter**
   - 優點：輕量級、內置
   - 缺點：美化難度高
   
3. **PySimpleGUI**
   - 優點：易於使用
   - 缺點：功能受限

**推薦選項：PyQt6**

### Dependencies
```
PyQt6>=6.5.0
PyQt6-sip>=13.5.0
PyInstaller>=5.0  # 用於打包成可執行檔
```

## Implementation Plan

### Phase 1: Project Setup (Week 1)
- [ ] 建立 PyQt6 開發環境
- [ ] 建立 GUI 專案結構
- [ ] 更新 requirements.txt 與 setup.py

### Phase 2: Core UI Implementation (Week 1-2)
- [ ] 設計應用主視窗
- [ ] 實現輸入欄位與單位切換
- [ ] 連接 BMI 計算邏輯
- [ ] 實現結果顯示區域

### Phase 3: Visual Enhancement (Week 2-3)
- [ ] 設計與實現應用樣式表 (QSS)
- [ ] 配置顏色主題（根據 BMI 分類）
- [ ] 實現動畫與過渡效果
- [ ] 測試跨平台外觀

### Phase 4: Testing & Packaging (Week 3)
- [ ] 單元測試適配與驗證
- [ ] UI 功能測試
- [ ] 使用 PyInstaller 打包
- [ ] 跨平台測試

## Deliverables
1. `gui/main.py` - 應用主入口
2. `gui/ui/` - UI 元件與樣式
3. `gui/styles/` - QSS 樣式檔案
4. 更新後的 `requirements.txt`
5. `setup.py` 或 `pyproject.toml`
6. 可執行檔（Windows、macOS、Linux）
7. 使用者文件

## Success Criteria
- ✅ GUI 應用正常啟動與計算 BMI
- ✅ 所有現有測試通過
- ✅ 支援單位切換功能
- ✅ 跨平台可用性驗證
- ✅ 視覺設計符合現代風格

## Resources Required
- 1 Developer（全職）
- PyQt6 文件與教程
- UI/UX 設計參考

## Timeline
- **開始日期**: 2026-05-30
- **預期完成日期**: 2026-06-20
- **總工期**: 3 週

## Notes
- 保留現有測試框架與測試案例
- 建立單獨的 `gui/` 目錄保持模組化
- 考慮未來擴展（如數據圖表、歷史記錄等）
