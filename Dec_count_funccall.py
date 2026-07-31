def count_calls(func):
    count = 0

    def wrapper(*arg):
        nonlocal count
        count = call
        print("Function will be called", count, "time(s)\n")
        return func(*arg)

    return wrapper

call = int(input("Enter how many times do you want to call the function?: "))


@count_calls
def addition(call):
    add = 0
    num2= 0
    for i in range(call):
        num = int(input("Enter any number: "))
        add += num
        print("Example: Addition of", num, "with", num2, "is", add)
        num2=num

addition(call)