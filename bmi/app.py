INCH_TO_METER = 0.0254


def inches_to_meters(height_in):
    return height_in * INCH_TO_METER


def calculate_bmi_value(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 24:
        return "Normal weight"
    if bmi < 27:
        return "Overweight"
    return "Obesity"


def calculate_bmi(weight_kg, height_in):
    height_m = inches_to_meters(height_in)
    bmi = calculate_bmi_value(weight_kg, height_m)
    category = classify_bmi(bmi)
    return bmi, category


def get_user_input():
    weight_kg = float(input("Enter your weight in kg: "))
    height_in = float(input("Enter your height in inches: "))
    return weight_kg, height_in


def format_result(bmi, category):
    return [
        f"Your BMI is: {bmi:.2f}",
        f"You are categorized as: {category}",
    ]


def main():
    weight_kg, height_in = get_user_input()
    bmi, category = calculate_bmi(weight_kg, height_in)

    for line in format_result(bmi, category):
        print(line)

if __name__ == "__main__":
    main()