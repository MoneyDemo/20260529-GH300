from app import classify_bmi


def test_classify_bmi_returns_underweight_for_value_less_than_18_5():
    # Arrange
    bmi = 18.49

    # Act
    category = classify_bmi(bmi)

    # Assert
    assert category == "Underweight"


def test_classify_bmi_returns_normal_weight_for_18_5():
    # Arrange
    bmi = 18.5

    # Act
    category = classify_bmi(bmi)

    # Assert
    assert category == "Normal weight"


def test_classify_bmi_returns_overweight_for_24():
    # Arrange
    bmi = 24

    # Act
    category = classify_bmi(bmi)

    # Assert
    assert category == "Overweight"


def test_classify_bmi_returns_obesity_for_27():
    # Arrange
    bmi = 27

    # Act
    category = classify_bmi(bmi)

    # Assert
    assert category == "Obesity"
