#include <fstream>
#include <iostream>
#include <vector>
#include <gmpxx.h>

using namespace std;

mpz_class exponentiation(mpz_class b, mpz_class power, mpz_class n) {
    mpz_class res = 1, tmp = b;
    for (mpz_class p = 1; p <= power; p <<= 1) {
        if ((p & power) != 0)
            res = (res * tmp) % n;
        tmp = tmp * tmp % n;
    }
    return res;
}

vector<mpz_class> factorize1(mpz_class n) {
    vector<mpz_class> output;
    mpz_class t0 = sqrt(n);
    for (mpz_class i = 1; i < t0; i += 1)
    {
        mpz_class t = t0 + i;
        mpz_class s = sqrt((t * t) - n);
        if (s * s == t) {
            vector<mpz_class> lv = factorize1(t - s);
            vector<mpz_class> rv = factorize1(t + s);
            output.insert(output.end(), lv.begin(), lv.end());
            output.insert(output.end(), rv.begin(), rv.end());
            return output;
        }
    }
    output.push_back(n);
    return output;
}

int main(){
    unsigned n, a;
    ifstream fin("data.in");
    ofstream fout("data.out");
    fin >> n;
    for (unsigned i = 0; i < n; ++i) {
        fin >> a;
        vector<mpz_class> bases;
        bases.push_back(1);
        for (mpz_class i = 2; i < a - 1; i += 1)
        {
            if (exponentiation(i, a - 1, a) == 1 && gcd(i, a) == 1)
            {
                bases.push_back(i);
            }
        }
        for (vector<mpz_class> :: iterator it = bases.begin(); it != bases.end(); ++it) {
            fout << (*it).get_str() << " ";
        }
        fout << "\n";
    }
    fin.close();
    fout.close();
    return 0;
}
