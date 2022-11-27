import FinanceDataReader as fdr

#Read list(symbol, name) of krx300
#Load and write the one-year closing price of each stock

fr = open("./krx300_list.txt",'r')
fw = open("./krx300_cp_list.txt", 'w')

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
