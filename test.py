import os

password = "admin123"
user_input = input("Enter username: ")

query = "SELECT * FROM users WHERE username = '" + user_input + "'"

print(password)
print(query)