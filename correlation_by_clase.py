import csv
import pandas as pd

data = {}
with open('/nfs/sloanlab001/projects/dapa2_proj/Tabasco/Data/October/historical_prices.csv', newline='') as file:
    prices = csv.DictReader(file)
    for row in prices:
        data[row['sku']] = ([], [], [])


with open('/nfs/sloanlab001/projects/dapa2_proj/Tabasco/Data/October/historical_prices.csv', newline='') as file:
    prices = csv.DictReader(file)
    for row in prices:
        if row['competidor'] == 'FALABELLA':
            try:
                data[row['sku']][0].append(float(row['price']))
            except ValueError:
                pass
        elif row['competidor'] == 'RIPLEY':
            try:
                data[row['sku']][1].append(float(row['price']))
            except ValueError:
                pass
        elif row['competidor'] == 'PARIS':
            try:
                data[row['sku']][2].append(float(row['price']))
            except ValueError:
                pass


sku_clase = {}
with open('/nfs/sloanlab001/projects/dapa2_proj/Tabasco/Data/October/historical_products.csv', newline='', encoding='utf-8') as file:
    products = csv.DictReader(file, delimiter= ';')
    for row in products:
        sku_clase[row['sku']] = row['id_clase']

print(sku_clase)

sku_corr = {}
for sku in data:
    falabella = pd.Series(data[sku][0])
    ripley_list = pd.Series(data[sku][1])
    paris_list = pd.Series(data[sku][2])
    corr_ripley = falabella.corr(ripley_list)
    corr_paris = falabella.corr(paris_list)
    try:
        sku_corr[sku_clase[sku]].append((sku, corr_ripley, len(data[sku][1]), corr_paris, len(data[sku][2])))
    except KeyError:
        try:
            sku_corr[sku_clase[sku]] = [(sku, corr_ripley, len(data[sku][1]), corr_paris, len(data[sku][2]))]
        except KeyError:
            try:
                sku_corr['None'].append((sku, corr_ripley, len(data[sku][1]), corr_paris, len(data[sku][2])))
            except KeyError:
                sku_corr['None'] = [(sku, corr_ripley, len(data[sku][1]), corr_paris, len(data[sku][2]))]


with open('Correlation_by_clase.csv', mode='w') as f:
    f_writer = csv.writer(f)
    f_writer.writerow(['sku', 'id_clase', 'competitor', 'correlation', 'num_data_points'])
    for clase in sku_corr.keys():
        print(clase)
        for sku in sku_corr[clase]:
            if str(sku[1]) != 'nan':
                try:
                    f_writer.writerow([sku[0], sku_clase[sku], 'RIPLEY', sku[1], sku[2]])
                except KeyError:
                    f_writer.writerow([sku[0], 'None', 'RIPLEY', sku[1], sku[2]])
            if str(sku[3]) != 'nan':
                try:
                    f_writer.writerow([sku[0], sku_clase[sku], 'PARIS', sku[3], sku[4]])
                except KeyError:
                    f_writer.writerow([sku[0], 'None', 'PARIS', sku[3], sku[4]])

