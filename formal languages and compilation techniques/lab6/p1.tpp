#include <cstdio>

int main() {
    int a;
    int b;
    scanf("%d", &a);
    scanf("%d", &b);

    int sum = a * b;
    printf("%d", sum);
    if (a) {
        printf("%d", a);
    }
    return 0;
}