# This program allows the user to choose what item they want to look for in the rooms.
# The user can only pick 1 item to search for. If the user types out more than 1 item, 
# then the program will pick the first item that was typed out.

# Boolean to check if the user wants to find another item
unfound_item = True

# Enter the True while loop at least once
while(unfound_item):
    # Boolean to make sure the user provides correct input
    invalid_input = True

    while(invalid_input):
        user_input = input("What item are you looking for? Choose one: ").lower()

        # if the object is found then store it in a variable and negate the boolean
        if ("thermos" in user_input):
            user_object = "Thermos"
            invalid_input = False
        elif ("keys" in user_input):
            user_object = "Keys"
            invalid_input = False
        elif ("phone" in user_input):
            user_object = "Phone"
            invalid_input = False
        elif ("wallet" in user_input):
            user_object = "Wallet"
            invalid_input = False
        # if invalid input, tell them to try again but don't negate the boolean
        else:
            print("Invalid input. Try again")

        
        print("The item you're looking for: {}".format(user_object))

    # Boolean to see if the user wants to find another object
    invalid_decision = True

    while(invalid_decision):
        user_decision = input("Would you like to find another object? y/n: ").lower()

        # negate or don't negate the boolean depending on the user's decision
        if (user_decision == "y" or user_decision == "y"):
            break
        elif (user_decision == "no" or user_decision == "n"):
            invalid_decision = False
            unfound_item = False
        else:
            print("Invalid input. Try again")
