#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

typedef unsigned long long UInt64;

ofstream fout("data1.out");
ofstream fout2("data2.out");

UInt64 gcd(UInt64 a, UInt64 b) {
    while (b != 0) {
        UInt64 aux = a % b;
        a = b;
        b = aux;
    }
    return a;
}

UInt64 exponentiation(UInt64 b, UInt64 power, UInt64 n) {
    UInt64 res = 1, tmp = b;
    for (UInt64 p = 1; p <= power; p <<= 1) {
        if ((p & power) != 0)
            res = (res * tmp) % n;
        tmp = tmp * tmp % n;
    }
    return res;
}

UInt64 calc_sqrt(UInt64 &n)
{
    if (n == 1) {
        return 1;
    }
    UInt64 sol=3, step = 1ULL << 29;
    for (; step; step >>= 1)
        if(n >= (sol+step)*(sol+step))
            sol+=step;
    return sol;
}

bool is_prime(UInt64 &n) {
    if (n == 1) {
        return false;
    }
    if (n % 2 == 0) {
        return true;
    }
    for (UInt64 i = 3; i * i <= n; ++i) {
        if (n % i == 0)
            return false;
    }
    return true;
}

vector<UInt64> factorize(UInt64 n) {
    vector<UInt64> factors;

    auto start = chrono::system_clock::now();

    while (!(n & 1)) {
        n >>= 1;
        factors.push_back(2);
    }
    UInt64 sq = calc_sqrt(n);
    for (UInt64 i = 3; i <= sq; i +=2) {
        if (n % i == 0) {
            while (n % i == 0) {
                n /= i;
                factors.push_back(i);
            }
            sq = calc_sqrt(n);
        }
    }
    if (n != 1) {
        factors.push_back(n);
    }

    auto end = chrono::system_clock::now();
    chrono::duration<double> elapsed_seconds = end-start;
    fout << n << " " << elapsed_seconds.count() << "\n";

    return factors;
}

UInt64 attempt_factorize(UInt64 n, UInt64 a, UInt64 k) {
    UInt64 p = exponentiation(a, k, n);
    return gcd(p-1, n);
}

vector<UInt64> factorize_pollard(UInt64 n, UInt64 &b, bool show) {
    vector<UInt64> factors;

    auto start = chrono::system_clock::now();

    UInt64 k;
    UInt64 step = 2;
    while ((step << 1) <= b) {
        step <<= 1;
    }
    k = step;
    for (UInt64 i = 3; i < b; i += 2) {
        if (is_prime(i)) {
            step = i;
            while (step * i <= b) {
                step *= i;
            }
            k *= step;
        }
    }
    UInt64 d = attempt_factorize(n, 2, k);
    for (UInt64 i = 3; (d == 1 || d == n) && i <= n; i += 2) {
        if (is_prime(i)) {
            d = attempt_factorize(n, i, k);
        }
    }
    if (d != 1 && d != n) {
        vector<UInt64> r1 = factorize_pollard(d, b, false);
        vector<UInt64> r2 = factorize_pollard(n / d, b, false);
        for (vector<UInt64> :: iterator it = r1.begin(); it != r1.end(); ++it)
            factors.push_back(*it);
        for (vector<UInt64> :: iterator it = r2.begin(); it != r2.end(); ++it)
            factors.push_back(*it);
    }
    else{
        factors.push_back(n);
    }

    if (show) {
        auto end = chrono::system_clock::now();
        chrono::duration<double> elapsed_seconds = end-start;
        fout2 << n << " " << elapsed_seconds.count() << "\n";
    }
    return factors;
}

int main() {
    ifstream fin("data.in");
    UInt64 nr, n, b;
    fout << fixed;
    fout2 << fixed;
    fin >> nr >> b;
    for (UInt64 i = 0; i < nr; ++i) {
        fin >> n;
        vector<UInt64> result = factorize(n);
        for (vector<UInt64> :: iterator it = result.begin(); it != result.end(); ++it) {
            cout << *it << " ";
        }
        cout << "\n";

        result = factorize_pollard(n, b, true);
        for (vector<UInt64> :: iterator it = result.begin(); it != result.end(); ++it) {
            cout << *it << " ";
        }
        cout << "\n";
    }
    fout.close();
    fout2.close();
    return 0;
}