---
description: "Use when writing or refactoring Python code. Enforces Python naming conventions for variables, functions, classes, constants, modules, and tests."
name: "Python 命名規則"
applyTo: "**/*.{py,pyi}"
---
# Python 命名規則

- 函式名稱必須使用 `snake_case`。
- 變數名稱必須使用 `snake_case`。
- 類別名稱必須使用 `PascalCase`。
- 常數名稱必須使用 `UPPER_SNAKE_CASE`。
- 模組檔名必須使用 `snake_case.py`。
- 私有成員（非公開）應以單一底線前綴，例如 `_internal_value`。
- 布林值命名優先使用可讀前綴，例如 `is_`、`has_`、`can_`。
- 測試函式名稱必須以 `test_` 開頭，並描述行為與預期結果。
- 避免不明縮寫；命名應優先可讀性與語意清晰。
