# BMI Console vs 成人版BMI計算機 比較報告

## 測試目的
以「手動逐筆執行 BMI console」方式，針對 4 種 BMI 分類各設計 1 筆案例，並與衛福部成人版 BMI 計算機結果比對。

## 測試條件
- Console 程式輸入單位：體重(kg) + 身高(in)
- 網頁輸入單位：體重(kg) + 身高(cm)
- 固定身高：68 in（等於 172.72 cm）
- 網頁固定條件：性別男、年齡 30 歲
- 比較來源網頁：https://www.hpa.gov.tw/Obesity/BmiCalculate.aspx

## 手動執行案例
| 案例ID | 目標分類 | 體重(kg) | 身高(in) | 身高(cm) |
|---|---|---:|---:|---:|
| C1 | Underweight | 50 | 68 | 172.72 |
| C2 | Normal weight | 65 | 68 | 172.72 |
| C3 | Overweight | 75 | 68 | 172.72 |
| C4 | Obesity | 90 | 68 | 172.72 |

## 詳細結果比較表
| 案例ID | Console BMI | Console 分類 | 網頁 BMI | 網頁分類 | 一致性判定 | 備註 |
|---|---:|---|---:|---|---|---|
| C1 | 16.76 | Underweight | 16.8 | 體位過輕 | 一致 | 僅小數位數不同（2 位 vs 1 位） |
| C2 | 21.79 | Normal weight | 21.8 | 體位正常 | 一致 | 僅小數位數不同（2 位 vs 1 位） |
| C3 | 25.14 | Overweight | 25.1 | 體位過重 | 一致 | 中英文名稱不同，語意一致 |
| C4 | 30.17 | Obesity | 30.2 | 體位超重 | 部分一致 | 皆屬 BMI >= 27 區間，但命名粒度不同 |

## Console 手動執行輸出摘要
### C1 (50kg, 68in)
- Your BMI is: 16.76
- You are categorized as: Underweight

### C2 (65kg, 68in)
- Your BMI is: 21.79
- You are categorized as: Normal weight

### C3 (75kg, 68in)
- Your BMI is: 25.14
- You are categorized as: Overweight

### C4 (90kg, 68in)
- Your BMI is: 30.17
- You are categorized as: Obesity

## 網頁查得結果摘要
### C1 (50kg, 172.72cm)
- BMI值：16.8
- 體位：體位過輕

### C2 (65kg, 172.72cm)
- BMI值：21.8
- 體位：體位正常

### C3 (75kg, 172.72cm)
- BMI值：25.1
- 體位：體位過重

### C4 (90kg, 172.72cm)
- BMI值：30.2
- 體位：體位超重

## 結論
- 4 筆案例的 BMI 數值皆與網頁結果高度一致，差異僅來自小數位顯示規則。
- 分類邏輯在 C1~C3 可視為一致。
- C4 在「高 BMI 區間命名」上有差異：console 使用 Obesity，網頁使用體位超重；兩者皆指向高風險區間。
