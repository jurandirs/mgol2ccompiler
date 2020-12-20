#include <stdio.h>
typedef char literal[256];
void main(void){
    /*----Variaveis temporarias----*/
    int T0;
    int T1;
    int T2;
    int T3;
    int T4;
    /*------------------------------*/
    literal A;
    int B;
    int D;
    double C;
    



    printf("Digite B\n");
    scanf("%d", &B);
    printf("Digite A:\n");
    scanf("%s", A);
    T0 = B > 2;
        if (T0) {
        T1 = B <= 4;
            if (T1) {
            printf("B esta entre 2 e 4\n");
        }
    }
    T2 = B + 1;
    B = T2;
    T3 = B + 2;
    B = T3;
    T4 = B + 3;
    B = T4;
    D = B;
    C = 5.0;
    printf("\nB=\n\n");
    printf("%d\n",D);
    printf("\n\n");
    printf("%lf\n",C);
    printf("\n\n");
    printf("%s\n",A);
}
