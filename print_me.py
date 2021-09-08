import os

result = os.system("cat print_me.py")

print(str(result)[:-1])