def check_temp(min_value):
    error = "Please enter a number that is more " \
            "than {}".format(min_value)

    try:
        response = float(input("Choose a number: "))

        if response < min_value:
            print(error)
        else:
            return response

    except ValueError:
        print(error)


# checks temperature to see if more than -459 and then converts it
def to_celsius(self):

    self.check_temp(-459)


# main routine

while True:
    to_check = check_temp(-459)
    print("Success!")
