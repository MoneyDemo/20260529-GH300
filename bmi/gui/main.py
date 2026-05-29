"""BMI 計算機 - 桌面版圖形介面 (PyQt6)

將原本的 Console BMI 計算機轉換為美化的桌面應用程式。
重用 ``app.py`` 中既有的 BMI 計算與分類邏輯，並提供：

* 體重輸入（公斤 / 磅 切換）
* 身高輸入（公分 / 英吋 切換）
* 即時 BMI 數值與分類顯示
* 依分類顯示對應顏色與健康建議
* 重置功能

執行方式：
    python -m gui.main      # 於 bmi/ 目錄下
或：
    python gui/main.py
"""

import os
import sys

# 讓本檔案無論從何處執行，都能匯入位於 bmi/ 目錄的 app.py
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_BMI_DIR = os.path.dirname(_THIS_DIR)
if _BMI_DIR not in sys.path:
    sys.path.insert(0, _BMI_DIR)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QColor

from app import (
    calculate_bmi_value,
    classify_bmi,
    cm_to_meters,
    inches_to_meters,
    pounds_to_kg,
)

# 將英文分類對應為繁體中文顯示文字、顏色與健康建議
CATEGORY_INFO = {
    "Underweight": {
        "label": "體重過輕",
        "color": "#3b82f6",
        "advice": "您的體重偏低，建議均衡飲食並適度增加營養攝取。",
    },
    "Normal weight": {
        "label": "正常範圍",
        "color": "#22c55e",
        "advice": "太棒了！您的體重維持在健康範圍，請繼續保持。",
    },
    "Overweight": {
        "label": "體重過重",
        "color": "#f59e0b",
        "advice": "體重稍高，建議搭配規律運動與飲食控制。",
    },
    "Obesity": {
        "label": "肥胖",
        "color": "#ef4444",
        "advice": "建議諮詢專業醫師，並透過運動與飲食調整改善健康。",
    },
}


def _resource_dir():
    """回傳資源檔所在目錄；於 PyInstaller 打包後改用 _MEIPASS 暫存目錄。"""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, "styles")
    return os.path.join(_THIS_DIR, "styles")


