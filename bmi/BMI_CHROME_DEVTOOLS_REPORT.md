# BMI Chrome DevTools MCP 重跑報告

## 執行方式
本次網頁驗證使用 Chrome DevTools MCP 工具（mcp_io_github_chr_*）重新執行。

- 網頁: https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx
- 固定條件: 男、30 歲、身高 172.72 cm
- 案例體重: 50 / 65 / 75 / 90 kg
- Console 對照值: 使用前次手動 console 執行結果

## 比較表（Console vs 網頁重跑）
| 案例ID | 輸入 (kg, in/cm) | Console BMI | Console 分類 | 網頁 BMI (DevTools MCP) | 網頁分類 | 比較結論 |
|---|---|---:|---|---:|---|---|
| C1 | 50, 68 / 172.72 | 16.76 | Underweight | 16.8 | 體位過輕 | 一致（僅小數位顯示差異） |
| C2 | 65, 68 / 172.72 | 21.79 | Normal weight | 21.8 | 體位正常 | 一致（僅小數位顯示差異） |
| C3 | 75, 68 / 172.72 | 25.14 | Overweight | 25.1 | 體位過重 | 一致（語意一致、命名不同） |
| C4 | 90, 68 / 172.72 | 30.17 | Obesity | 30.2 | 體位超重 | 部分一致（皆屬高 BMI 區間，命名粒度不同） |

## 網頁重跑實際結果（MCP 擷取）
- C1: BMI值 16.8，分類「體位過輕」
- C2: BMI值 21.8，分類「體位正常」
- C3: BMI值 25.1，分類「體位過重」
- C4: BMI值 30.2，分類「體位超重」

## Network Requests 統整
本次 Network 共擷取 39 筆請求（含 preserved requests）。

### 1) 狀態碼統計
- 200: 38 筆
- 302: 1 筆（重新計算動作觸發 POST -> redirect）

### 2) 方法統計
- GET: 36 筆
- POST: 3 筆

### 3) 資源類型（依 URL 粗分）
- Document / ASPX: 4 筆
- CSS: 9 筆
- Image: 26 筆

### 4) 關鍵請求流程（Demo 重點）
1. POST /Obesity/BmiCalculate.aspx -> 302（重新計算）
2. GET /Obesity/BmiCalculate.aspx -> 200（回到輸入頁）
3. POST /Obesity/BmiCalculate.aspx -> 200（送出新身高/體重計算結果）

## Network Requests 明細（39 筆）
| reqid | Method | Status | URL |
|---:|---|---:|---|
| 66 | POST | 200 | https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx |
| 67 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/layout.css |
| 68 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/inner.css |
| 69 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/sport.css |
| 70 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/title/BMI_content.png |
| 71 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiBg.png |
| 72 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-01.png |
| 73 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-02.png |
| 74 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-03.png |
| 75 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-04.png |
| 76 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-05.png |
| 77 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiCTBg.jpg |
| 78 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/noteBg.png |
| 79 | POST | 302 | https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx |
| 80 | GET | 200 | https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx |
| 81 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/layout.css |
| 82 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/inner.css |
| 83 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/sport.css |
| 84 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/title/BMI.png |
| 85 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiBg.png |
| 86 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-01.png |
| 87 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-02.png |
| 88 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-03.png |
| 89 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-04.png |
| 90 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-05.png |
| 91 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiCTBg.jpg |
| 92 | POST | 200 | https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx |
| 93 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/layout.css |
| 94 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/inner.css |
| 95 | GET | 200 | https://www.hpa.gov.tw/Obesity/css/sport.css |
| 96 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/title/BMI_content.png |
| 97 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiBg.png |
| 98 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-01.png |
| 99 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-02.png |
| 100 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-03.png |
| 101 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-04.png |
| 102 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/pic/adultBmiPic-05.png |
| 103 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/adultBmiCTBg.jpg |
| 104 | GET | 200 | https://www.hpa.gov.tw/Obesity/images/bg/noteBg.png |
