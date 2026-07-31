def validate_positive_integers(func):
    def wrapper(*A):
        for PosOrNeg in A:
            if not isinstance(PosOrNeg, int) or PosOrNeg <= 0:
                print("Error: All arguments must be positive integers.")
                return
        return func(*A)
    return wrapper

@validate_positive_integers
def check(a, b):
    print("Arguements are Positive and Hence Valid.")

number1= input("Enter First Number: ")
number2= input("Enter Second Number: ")

check(int(number1), int(number2))
