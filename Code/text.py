def textFunction(user_input):
    print("text function executed")
    print("The item you're looking for: " + user_input)

    # This program allows the user to choose what item they want to look for in the rooms.
    # The user can only pick 1 item to search for. If the user types out more than 1 item, 
    # then the program will pick the first item that was typed out.

    # Enter the True while loop at least once

    # Boolean to make sure the user provides correct input
    invalid_input = True

    while(invalid_input):
        #user_input = input("What item are you looking for? Choose one: ").lower()

        # if the object is found then store it in a variable and negate the boolean
        if ("thermos" in user_input):
            user_object = "Thermos"
            invalid_input = False
            return user_object
        elif ("keys" in user_input):
            user_object = "Keys"
            invalid_input = False
            return user_object
        elif ("phone" in user_input):
            user_object = "Phone"
            invalid_input = False
            return user_object
        elif ("wallet" in user_input):
            user_object = "Wallet"
            invalid_input = False
            return user_object
        # if invalid input, tell them to try again but don't negate the boolean
        else:
            return "Invalid input. Try again"

