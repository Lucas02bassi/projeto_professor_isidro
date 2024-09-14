#include <stdio.h>

int main() {
    int a, b;
    printf("Programa Teste\n");
    printf("Digite A\n");
    scanf("%d", &a);
    printf("Digite B\n");
    scanf("%d", &b);
    if (a < b) {
    c = (a / b);
    } else {
    c = (a * b);
    }
    printf("C e igual a \n");
    printf("%d", c);
    printf("\n");
    return 0;
}
