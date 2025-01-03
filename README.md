# password-strength-checker

To start: Python3 PasswordStrength.py

This project was made to learn more about AuthN and password cracking.

The formula used for entropy is: log_2(R^L) where R is the pool of possible characters and L is the length of the password

The passwords are also checked against the top 100,000 most common passwords.

This is not a complete check of how secure a password is, as it only takes into account brute force attacks.

The number for time to crack assumes an attacker has access to the database and can try 350 billion hashes per second
(this is the number achieved by researchers using a machine designed for brute force attacks)
