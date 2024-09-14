#include <stdio.h>

int main() {
    int a, c;
    a = 2;
    printf("Digite o valor de c: ");
    scanf("%d", &c);
    c = ((c * a) - a);
    printf("%d\n", c);

    return 0;
}