def load_stylesheet():
    """讀取 QSS 樣式表內容，若檔案不存在則回傳空字串。"""
    qss_path = os.path.join(_resource_dir(), "style.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as qss_file:
            return qss_file.read()
    except OSError:
        return ""


class BMIWindow(QMainWindow):
    """BMI 計算機主視窗。"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI 健康計算機")
        self.setMinimumSize(440, 640)
        self._build_ui()

    # ------------------------------------------------------------------
    # 介面建構
    # ------------------------------------------------------------------
    def _build_ui(self):
        root = QWidget()
        root.setObjectName("rootWidget")
        self.setCentralWidget(root)

        outer_layout = QVBoxLayout(root)
        outer_layout.setContentsMargins(24, 24, 24, 24)

        card = QFrame()
        card.setObjectName("card")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_shadow(card, blur=40, alpha=60, y_offset=12)
        outer_layout.addWidget(card)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        card_layout.addWidget(self._build_header())

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(28, 24, 28, 24)
        body_layout.setSpacing(18)
        card_layout.addWidget(body)

        # 體重輸入
        self.weight_input = self._make_spinbox(maximum=500.0, value=60.0, suffix="")
        self.weight_unit = self._make_unit_combo(["公斤 (kg)", "磅 (lbs)"])
        body_layout.addLayout(
            self._build_field_row("體重", self.weight_input, self.weight_unit)
        )

        # 身高輸入
        self.height_input = self._make_spinbox(maximum=300.0, value=170.0, suffix="")
        self.height_unit = self._make_unit_combo(["公分 (cm)", "英吋 (in)"])
        self.height_unit.currentIndexChanged.connect(self._on_height_unit_changed)
        body_layout.addLayout(
            self._build_field_row("身高", self.height_input, self.height_unit)
        )

        # 按鈕列
        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.calculate_button = QPushButton("計算 BMI")
        self.calculate_button.setObjectName("calculateButton")
        self.calculate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calculate_button.clicked.connect(self.calculate)

        self.reset_button = QPushButton("重置")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset)

        button_row.addWidget(self.calculate_button, stretch=2)
        button_row.addWidget(self.reset_button, stretch=1)
        body_layout.addLayout(button_row)

        # 結果卡片
        body_layout.addWidget(self._build_result_card())

        body_layout.addStretch(1)

        self.footer_label = QLabel("BMI = 體重(kg) ÷ 身高(m)²　·　僅供健康參考")
        self.footer_label.setObjectName("footerLabel")
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body_layout.addWidget(self.footer_label)

    def _build_header(self):
        banner = QFrame()
        banner.setObjectName("headerBanner")
        banner.setFixedHeight(120)
        layout = QVBoxLayout(banner)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(4)
        layout.addStretch(1)

        title = QLabel("BMI 健康計算機")
        title.setObjectName("titleLabel")
        subtitle = QLabel("輸入您的體重與身高，立即掌握身體質量指數")
        subtitle.setObjectName("subtitleLabel")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch(1)
        return banner

    def _build_field_row(self, label_text, spinbox, combo):
        container = QVBoxLayout()
        container.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        container.addWidget(label)

        row = QHBoxLayout()
        row.setSpacing(10)
        row.addWidget(spinbox, stretch=2)
        row.addWidget(combo, stretch=1)
        container.addLayout(row)
        return container

    def _build_result_card(self):
        card = QFrame()
        card.setObjectName("resultCard")
        self._apply_shadow(card, blur=24, alpha=30, y_offset=6)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(6)

        value_row = QHBoxLayout()
        value_row.setSpacing(8)
        value_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bmi_value_label = QLabel("--")
        self.bmi_value_label.setObjectName("bmiValueLabel")
        unit_label = QLabel("kg/m²")
        unit_label.setObjectName("bmiUnitLabel")
        unit_label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )

        value_row.addWidget(self.bmi_value_label)
        value_row.addWidget(unit_label)
        layout.addLayout(value_row)

        self.category_label = QLabel("請輸入資料後按下計算")
        self.category_label.setObjectName("categoryLabel")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.category_label)

        self.advice_label = QLabel("")
        self.advice_label.setObjectName("adviceLabel")
        self.advice_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advice_label.setWordWrap(True)
        layout.addWidget(self.advice_label)

        return card

    # ------------------------------------------------------------------
    # 小工具建立輔助
    # ------------------------------------------------------------------
    def _make_spinbox(self, maximum, value, suffix):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(0.0, maximum)
        spinbox.setDecimals(1)
        spinbox.setSingleStep(0.5)
        spinbox.setValue(value)
        if suffix:
            spinbox.setSuffix(suffix)
        spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spinbox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.UpDownArrows)
        return spinbox

    def _make_unit_combo(self, items):
        combo = QComboBox()
        combo.addItems(items)
        combo.setCursor(Qt.CursorShape.PointingHandCursor)
        return combo

    def _apply_shadow(self, widget, blur, alpha, y_offset):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, y_offset)
        shadow.setColor(QColor(99, 102, 241, alpha))
        widget.setGraphicsEffect(shadow)

    # ------------------------------------------------------------------
    # 行為邏輯
    # ------------------------------------------------------------------
    def _on_height_unit_changed(self, index):
        """切換身高單位時，調整合理的預設值與範圍。"""
        if index == 0:  # 公分
            self.height_input.setRange(0.0, 300.0)
            self.height_input.setValue(170.0)
        else:  # 英吋
            self.height_input.setRange(0.0, 120.0)
            self.height_input.setValue(67.0)

    def _weight_in_kg(self):
        value = self.weight_input.value()
        if self.weight_unit.currentIndex() == 1:  # 磅
            return pounds_to_kg(value)
        return value

    def _height_in_meters(self):
        value = self.height_input.value()
        if self.height_unit.currentIndex() == 1:  # 英吋
            return inches_to_meters(value)
        return cm_to_meters(value)

    def calculate(self):
        weight_kg = self._weight_in_kg()
        height_m = self._height_in_meters()

        if weight_kg <= 0 or height_m <= 0:
            self._show_error("請輸入大於 0 的體重與身高")
            return

        bmi = calculate_bmi_value(weight_kg, height_m)
        category = classify_bmi(bmi)
        info = CATEGORY_INFO[category]

        self.bmi_value_label.setText(f"{bmi:.1f}")
        self.bmi_value_label.setStyleSheet(f"color: {info['color']};")
        self.category_label.setText(info["label"])
        self.category_label.setStyleSheet(f"color: {info['color']};")
        self.advice_label.setText(info["advice"])

    def reset(self):
        self.weight_unit.setCurrentIndex(0)
        self.height_unit.setCurrentIndex(0)
        self.weight_input.setValue(60.0)
        self.height_input.setRange(0.0, 300.0)
        self.height_input.setValue(170.0)

        self.bmi_value_label.setText("--")
        self.bmi_value_label.setStyleSheet("color: #1e293b;")
        self.category_label.setText("請輸入資料後按下計算")
        self.category_label.setStyleSheet("color: #94a3b8;")
        self.advice_label.setText("")

    def _show_error(self, message):
        self.bmi_value_label.setText("--")
        self.bmi_value_label.setStyleSheet("color: #1e293b;")
        self.category_label.setText(message)
        self.category_label.setStyleSheet("color: #ef4444;")
        self.advice_label.setText("")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("BMI 健康計算機")

    # 設定跨平台的繁體中文字型優先序，確保各作業系統都能正確顯示
    font = QFont()
    font.setFamilies(
        [
            "Noto Sans CJK TC",
            "Microsoft JhengHei",
            "PingFang TC",
            "Heiti TC",
            "sans-serif",
        ]
    )
    font.setPointSize(10)
    app.setFont(font)

    app.setStyleSheet(load_stylesheet())

    window = BMIWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
