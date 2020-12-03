import csv, pandas as pd

data = {}
competitor_set = set()
with open('/nfs/sloanlab001/projects/dapa2_proj/Tabasco/Data/October/historical_prices.csv', newline='') as file:
    prices = csv.DictReader(file)
    for row in prices:
        data[row['sku']] = dict()


with open('/nfs/sloanlab001/projects/dapa2_proj/Tabasco/Data/October/historical_prices.csv', newline='') as file:
    prices = csv.DictReader(file)
    for row in prices:
        try:
            try:
                data[row['sku']][row['competidor']].append(int(row['price']))
            except ValueError:
                pass
        except KeyError:
            try:
                data[row['sku']][row['competidor']] = [int(row['price'])]
            except ValueError:
                pass
        if row['competidor'] != 'FALABELLA':
            competitor_set.add(row['competidor'])


with open('Correlation_between_competitors.txt', 'w') as f:
    for sku in data:
        for competitor in competitor_set:
            try:
                falabella = pd.Series(data[sku]['FALABELLA'])
                competitor_list = pd.Series(data[sku][competitor])
                corr = str(falabella.corr(competitor_list))
                if corr != 'nan':
                    f.write('Sku: ' + str(sku) + '\n')
                    f.write('Correlation b/w FALABELLA and ' + competitor + ': ' + str(falabella.corr(competitor_list)) + '\n')
            except KeyError:
                continue