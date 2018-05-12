i = 0
with open('test.csv', 'w') as testCSV:
    if i <= 10:
        testCSV.write('test', 'cell2')
    i += i

