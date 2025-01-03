from flask import Flask, render_template, request, jsonify
import math
import re
import humanize

MAX_GUESSES_PER_SECOND = 350000000000

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/strength', methods=['POST'])
def strength():
    password = request.json.get('password', '')
    entropy = bits_of_entropy(password)

    return jsonify({
        'bits_of_entropy': entropy,
        'password_strength': password_strength(entropy, password),
        'time_to_crack' : time_to_crack(entropy, password)
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
    
def password_strength(entropy, password):
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


if __name__ == "__main__":
    app.run(debug=True)