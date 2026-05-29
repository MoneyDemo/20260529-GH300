import math

from app import calculate_bmi


def test_calculate_bmi_returns_expected_bmi_and_category_for_normal_weight():
    # Arrange
    weight_kg = 70
    height_in = 68

    # Act
    bmi, category = calculate_bmi(weight_kg, height_in)

    # Assert
    assert math.isclose(bmi, 23.464579801131926, rel_tol=1e-12)
    assert category == "Normal weight"


def test_calculate_bmi_returns_underweight_when_bmi_is_less_than_18_5():
    # Arrange
    weight_kg = 45
    height_in = 68

    # Act
    bmi, category = calculate_bmi(weight_kg, height_in)

    # Assert
    assert bmi < 18.5
    assert category == "Underweight"


def test_calculate_bmi_returns_obesity_when_bmi_is_27_or_higher():
    # Arrange
    weight_kg = 85
    height_in = 64

    # Act
    bmi, category = calculate_bmi(weight_kg, height_in)

    # Assert
    assert bmi >= 27
    assert category == "Obesity"
