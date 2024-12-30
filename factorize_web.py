from flask import Flask, request, render_template
from math import gcd
from random import randint
import os

app = Flask(__name__)

# Sieve for small numbers
N = 100005
primes = []

def sieve():
    prime = [1] * N
    prime[0] = prime[1] = 0
    for i in range(2, N):
        if prime[i] == 0:
            continue
        primes.append(i)
        for j in range(i << 1, N, i):
            prime[j] = 0

sieve()

def modPow(a, b, m):
    res = 1
    while b > 0:
        if b & 1:
            res = (res * a) % m
        b >>= 1
        a = (a * a) % m
    return res

def millerRabin(n):
    if n < 2:
        return 0
    if n == 2 or n == 3:
        return 1
    if n % 2 == 0:
        return 0

    x, two = n - 1, 0
    while x % 2 == 0:
        two += 1
        x //= 2

    for _ in range(10):  # Reduced iterations for speed
        a = randint(1, n - 1)
        res = modPow(a, x, n)
        if res == 1 or res == n - 1:
            continue
        composite = True
        for _ in range(two):
            res = res * res % n
            if res == n - 1:
                composite = False
                break
        if composite:
            return 0
    return 1

def get_factors(n):
    factors = {}
    def get(n, m):
        if n <= 1:
            return
        if millerRabin(n):
            m[n] = m.get(n, 0) + 1
            return
        d, cnt = n, 2
        while d == n:
            d = gcd(randint(2, n - 1), n)
            cnt += 1
        get(d, m)
        get(n // d, m)

    get(n, factors)
    return dict(sorted(factors.items()))

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    number = ""
    if request.method == "POST":
        number = request.form.get("number")
        if number.isdigit():
            num = int(number)
            if num > 0 and len(number) <= 20:
                factors = get_factors(num)
                result = " ".join(f"{k}^{v}" for k, v in factors.items())
            else:
                result = "Please enter a positive number up to 20 digits."
        else:
            result = "Invalid input. Please enter a valid positive integer."
    return render_template("index.html", result=result, number=number)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
