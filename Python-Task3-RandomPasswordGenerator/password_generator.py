import random
import string

print("================================")
print("   RANDOM PASSWORD GENERATOR")
print("================================")

while True:

    # Ask for password length
    while True:
        try:
            length = int(input("\nEnter password length (minimum 8): "))

            if length >= 8:
                break
            else:
                print("Password must be at least 8 characters.")

        except ValueError:
            print("Please enter a valid number.")

    # Ask for character types
    print("\nChoose character types:")
    print("1. Uppercase letters")
    print("2. Lowercase letters")
    print("3. Numbers")
    print("4. Symbols")

    while True:
        choice = input("Enter at least 2 choices (example: 1,2,3): ")

        choices = choice.replace(" ", "").split(",")

        if len(set(choices)) < 2:
            print("Please select at least 2 types.")
        else:
            break

    characters = ""
    password = []

    if "1" in choices:
        characters += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))

    if "2" in choices:
        characters += string.ascii_lowercase
        password.append(random.choice(string.ascii_lowercase))

    if "3" in choices:
        characters += string.digits
        password.append(random.choice(string.digits))

    if "4" in choices:
        characters += string.punctuation
        password.append(random.choice(string.punctuation))

    # Generate remaining characters
    for i in range(length - len(password)):
        password.append(random.choice(characters))

    random.shuffle(password)

    final_password = "".join(password)

    print("\nYour Password is:")
    print(final_password)

    again = input("\nGenerate another password? (y/n): ")

    if again.lower() != "y":
        print("Thank you!")
        break