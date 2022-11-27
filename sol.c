#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <math.h>

#define BUF_1024 1024
#define BUF_10240 10240
#define PATH_COMPANRY_CODE "./data/dataset/total_list.txt"
#define PATH_CLOSING_PRICE "./data/dataset/total_cp_list.txt"

#define DAY_IN_2021 248
#define NUM_STOCK 100

typedef char LABEL[BUF_1024][2];
typedef double DATA[NUM_STOCK][DAY_IN_2021];

//파일 입출력 함수
void readCodeAndName(char * path, LABEL label[NUM_STOCK]);
void readStock(char * path, DATA stock);
void printLABEL(LABEL label[NUM_STOCK]);
void printDATA(DATA stock);

//전처리 함수
//roc = Rate Of Change, 일간변화율(%) = 100 * (당일종가 / 전일종가  - 1)
void getStockRoc(DATA stock, DATA stockRoc);
//누적변화율(%) = 100 * (당일누적종가 / 전일누적종가  - 1)
void getStockSumRoc(DATA stock, DATA stockSumRoc);
//log10 = log10(당일종가)
void getStockLog10(DATA stock, DATA stockLog10);
//log2 = log2(당일종가)
void getStockLog2(DATA stock, DATA stockLog2);


int main(void)
{
    LABEL label[NUM_STOCK];
    readCodeAndName(PATH_COMPANRY_CODE, label);
    DATA stock;
    readStock(PATH_CLOSING_PRICE , stock);

    //Phase 1 : 데이터 전처리
    DATA stockRoc;
    getStockRoc(stock, stockRoc);
    DATA stockSumRoc;
    getStockRoc(stock, stockSumRoc);
    DATA stockLog10;
    getStockLog10(stock, stockLog10);
    DATA stockLog2;
    getStockLog2(stock, stockLog2);

    //Phase 2 : 특징 추출

    
   
   return 0;
}


void readCodeAndName(char * path, LABEL label[NUM_STOCK]){
    FILE*fp=fopen(path, "r");
    char buf[BUF_1024];
    for(int i = 0; i < NUM_STOCK; i++){
        fgets(buf, BUF_1024, fp);
        strcpy(label[i][0], strtok(buf, " "));
        strcpy(label[i][1], strtok(NULL, "\n"));
    }
}
void readStock(char * path,  DATA stock){
    FILE*fp=fopen(path, "r");
    char buf[BUF_10240];

    int i = 0;
    while (feof(fp) == 0) {
        fgets(buf, BUF_10240, fp);
        if(strlen(buf)<=2) continue;
        stock[i][0] = atoi(strtok(buf, " "));
        for(int j = 1; j < DAY_IN_2021-1; j++)
            stock[i][j] = atoi(strtok(NULL, " "));
        stock[i][DAY_IN_2021-1] = atoi(strtok(NULL, "\n"));
        i++;
    }

}
void printLABEL(LABEL label[NUM_STOCK]){
   for(int i = 0; i < NUM_STOCK; i++)
        printf("%d: %s %s\n", i+1, label[i][0], label[i][1]);
}
void printDATA(DATA stock){
    for(int i = 0; i < NUM_STOCK; i++){
        printf("%d: ", i+1);
        for(int j = 0; j < DAY_IN_2021; j++)
            printf("%f ", stock[i][j]);
        printf("\n");
    }
}


//--------전처리--------   
//일간변화율(%) = 100 * (당일종가 / 전일종가  - 1)
void getStockRoc(DATA stock, DATA stockRoc){
     for(int i = 0; i < NUM_STOCK; i++){
        for(int j = 1; j < DAY_IN_2021; j++)
            stockRoc[i][j] = 100*(stock[i][j]/stock[i][j-1]-1);
        stockRoc[i][0] = stockRoc[i][1];
     }
}
//누적변화율(%) = 100 * (당일누적종가 / 전일누적종가  - 1)
void getStockSumRoc(DATA stock, DATA stockSumRoc){
     for(int i = 0; i < NUM_STOCK; i++){
        double temp[DAY_IN_2021];
        temp[0] = stock[i][0];
        for(int j = 1; j < DAY_IN_2021; j++)
            temp[j] = temp[j-1] + stock[i][j];

        for(int j = 1; j < DAY_IN_2021; j++)
            stockSumRoc[i][j] = 100*(temp[j]/temp[j-1]-1);
        stockSumRoc[i][0] = temp[0];
     }
}
//log10 = log10(당일종가)
void getStockLog10(DATA stock, DATA stockLog10){
     for(int i = 0; i < NUM_STOCK; i++){
        for(int j = 0; j < DAY_IN_2021; j++)
            stockLog10[i][j] = log10(stock[i][j]);
     }
}
//log2 = log2(당일종가)
void getStockLog2(DATA stock, DATA stockLog10){
     for(int i = 0; i < NUM_STOCK; i++){
        for(int j = 0; j < DAY_IN_2021; j++)
            stockLog10[i][j] = log2(stock[i][j]);
     }
}
