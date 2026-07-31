from datetime import datetime

def log_function_call(func):
    def wrapper():
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"Function Name: {func.__name__}")
        print(f"Was called at: {current_time}")
        return func()
    return wrapper

@log_function_call
def sayhello():
    print("HELLLOOO!")

sayhello()