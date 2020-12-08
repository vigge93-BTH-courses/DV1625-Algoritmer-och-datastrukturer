import math
import time
import random


def coin_greedy(n):
    coins = [1, 2, 5, 10, 25][::-1]

    res = 0

    for coin in coins:
        res += n // coin
        n %= coin

    return res


def coin_dynamic(n):

    coins = [1, 2, 5, 10, 25]

    if n == 0:
        return 0

    known_values = [math.inf for idx in range(n+1)]
    known_values[0] = 0

    for coin in coins:
        for i in range(1, n + 1):
            if i >= coin:
                known_values[i] = min(known_values[i], known_values[i-coin]+1)

    return known_values[-1]


amount = random.randint(10**8, 10**9)

t1 = time.perf_counter_ns()
print(coin_greedy(amount))
t2 = time.perf_counter_ns()
print(coin_dynamic(amount))
t3 = time.perf_counter_ns()

print("Greedy:", str((t2 - t1) / 1000000) + ' ms')
print("Dynamic", str((t3 - t2) / 1000000) + ' ms')
