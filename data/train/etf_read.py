import FinanceDataReader as fdr
#Read list(symbol, name) of etf
#Load and write the one-year closing price of each stock

PATH_COMPANY_CODE = "./data/train/etf_list.txt" #(회사명 주식코드)로 이루어진 파일
PATH_CLOSING_PRICE_OF_1YEAR = "./data/train/etf_cp_list.txt" #(584개의 회사에 대한 1년 개장일 248일 종가)로 이루어진 파일

fr = open(PATH_COMPANY_CODE, "r", encoding='euc-kr')
fw = open(PATH_CLOSING_PRICE_OF_1YEAR, 'w', encoding='euc-kr')
count = 0
while True:
    line = fr.readline()
    if not line: break

    symbol = line.split(' ')[0]
    cp_oneyear = fdr.DataReader(symbol, '2020-01-01', '2020-12-31').Close

    for cp_day in cp_oneyear:
        fw.write(str(cp_day)+" ")
    fw.write("\n\n")

fr.close()
fw.close()
