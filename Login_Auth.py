def login(func):
    def wrapper(logged_in):
        if logged_in:
            func(logged_in)
        else:
            print ("================================")
            print ("ACCESS DENIED: Login Required")
            print ("================================")

    return wrapper

@login
def disp(logged_in):
    print("Login successful! Welcome.")


CORRECT_USER = "Rudyy"
CORRECT_PASS = "Rudyy2986"

username = input("Enter username: ")
password = input("Enter password: ")

if username == CORRECT_USER and password == CORRECT_PASS:
        disp(logged_in=True)
else:
        disp(logged_in=False)