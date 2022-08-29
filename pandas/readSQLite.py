import pandas as pd
import sqlite3
from tabulate import tabulate

if __name__ == "__main__":
    con = sqlite3.connect('property.db')

    flats = pd.read_sql("SELECT f.flat_id, r.region, c.city, s.street, f.house_number, "
                 "f.flat_number, rm.name, rm.length, rm.width, rm.height FROM room rm "
                 "JOIN flat f ON rm.flat_id = f.flat_id "
                 "JOIN street s ON f.street_id = s.street_id "
                 "JOIN city c ON s.city_id = c.city_id "
                 "JOIN region r ON c.region_id = r.region_id "
                 "ORDER BY city, street, house_number, flat_number", con)


    flats['square'] = flats['width'] * flats['length']
    flats['cost'] = flats['square'] * 600
    flats['volume'] = flats['square'] * flats['height']

    flats['address'] = flats['city'] + ' ' + flats['street'] + ' ' + flats['house_number'].apply(str) + '/' + flats['flat_number'].apply(str)
    flats.loc[flats['name'] == 'Bedroom', 'rooms'] = 1
    #print(tabulate(flats, headers='keys', tablefmt='psql'))

    flats_info = flats[['address', 'rooms', 'square', 'volume', 'cost']].groupby(['address']).sum()
    flats_info = flats_info.reset_index()
    print(tabulate(flats_info, headers='keys', tablefmt='psql'))

    categories = ['Количество квартир:',
                  'Количество 1-к. кв.:',
                  'Количество 2-к. кв.:',
                  'Количество 3-к. кв.:',
                  'Квартира с комнатой наименьшей площади:',
                  'Квартира с комнатой наибольшей площади:',
                  'Квартира с ванной наименьшего объема:',
                  'Квартира с ванной наибольшего объема:']

    values = [len(flats_info),
              len(flats_info['address'][flats_info['rooms'] == 1]),
              len(flats_info['address'][flats_info['rooms'] == 2]),
              len(flats_info['address'][flats_info['rooms'] == 3]),
              flats['address'].iloc[flats['square'][flats['name'] == 'Bedroom'].idxmin()],
              flats['address'].iloc[flats['square'][flats['name'] == 'Bedroom'].idxmax()],
              flats['address'].iloc[flats['volume'][flats['name'] == 'Bathroom'].idxmin()],
              flats['address'].iloc[flats['volume'][flats['name'] == 'Bathroom'].idxmax()]]

    flats_analysis = pd.DataFrame({'Категории': categories, 'Значения': values})
    print(tabulate(flats_analysis, headers='keys', tablefmt='psql'))

    #with pd.ExcelWriter('test.xlsx') as writer:
    #    flats_info.to_excel(writer, sheet_name='Info', index=False)
    #    flats_analysis.to_excel(writer, sheet_name='Analysis', index=False)
