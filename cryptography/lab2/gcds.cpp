#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <ctime>

#include <gmpxx.h>


using namespace std;

typedef mpz_class (gcd_function)(mpz_class a, mpz_class b);

gcd_function gcd1, gcd2, gcd3;

mpz_class gcd1(mpz_class a, mpz_class b) {
    while (b != 0) {
        mpz_class aux = a % b;
        a = b;
        b = aux;
    }
    return a;
}

mpz_class gcd2(mpz_class a, mpz_class b) {
    // simple cases (termination)
    if (a == b)
        return a;

    if (a == 0)
        return b;

    if (b == 0)
        return a;

    // look for factors of 2
    if ((a & 1) == 0) // a is even
    {
        if ((b & 1) == 1) // b is odd
            return gcd2((a >> 1), b);
        else // both a and b are even
            return gcd2((a >> 1), (b >> 1)) << 1;
    }

    if ((b & 1) == 0) // a is odd, b is even
        return gcd2(a, (b >> 1));

    // reduce larger argument
    if (a > b)
        return gcd2(((a - b) >> 1), b);

    return gcd2(((b - a) >> 1), a);
}

mpz_class gcd3(mpz_class a, mpz_class b) {
    while (a != b) {
        if (a > b)
            a -= b;
        else
            b -= a;
    }
    return a;
}



int main() {
    ifstream fin("data.in");
    ofstream fout1("data1.out"), fout2("data2.out"), fout3("data3.out");
    const gcd_function* gcd[] = {gcd1, gcd2, gcd3};
    ofstream* fout[] = {&fout1, &fout2, &fout3};
    int n;
    fin >> n;
    mpz_class p, q;
    for (int j = 0; j < 3; ++j)
        *fout[j] << fixed;
    for (int i = 0; i < n; ++i) {
        string s1, s2;
        fin >> s1 >> s2;
        p = s1;
        q = s2;
        for (int j = 0; j < 3; ++ j) {
            mpz_class a = p, b = q;
            auto start = chrono::system_clock::now();
            mpz_class res = gcd[j](a, b);
            auto end = chrono::system_clock::now();
            chrono::duration<double> elapsed_seconds = end-start;
            *fout[j] << res.get_str() << " " << elapsed_seconds.count() << " " << s1 << " " << s2 << "\n";
        }
    }
    fin.close();
    fout1.close();
    fout2.close();
    fout3.close();
    return 0;
}