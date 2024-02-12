my_str = "1 2 COM34 4 5)"
stripped = my_str[2:-1]
print(f"Data: {stripped}, len: {len(stripped)}")

result = my_str.find('COM')
for i in range(result, len(my_str)):
    if my_str[i] == ' ':
        print(f'Blank space found. Position: {i}')
        print(f'String before blank space: {my_str[result:i]}')
        break
    else:
        continue
