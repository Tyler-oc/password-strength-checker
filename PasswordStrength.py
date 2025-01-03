from flask import Flask, render_template, request, jsonify
import math
import re
import humanize

MAX_GUESSES_PER_SECOND = 350000000000
COMMON_WALKS = ['qwerty', '1234567890', '!23', '!@#$%^&*()', 'asdf', 'jkl;']

#Generate a list of all possible substrings of 3 or more:
common_substrings = set()
for walk in COMMON_WALKS:
    for i in range(len(walk)):
        for j in range(i + 3, len(walk) + 1):
            common_substrings.add(walk[i:j])

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/strength', methods=['POST'])
def strength():
    password = request.json.get('password', '')
    entropy = bits_of_entropy(password)
    adjusted_entropy = get_adjusted_entropy(password)

    return jsonify({
        'bits_of_entropy': entropy,
        'password_strength': password_strength(entropy, adjusted_entropy, password),
        'time_to_crack' : time_to_crack(entropy, password),
        'suggestions': get_suggestions(entropy, adjusted_entropy, password)
                    })


def bits_of_entropy(password):
    character_range = 0
    if has_lowercase_letter(password):
        character_range += 26
    if has_uppercase_letter(password):
        character_range += 26
    if has_symbol(password):
        character_range += 32
    if has_number(password):
        character_range += 10
    
    if character_range == 0:
        return 0
    
    return round(len(password) * math.log2(character_range))
    
def password_strength(entropy, adjusted_entropy, password):
    if entropy - adjusted_entropy >= 15:
        return 'Poor'
    if check_common_password(password):
        return 'Poor'
    if entropy >= 100:
        return 'Strong'
    if entropy >= 78:
        return 'Okay'
    return 'Poor'

def time_to_crack(entropy, password):
    if check_common_password(password):
        return '0 seconds'
    combinations = 2 ** entropy
    time_in_seconds = combinations / MAX_GUESSES_PER_SECOND / 2 #divide by 2 in order to get average time
    return convert_time(time_in_seconds)

def convert_time(seconds):
    if seconds < 60:
        return humanize.intword(seconds) + ' seconds'
    minutes = seconds / 60
    if minutes < 60:
        return humanize.intword(minutes) + ' minutes'
    hours = minutes / 60
    if hours < 24:
        return humanize.intword(hours) + ' hours'
    days = hours / 24
    if days < 7:
        return humanize.intword(days) + ' days'
    weeks = days / 7
    if weeks < 52:
        return humanize.intword(weeks) + ' weeks'
    return humanize.intword(weeks / 52) + ' years'

def has_lowercase_letter(password):
    return bool(re.search(r"[a-z]", password))


def has_uppercase_letter(password):
    return bool(re.search(r"[A-Z]", password))


def has_symbol(password):
    return bool(re.search(r"[^a-zA-Z0-9\s]", password))

def has_number(password):
    return bool(re.search(r"[0-9]", password))


def check_common_password(password):
    with open('commonpasswords.txt', 'r') as passwords:
        for line in passwords:
            if password in line:
                return True
    return False


def get_adjusted_entropy(password):
    updated_password_list = []

    for i in range(len(password)):
        # Append the character if it's different from the last appended one
        if not updated_password_list or updated_password_list[-1] != password[i]:
            updated_password_list.append(password[i])

    updated_password = ''.join(updated_password_list)

    for substring in common_substrings:
        if substring.lower() in password.lower():
            updated_password = updated_password.replace(substring, substring[0])

    return bits_of_entropy(updated_password)


def get_suggestions(entropy, adjusted_entropy, password):
    suggestions = []
    if entropy - adjusted_entropy >= 15:
        suggestions.append('Try to use less repeating characters or common keyboard walks')
    if check_common_password(password):
        suggestions.append('This is a very common password try to think of something more unique')

    return suggestions
        

if __name__ == "__main__":
    app.run(debug=True)