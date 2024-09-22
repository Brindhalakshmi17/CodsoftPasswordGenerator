import string
import secrets
import sys
import os

# Define the character sets
UPPERCASE_LETTERS = string.ascii_uppercase
LOWERCASE_LETTERS = string.ascii_lowercase
DIGITS = string.digits
PUNCTUATION = string.punctuation

# Define ambiguous characters to exclude if needed
AMBIGUOUS_CHARACTERS = 'O0l1I|`\'"\\'

def get_user_preferences():
    print("=== Enhanced Password Generator ===\n")

    # Get password length
    while True:
        try:
            length = int(input("Enter the desired password length (minimum 6): "))
            if length < 6:
                print("Please enter a length of at least 6 characters for better security.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Choose character sets
    print("\nSelect character types to include in the password:")
    include_upper = get_yes_no("Include uppercase letters? (Y/N): ")
    include_lower = get_yes_no("Include lowercase letters? (Y/N): ")
    include_digits = get_yes_no("Include digits? (Y/N): ")
    include_punctuation = get_yes_no("Include punctuation symbols? (Y/N): ")

    # Ensure at least one character set is selected
    if not (include_upper or include_lower or include_digits or include_punctuation):
        print("You must select at least one character type. Please try again.\n")
        return get_user_preferences()

    # Exclude ambiguous characters
    exclude_ambiguous = get_yes_no("Exclude ambiguous characters (e.g., O, 0, l, 1)? (Y/N): ")

    # Option to save password
    save_password = get_yes_no("Do you want to save the password to a file? (Y/N): ")

    return {
        'length': length,
        'include_upper': include_upper,
        'include_lower': include_lower,
        'include_digits': include_digits,
        'include_punctuation': include_punctuation,
        'exclude_ambiguous': exclude_ambiguous,
        'save_password': save_password
    }

def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter Y (yes) or N (no).")

def generate_password(length, include_upper, include_lower, include_digits, include_punctuation, exclude_ambiguous):
    # Build the character pool based on user preferences
    character_pool = ''
    mandatory_characters = []

    if include_upper:
        chars = UPPERCASE_LETTERS
        if exclude_ambiguous:
            chars = ''.join([c for c in chars if c not in AMBIGUOUS_CHARACTERS])
        character_pool += chars
        mandatory_characters.append(secrets.choice(chars))

    if include_lower:
        chars = LOWERCASE_LETTERS
        if exclude_ambiguous:
            chars = ''.join([c for c in chars if c not in AMBIGUOUS_CHARACTERS])
        character_pool += chars
        mandatory_characters.append(secrets.choice(chars))

    if include_digits:
        chars = DIGITS
        if exclude_ambiguous:
            chars = ''.join([c for c in chars if c not in AMBIGUOUS_CHARACTERS])
        character_pool += chars
        mandatory_characters.append(secrets.choice(chars))

    if include_punctuation:
        chars = PUNCTUATION
        if exclude_ambiguous:
            chars = ''.join([c for c in chars if c not in AMBIGUOUS_CHARACTERS])
        character_pool += chars
        mandatory_characters.append(secrets.choice(chars))

    if not character_pool:
        raise ValueError("No characters available to generate password. Please adjust your preferences.")

    # Generate the remaining characters
    remaining_length = length - len(mandatory_characters)
    if remaining_length < 0:
        raise ValueError("Password length too short for the selected character types.")

    password_characters = mandatory_characters.copy()
    for _ in range(remaining_length):
        password_characters.append(secrets.choice(character_pool))

    # Shuffle the resulting password to prevent predictable sequences
    secrets.SystemRandom().shuffle(password_characters)

    # Combine into a single string
    password = ''.join(password_characters)
    return password

def assess_strength(length, types_included):
    strength = 0
    if length >= 12:
        strength += 2
    elif length >= 8:
        strength += 1
    if types_included >= 3:
        strength += 2
    elif types_included == 2:
        strength += 1

    if strength >= 4:
        return "Strong"
    elif strength == 3:
        return "Moderate"
    else:
        return "Weak"

def save_password_to_file(password):
    file_path = 'passwords.txt'
    try:
        with open(file_path, 'a') as file:
            file.write(password + '\n')
        print(f"Password saved to {file_path}")
    except IOError as e:
        print(f"Failed to save password to file: {e}")

def main():
    preferences = get_user_preferences()
    
    try:
        password = generate_password(
            length=preferences['length'],
            include_upper=preferences['include_upper'],
            include_lower=preferences['include_lower'],
            include_digits=preferences['include_digits'],
            include_punctuation=preferences['include_punctuation'],
            exclude_ambiguous=preferences['exclude_ambiguous']
        )
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)

    # Determine the number of character types included
    types_included = sum([
        preferences['include_upper'],
        preferences['include_lower'],
        preferences['include_digits'],
        preferences['include_punctuation']
    ])

    # Assess password strength
    strength = assess_strength(preferences['length'], types_included)

    # Display the password and its strength
    print("\n=== Generated Password ===")
    print(password)
    print(f"Password Strength: {strength}")

    # Optionally save the password
    if preferences['save_password']:
        save_password_to_file(password)

if __name__ == "__main__":
    main()
