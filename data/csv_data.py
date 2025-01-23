from io import StringIO


with open('csv_data_file.csv', 'w') as file:
    file.write('name,email\n')
    file.write('john Doe,john.doe@example.com\n')

# data = "name,email\njohn Doe,john.doe@example.com\n"
# file = StringIO(data)

