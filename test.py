import random

while True:
    rnd = random.randint(0,2)
    if rnd == 0:
        a1 = 10
        a2 = random.randint(0,255)
        a3 = random.randint(0,255)
        a4 = random.randint(0,255)
    elif rnd == 1:
        a1 = 172
        a2 = random.randint(16,32)
        a3 = random.randint(0,255)
        a4 = random.randint(0,255)
    else:
        a1 = 192
        a2 = 168
        a3 = random.randint(0,255)
        a4 = random.randint(0,255)
    print(f'{a1}.{a2}.{a3}.{a4}')
