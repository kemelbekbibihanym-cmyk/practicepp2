numbers = [1, 2, 3, 4, 5]

# Using map with a lambda function
squared_numbers = list(map(lambda x: x**2, numbers))

print(squared_numbers)
# Output: [1, 4, 9, 16, 25]


string_prices = ["100", "250", "500"]

# Convert all strings to integers
int_prices = list(map(lambda x: int(x), string_prices))

print(int_prices) 
# Output: [100, 250, 500]

list1 = [1, 2, 3]
list2 = [10, 20, 30]

# Add elements from two lists together
sums = list(map(lambda x, y: x + y, list1, list2))

print(sums)
# Output: [11, 22, 33]