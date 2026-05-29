import math

from app import cm_to_meters, inches_to_meters, pounds_to_kg


def test_inches_to_meters_converts_correctly():
    # Arrange
    height_in = 68

    # Act
    result = inches_to_meters(height_in)

    # Assert
    assert math.isclose(result, 1.7272, rel_tol=1e-12)


def test_cm_to_meters_converts_correctly():
    # Arrange
    height_cm = 170

    # Act
    result = cm_to_meters(height_cm)

    # Assert
    assert math.isclose(result, 1.7, rel_tol=1e-12)


def test_pounds_to_kg_converts_correctly():
    # Arrange
    weight_lb = 150

    # Act
    result = pounds_to_kg(weight_lb)

    # Assert
    assert math.isclose(result, 68.0388555, rel_tol=1e-9)
