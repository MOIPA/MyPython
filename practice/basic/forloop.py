# input form user
name = input('name:')

# for loop
x = [i for i in range(10)]
print(x)

for i in [x*2 for x in range(10)]:
    print(i)

f = [x + y for x in 'ABCDE' for y in '1234567']
print(f)
