# 編碼助手指南（Agents Guide）

## 專案概觀

此倉庫包含兩個主要子專案：

1. **BMI 計算機（Python）** - `bmi/` 資料夾
   - 主要應用：體重身高 BMI 計算與分類
   - 計畫轉換為美化的 PyQt6 桌面應用（參見 `DESKTOP_GUI_PLAN.md` 與 GitHub Issue #1）
   - 包含完整的單元測試與測試文件

2. **平行非同步示例（C# / .NET 6 WPF）** - `APL2007M2Sample1/` 資料夾
   - 教學用途：示範 async/await 與平行 HTTP 下載
   - WPF 桌面應用

## 核心習慣與慣例

### Python 專案（BMI）

#### 專案結構
```
bmi/
├── app.py                           # 主要應用程式
├── requirements.txt                 # 相依套件
├── .venv/                           # Python 虛擬環境
├── tests/
│   ├── test_calculate_bmi.py        # BMI 計算單元測試
│   └── test_classify_bmi.py         # BMI 分類單元測試
├── UNIT_TESTING_GUIDE.md            # 測試操作指南
├── BMI_CONSOLE_WEB_COMPARISON.md    # Console vs 網頁對比
└── BMI_CHROME_DEVTOOLS_REPORT.md    # Chrome DevTools 驗證報告
```

#### 關鍵習慣
- **模組化設計**：邏輯函式與 UI 邏輯分離
  - `calculate_bmi_value()` - 純計算函式
  - `classify_bmi()` - 分類邏輯
  - `inches_to_meters()` - 單位轉換
  - `get_user_input()` / `format_result()` - I/O 邏輯
  - `main()` - 流程協調

- **單元測試原則（3A模式）**：
  - Arrange（準備）→ Act（執行）→ Assert（驗證）
  - 每個測試案例必須是獨立函式
  - 測試檔案與目標函式一一對應

- **文件規範**：
  - `UNIT_TESTING_GUIDE.md` - 如何執行測試
  - `BMI_*_REPORT.md` - 驗證與比對報告
  - `DESKTOP_GUI_PLAN.md` - GUI 轉換計畫

#### 常用命令

**虛擬環境**
```bash
# 啟動虛擬環境（PowerShell）
cd bmi
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)

# 安裝相依套件
python -m pip install -r requirements.txt
```

**運行測試**
```bash
# 簡潔輸出
python -m pytest -q

# 詳細輸出與執行耗時
python -m pytest -v --durations=0

# 特定測試檔
python -m pytest tests/test_calculate_bmi.py -v
```

**運行應用**
```bash
# Console 版本
python app.py
```

### C# / .NET 專案（WPF）

#### 專案結構
```
APL2007M2Sample1/
├── APL2007M2Sample1.csproj         # 專案檔
├── App.xaml / App.xaml.cs          # 應用程式進入點
├── MainWindow.xaml / MainWindow.xaml.cs  # 主視窗 UI 與邏輯
├── README.md                        # 詳細技術說明
├── generate_*.py                    # 報告生成腳本
├── bin/                             # 編譯輸出
├── obj/                             # 中間物件檔（.gitignore 中排除）
└── docs/                            # 文件與範本
```

#### 關鍵習慣
- **非同步程式設計**：使用 `async/await` 與 `Task.WhenAll`
- **UI 執行緒安全**：使用 `Dispatcher.BeginInvoke()` 切換回 UI 線程
- **平行 HTTP 下載**：多個 URL 同時發送 GET 請求

#### 常用命令

**編譯**
```bash
dotnet build APL2007M2Sample1/APL2007M2Sample1.csproj
```

**執行**
```bash
dotnet run --project APL2007M2Sample1/APL2007M2Sample1.csproj
```

## 開發環境設定

### VS Code 設定
- **MCP 伺服器** - `.vscode/mcp.json`
  - Context7（文件查詢）
  - Microsoft Docs（官方文件）
  - Chrome DevTools（網頁調試）

