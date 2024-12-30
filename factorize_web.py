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

def f(x:int,c:int,mod:int)->int:
    return (modPow(x,2,mod)+c)%mod

############ Pollard Rho ################################
# works in O(N^0.25)
def rho(n:int,x0:int,c:int)->int:
    if n&1==0 :
        return 2
    x=x0
    y=x0
    g=1
    cnt = 800000
    while g==1 and cnt>0:
        x=f(x,c,n)
        y=f(f(y,c,n),c,n)
        g=gcd(abs(x-y),n)
        cnt-=1
    
    return g

def get_factors(n):
    factors = {}

    for k in primes:
        if k > n:
            break

        while n%k==0:
            factors[k]=factors.get(k,0)+1
            n//=k
        
    def get(n:int,m:dict)->None:
        if n<=1:
            return
        # print("call for n=",n)
    
        p=millerRabin(n)
        # print("prime status=",p)
        if p == 1:
            m[n]= 1 if n not in m else m[n]+1
            return

        d,cnt=rho(n,2,1),2
    
        # print("for n=",n," div=",d)

        if d==n:
            d=rho(n,2,cnt)
            cnt+=1
    
        if d==1:
            return
        get(d,m)
        get(n//d,m)

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
    sieve()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
