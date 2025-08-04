
        try:
            with open(f"rockyou_{i}.pkl", "rb") as f:
                chunk = pickle.load(f)
                if password in chunk:
                    return True
        except FileNotFoundError:
            print(f"rockyou_{i}.pkl not found.")
    return False

def password_strength(password, guesses_per_second):
    length_error = len(password) < 8
    lowercase_error = re.search("[a-z]", password) is None
    uppercase_error = re.search("[A-Z]", password) is None
    digit_error = re.search("[0-9]", password) is None
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    charset = 0
    if not lowercase_error: charset += 26