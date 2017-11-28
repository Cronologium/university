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

int main(){
    unsigned n, a;
    ifstream fin("data.in");
    ofstream fout("data.out");
    fin >> n;
    for (unsigned i = 0; i < n; ++i) {
        fin >> a;
        vector<mpz_class> bases;
        bases.push_back(1);
        for (mpz_class i = 2; i <= a - 1; i += 1)
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