### Dev Container
- **配置檔** - `.devcontainer/devcontainer.json`
  - Python 3.12 + .NET 8
  - 包含 GitHub CLI
  - 自動安裝 BMI requirements.txt

### .gitignore 規則
- **Python**：`__pycache__/`、`.venv/`、`.pytest_cache/`、`*.pyc`
- **.NET**：`bin/`、`obj/`、`*.csproj.nuget.*`、`project.assets.json`
- **報告**：`report_assets/`、`*.docx`、`*.pdf`
- 詳見 `.gitignore`

## 架構決策

### BMI 應用設計
- **分層架構**
  - 計算層：純函式（易於測試）
  - 邏輯層：組合函式的業務流程
  - 展示層：`main()` 處理 I/O

- **GUI 轉換策略**
  - 推薦框架：**PyQt6**（功能完整、跨平台、易於美化）
  - 架構：保留現有計算邏輯，包裝為 PyQt6 元件
  - 計畫見 `DESKTOP_GUI_PLAN.md`

### 測試策略
- **單元測試優先**：每個純函式都有對應測試
- **獨立測試案例**：3A 模式（Arrange→Act→Assert）
- **覆蓋率目標**：>= 70%（尤其是計算邏輯）

## 關鍵檔案與對應責任

| 檔案 | 用途 | 修改時機 |
|------|------|---------|
| `bmi/app.py` | 核心 BMI 計算與 I/O | 新增計算邏輯或改進算法 |
| `bmi/tests/test_calculate_bmi.py` | BMI 計算測試 | 新增或修改計算函式 |
| `bmi/tests/test_classify_bmi.py` | BMI 分類測試 | 新增或修改分類範圍 |
| `bmi/requirements.txt` | Python 相依 | 新增外部套件 |
| `DESKTOP_GUI_PLAN.md` | GUI 轉換計畫 | 規劃新功能或修改設計 |
| `.vscode/mcp.json` | MCP 伺服器設定 | 新增開發工具 |
| `.gitignore` | Git 排除規則 | 新增專案類型或構建工具 |

## 常見開發流程

### 添加新的 BMI 計算功能
1. 在 `bmi/app.py` 新增純函式
2. 在 `bmi/tests/test_*.py` 添加測試案例（3A 模式）
3. 執行 `pytest` 驗證
4. 更新 `UNIT_TESTING_GUIDE.md`（如適用）
5. Commit 與 Push

### GUI 開發（未來）
1. 在 `gui/` 資料夾建立 PyQt6 應用
2. 複用 `bmi/app.py` 中的計算邏輯
3. 為 GUI 元件編寫對應測試
4. 更新 `requirements.txt` 加入 PyQt6

### 跨平台驗證
- 使用 Dev Container（自動一致性）
- 本地 Windows / macOS / Linux 測試
- 使用 GitHub Actions（未來可考慮）

## 後續改進與待辦項

- [ ] GUI 桌面應用開發（PyQt6）- 見 GitHub Issue #1
- [ ] 構建 GitHub Actions 自動化測試流程
- [ ] 添加數據持久化功能（歷史記錄）
- [ ] 支援多語言（繁中、英文等）
- [ ] 國際化單位支援（BMI vs 其他指標）

## 貢獻指南

1. **建立新分支**：`git checkout -b feature/your-feature-name`
2. **遵循 3A 測試模式**：新增測試案例必須明確標示 Arrange→Act→Assert
3. **提交前驗證**：
   ```bash
   pytest -v
   git status
   ```
4. **撰寫清晰的 Commit 訊息**：說明「做了什麼」與「為什麼」
5. **推送並建立 Pull Request**

## 相關文件連結

- [BMI 單元測試指南](bmi/UNIT_TESTING_GUIDE.md)
- [Console vs 網頁比對報告](bmi/BMI_CONSOLE_WEB_COMPARISON.md)
- [Chrome DevTools 驗證報告](bmi/BMI_CHROME_DEVTOOLS_REPORT.md)
- [桌面 GUI 轉換計畫](DESKTOP_GUI_PLAN.md)
- [WPF 應用詳細說明](APL2007M2Sample1/README.md)
