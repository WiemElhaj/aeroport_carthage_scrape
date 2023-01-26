import logging
import pandas as pd
import requests
from calendar import monthrange

global df_final
headers = ["Heure Locale", "Origine", "Compagnie", "N° de Vol", "Statut"]
for year in [2021, 2022]:
    for month in range(1, 13):
        # number days per month 
        number_days = monthrange(year, month)[1]
        for day in range(1, number_days+1):
            try:
                url = requests.get(f'http://www.aeroport-de-tunis-carthage.com/tunisie-aeroport-de-tunis-carthage-vol-arrivee-date-{year}-{month}-{day}')
                df = pd.read_html(url.text)
                pd.set_option('display.max_rows', None)
                df = df[4]
                new_df = pd.DataFrame(df.values[1:], columns=headers)
                # remove all rows that contain NA values

                new_df = new_df.dropna()
                # remove all rows that contain publicity information and ads

                new_df = new_df[~new_df.Origine.str.contains('|'.join("google_ad_client"))]
                # add a new column and we will set its value to the day number with the same length as other columns

                new_df.insert(5, "N° du jour", [day] * len(new_df.index), True)
                # add a new column and we will set its value to the month number going from 1 to 12 with the same length as other columns
                
                new_df.insert(6, "N° du mois", [month] * len(new_df.index), True)
                # add a new column and we will set its value to the year with the same length as other columns
                
                new_df.insert(7, "Année", [year] * len(new_df.index), True)

                # concatenate all the days informations into one dataframe
                if day == 1 and year == 2021 and month == 1:
                    df_final = new_df
                else:
                    df_final = pd.concat([df_final, new_df])
            except Exception:
                
                logging.warning(f'error occured for this date : {year}/{month}/{day}!')
                continue

files_header = headers + ["N° du jour"] + ["N° du mois"] + ["Année"]
# save the DataFrame to a csv file
# na_rep = 'NotFound' : replace all NaN values with NotFound ( default is "")
# index = False : didn't use the rows index column
# header parameter : Setting Custom Column Names in the CSV
# sep : Specifying separator for the CSV/XLSX Output, default is comma ( csv : comma separated value )
df_final.to_csv('aeroport_carthage.csv', sep='\t', na_rep="None", index=False, header=files_header)

