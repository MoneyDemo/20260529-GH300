---
description: "Use when writing or refactoring C# code. Enforces C# naming conventions for types, members, fields, interfaces, constants, and async methods."
name: "CSharp 命名規則"
applyTo: "**/*.{cs,csx}"
---
# C# 命名規則

- 類別、介面、列舉、結構名稱必須使用 `PascalCase`。
- 介面名稱必須以 `I` 開頭，例如 `IUserService`。
- 公開方法、屬性、事件名稱必須使用 `PascalCase`。
- 區域變數與方法參數必須使用 `camelCase`。
- 私有欄位必須使用 `_camelCase`。
- `const` 與 `static readonly` 欄位名稱必須使用 `PascalCase`。
- 非同步方法名稱必須以 `Async` 結尾。
- 測試方法名稱應清楚描述情境、行為與預期結果。
- 避免不明縮寫；命名應以可讀性與維護性為優先。
