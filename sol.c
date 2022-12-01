#include <stdio.h>
#include <stdlib.h>
#include <string.h> 
#include <math.h>

#define BUF_1024 1024
#define BUF_2048 2048
#define BUF_20480 20480

#define OPENING_DAY 248
#define STOCK_TRAIN 584
#define STOCK_TEST 100

#define PATH_TEST_LABEL "./data/test/total_list.txt"
#define PATH_TEST_DATA "./data/test/total_cp_list.txt"

#define PATH_TRAIN_LABEL_ETF "./data/train/etf_list.txt"
#define PATH_TRAIN_DATA_ETF "./data/train/etf_cp_list.txt"
#define PATH_TRAIN_LABEL_KRX "./data/train/krx300_list.txt"
#define PATH_TRAIN_DATA_KRX "./data/train/krx300_cp_list.txt"

typedef char LABEL[BUF_2048];
typedef double TRAIN[STOCK_TRAIN][OPENING_DAY];
typedef double TEST[STOCK_TEST][OPENING_DAY];

//파일 입출력 함수
void readLabel(char * etf_path, char * krx_path, LABEL label[]);
void readStock(char * etf_path, char * krx_path, TRAIN stock);
void printLabel(LABEL label[]);
void printStock(TRAIN stock);

//전처리 함수
//roc = Rate Of Change, 일간변화율(%) = 100 * (당일종가 / 전일종가  - 1)
void getStockRoc(TRAIN stock, TRAIN stockRoc);
//누적변화율(%) = 100 * (당일누적종가 / 전일누적종가  - 1)
void getStockSumRoc(TRAIN stock, TRAIN stockSumRoc);
//log10 = log10(당일종가)
void getStockLog10(TRAIN stock, TRAIN stockLog10);
//log2 = log2(당일종가)
void getStockLog2(TRAIN stock, TRAIN stockLog2);


int main(void)
{
    LABEL label[STOCK_TRAIN];
    readLabel(PATH_TRAIN_LABEL_ETF, PATH_TRAIN_LABEL_KRX, label);
    TRAIN stock;
    readStock(PATH_TRAIN_DATA_ETF, PATH_TRAIN_DATA_KRX, stock);    

    //Phase 1 : 데이터 전처리
    TRAIN stockRoc;
    getStockRoc(stock, stockRoc);
    /*
    TRAIN stockSumRoc;
    getStockRoc(stock, stockSumRoc);
    TRAIN stockLog10;
    getStockLog10(stock, stockLog10);
    TRAIN stockLog2;
    getStockLog2(stock, stockLog2);
    */

    //Phase 2 : 특징 추출

    
   
   return 0;
}


void readLabel(char * etf_path, char * krx_path, LABEL label[]){
    FILE*fp=fopen(etf_path, "r" );
    char buf[BUF_2048];

    int i = 0;
    while (feof(fp) == 0) {
        fgets(buf, BUF_2048, fp);
        strcpy(label[i], buf);
        i++;
    }
    fclose(fp);
    
    fp = fopen(krx_path, "r");
    while (feof(fp) == 0) {
        fgets(buf, BUF_2048, fp);
        strcpy(label[i], buf);
        i++;
    }
    
}
void readStock(char * etf_path, char * krx_path, TRAIN stock){
    FILE*fp=fopen(etf_path, "r");
    char buf[BUF_20480];

    int i = 0;
    while (feof(fp) == 0) {
        fgets(buf, BUF_20480, fp);
        if(strlen(buf)<=2) continue;
        stock[i][0] = atof(strtok(buf, " "));
        for(int j = 1; j < OPENING_DAY-1; j++)
            stock[i][j] = atof(strtok(NULL, " "));
        stock[i][OPENING_DAY-1] = atof(strtok(NULL, "\n"));
        i++;
    }
    fclose(fp);
    
    fp=fopen(krx_path, "r");
    while (feof(fp) == 0) {
        fgets(buf, BUF_20480, fp);
        if(strlen(buf)<=2) continue;
        stock[i][0] = atof(strtok(buf, " "));
        for(int j = 1; j < OPENING_DAY-1; j++)
            stock[i][j] = atof(strtok(NULL, " "));
        stock[i][OPENING_DAY-1] = atof(strtok(NULL, "\n"));
        i++;
    }
}
void printLabel(LABEL label[]){
   for(int i = 0; i < STOCK_TRAIN; i++)
        printf("%d: %s", i+1, label[i]);
}
void printStock(TRAIN stock){
    for(int i = 0; i < STOCK_TRAIN; i++){
        printf("%d: ", i+1);
        for(int j = 0; j < OPENING_DAY; j++)
            printf("%f ", stock[i][j]);
        printf("\n");
    }
}


//--------전처리--------   
//일간변화율(%) = 100 * (당일종가 / 전일종가  - 1)
void getStockRoc(TRAIN stock, TRAIN stockRoc){
     for(int i = 0; i < STOCK_TRAIN; i++){
        for(int j = 1; j < OPENING_DAY; j++)
            stockRoc[i][j] = 100*(stock[i][j]/stock[i][j-1]-1);
        stockRoc[i][0] = stockRoc[i][1];
     }
}
//누적변화율(%) = 100 * (당일누적종가 / 전일누적종가  - 1)
void getStockSumRoc(TRAIN stock, TRAIN stockSumRoc){
     for(int i = 0; i < STOCK_TRAIN; i++){
        double temp[OPENING_DAY];
        temp[0] = stock[i][0];
        for(int j = 1; j < OPENING_DAY; j++)
            temp[j] = temp[j-1] + stock[i][j];

        for(int j = 1; j < OPENING_DAY; j++)
            stockSumRoc[i][j] = 100*(temp[j]/temp[j-1]-1);
        stockSumRoc[i][0] = temp[0];
     }
}
//log10 = log10(당일종가)
void getStockLog10(TRAIN stock, TRAIN stockLog10){
     for(int i = 0; i < STOCK_TRAIN; i++){
        for(int j = 0; j < OPENING_DAY; j++)
            stockLog10[i][j] = log10(stock[i][j]);
     }
}
//log2 = log2(당일종가)
void getStockLog2(TRAIN stock, TRAIN stockLog10){
     for(int i = 0; i < STOCK_TRAIN; i++){
        for(int j = 0; j < OPENING_DAY; j++)
            stockLog10[i][j] = log2(stock[i][j]);
     }
}
