from flask import Flask, render_template, request
import re, math, pickle

app = Flask(__name__)

def is_in_wordlist(password):
    for i in range(1, 4):
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
    if not uppercase_error: charset += 26
    if not digit_error: charset += 10
    if not special_char_error: charset += 32

    strength = len(password) * math.log2(charset) if charset > 0 else 0
    total_guesses = 2 ** strength
    time_seconds = total_guesses / float(guesses_per_second)

    def time_format(seconds):
        if seconds < 1:
            return "Less than a second."
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds / 86400:.2f} days"
        else:
            return f"{seconds / 31536000:.2f} years"

    brute_time = time_format(time_seconds)
    errors = []
    if length_error: errors.append(" At least 8 characters.")
    if lowercase_error: errors.append(" Add a lowercase letter.")
    if uppercase_error: errors.append(" Add an uppercase letter.")
    if digit_error: errors.append(" Add a digit.")
    if special_char_error: errors.append(" Add a special character.")

    return len(errors) == 0, brute_time, errors

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    brute_time = None
    errors = []
    found_in_wordlist = False
    password_match = True

    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        level = request.form.get("threat_level") or "1e9"

        is_strong, brute_time, errors = password_strength(password, level)
        found_in_wordlist = is_in_wordlist(password)
        password_match = password == confirm

        if not is_strong or found_in_wordlist or not password_match:
            result = "❌ Password is weak or unsafe. Please improve it."
        else:
            result = "✅ Password is strong and safe."

    return render_template("index.html", result=result, brute_time=brute_time, errors=errors, found=found_in_wordlist, password_match=password_match)

if __name__ == "__main__":
    app.run(debug=True)
