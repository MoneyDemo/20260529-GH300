# BMI 專案單元測試操作文件

本文件說明如何：
1. 啟動 Python 虛擬環境
2. 執行完整單元測試
3. 輸出詳細測試訊息

## 1. 進入專案資料夾

先在終端機切換到 BMI 專案資料夾：

```powershell
cd C:\Users\tzyu\Downloads\20260529\bmi
```

## 2. 建立虛擬環境（首次執行才需要）

如果尚未建立 .venv，請先執行：

```powershell
python -m venv .venv
```

## 3. 啟動虛擬環境

### PowerShell（建議）

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
```

啟動成功後，提示字元通常會出現 (.venv)。

### Command Prompt（cmd）

```bat
.venv\Scripts\activate.bat
```

### Git Bash

```bash
source .venv/Scripts/activate
```

## 4. 安裝相依套件

依 requirements.txt 安裝套件：

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5. 執行完整單元測試

執行 tests 資料夾下所有測試：

```powershell
python -m pytest
```

若要精簡輸出：

```powershell
python -m pytest -q
```

## 6. 輸出詳細測試訊息

需要更完整資訊時，使用以下參數：

### 顯示更詳細的測試名稱

```powershell
python -m pytest -v
```

### 顯示測試內 print() 輸出

```powershell
python -m pytest -s
```

### 失敗時顯示完整 Traceback

```powershell
python -m pytest --tb=long
```

### 常用詳細輸出組合

```powershell
python -m pytest -v -s --tb=long
```

### 顯示每個測試耗時

```powershell
python -m pytest -v --durations=0
```

## 7. 只跑特定測試檔

只執行 BMI 計算測試：

```powershell
python -m pytest tests/test_calculate_bmi.py -v
```

只執行 BMI 分類測試：

```powershell
python -m pytest tests/test_classify_bmi.py -v
```

## 8. 只跑單一測試案例

以下示範只執行一個測試 function：

```powershell
python -m pytest tests/test_classify_bmi.py::test_classify_bmi_returns_normal_weight_for_18_5 -v
```

## 9. 離開虛擬環境

完成後可執行：

```powershell
deactivate
```

## 10. 常見問題排除

### 問題：啟動腳本被封鎖

請在同一個終端機工作階段執行：

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned)
```

再重新啟動虛擬環境：

```powershell
& .\.venv\Scripts\Activate.ps1
```

### 問題：找不到 pytest

請先確認虛擬環境已啟動，再重新安裝 requirements：

```powershell
python -m pip install -r requirements.txt
```

### 問題：執行測試時出現 import 錯誤

請確認你是在 bmi 資料夾內執行 pytest：

```powershell
cd C:\Users\tzyu\Downloads\20260529\bmi
python -m pytest -v
```
