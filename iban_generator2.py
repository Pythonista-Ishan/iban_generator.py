import tkinter as tk
import random
import os

# File to store generated account numbers and IBANs
DATA_FILE = "generated_account_number_and_IBAN.txt"

def load_existing_data():
    """Load existing account numbers and IBANs from the text file."""
    if not os.path.exists(DATA_FILE):
        return set()

    with open(DATA_FILE, 'r') as file:
        lines = file.readlines()
        return {line.strip() for line in lines}

def save_generated_data(account_number, iban):
    """Save the generated account number and IBAN to the text file."""
    with open(DATA_FILE, 'a') as file:
        file.write(f"{account_number},{iban}\n")

def generate_unique_number(existing_numbers):
    """Generate a unique 8-digit number not in existing_numbers."""
    while True:
        unique_number = str(random.randint(10000000, 99999999))
        if unique_number not in existing_numbers:
            return unique_number

def calculate_check_digits(iban):
    """Calculate the check digits for the IBAN."""
    expanded_iban = ''
    for char in iban:
        if char.isdigit():
            expanded_iban += char
        else:
            expanded_iban += str(ord(char.upper()) - 55)

    remainder = int(expanded_iban) % 97
    check_digits = (98 - remainder) % 100
    return f"{check_digits:02}"

def generate_iban():
    """Generate a new unique IBAN."""
    sort_code = "248652"
    country_code = "GB"
    bank_identifier_code = "WEST"
    additional_number = "12"

    existing_data = load_existing_data()
    
    while True:
        unique_number = generate_unique_number({line.split(',')[0] for line in existing_data})
        account_number = sort_code + unique_number
        
        modulus_weights = [0, 0, 1, 8, 2, 6, 3, 7, 9, 5, 8, 4, 2, 1]
        total = sum(int(digit) * weight for digit, weight in zip(account_number, modulus_weights))
        
        if total % 10 == 0:
            break
    
    iban_without_check_digits = f"{country_code}{bank_identifier_code}{sort_code}{unique_number}{additional_number}"
    check_digits = calculate_check_digits(iban_without_check_digits)
    
    iban = f"{country_code}{check_digits}{bank_identifier_code}{sort_code}{unique_number}"
    
    # Save the generated data
    save_generated_data(account_number, iban)

    # Display the IBAN
    result_label.config(text=iban)

# Create the main window
root = tk.Tk()
root.title("IBAN Generator")

# Create a button to generate the IBAN
generate_button = tk.Button(root, text="Generate IBAN", command=generate_iban)
generate_button.pack(pady=20)

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=20)

# Start the GUI event loop
root.mainloop()
