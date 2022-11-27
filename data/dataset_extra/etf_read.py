import FinanceDataReader as fdr

#Read list(symbol, name) of etf
#Load and write the one-year closing price of each stock

fr = open("./etf_list.txt","r")
fw = open("./etf_cp_list.txt", 'w')
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
