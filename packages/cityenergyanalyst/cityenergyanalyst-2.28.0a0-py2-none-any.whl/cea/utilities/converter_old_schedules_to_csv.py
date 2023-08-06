import csv
import os

import pandas as pd


def main():
    DAY = ['WEEKDAY'] * 24 + ['SATURDAY'] * 24 + ['SUNDAY'] * 24
    HOUR = range(1, 25) + range(1, 25) + range(1, 25)

    COLUMN_NAMES = ['DAY',
                    'HOUR',
                    'OCCUPANCY',
                    'APPLIANCES',
                    'LIGHTING',
                    'WATER',
                    'HEATING',
                    'COOLING',
                    'PROCESSES',
                    'SERVERS']

    path = r'C:\Users\JimenoF\Documents\CityEnergyAnalyst\CityEnergyAnalyst\cea\databases'

    for region, standard in zip(['CH', 'SG'], ['CH-SIA-2024', 'SG-ASHRAE-2009']):
        path_to_database = os.path.join(path, region, 'archetypes/occupancy_schedules.xlsx')
        xls = pd.ExcelFile(path_to_database)
        uses = xls.sheet_names
        for use in uses:
            occ = []
            appl =[]
            light =[]
            dhw = []
            cset = []
            hset = []
            pro = []
            server = []

            archetypes_schedules = pd.read_excel(path_to_database, use, index_col=0).T
            # read schedules from excel file
            occ.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_1'].values[:24]])
            occ.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_1'].values[:24]])
            occ.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_1'].values[:24]])

            appl.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_2'].values[:24]])
            appl.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_2'].values[:24]])
            appl.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_2'].values[:24]])

            light.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_2'].values[:24]])
            light.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_2'].values[:24]])
            light.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_2'].values[:24]])

            dhw.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_3'].values[:24]])
            dhw.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_3'].values[:24]])
            dhw.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_3'].values[:24]])

            cset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Weekday_4'].values[:24]])
            cset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Saturday_4'].values[:24]])
            cset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Sunday_4'].values[:24]])

            hset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Weekday_5'].values[:24]])
            hset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Saturday_5'].values[:24]])
            hset.extend([str(round(float(x), 2)) if type(x) is not unicode else x for x in
                         archetypes_schedules['Sunday_5'].values[:24]])
            x = 1
            if use in {"INDUSTRIAL", "HOSPITAL", "LAB"}:
                pro.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_6'].values[:24]])
                pro.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_6'].values[:24]])
                pro.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_6'].values[:24]])
            else:
                pro.extend([str(0.0) for x in range(24)])
                pro.extend([str(0.0) for x in range(24)])
                pro.extend([str(0.0) for x in range(24)])

            if use in {"SERVERROOM"}:
                server.extend([str(round(float(x), 2)) for x in archetypes_schedules['Weekday_2'].values[:24]])
                server.extend([str(round(float(x), 2)) for x in archetypes_schedules['Saturday_2'].values[:24]])
                server.extend([str(round(float(x), 2)) for x in archetypes_schedules['Sunday_2'].values[:24]])
            else:
                server.extend([str(0.0) for x in range(24)])
                server.extend([str(0.0) for x in range(24)])
                server.extend([str(0.0) for x in range(24)])



            METADATA = ['METADATA', standard, use]
            MULTIPLIER = ['MONTHLY_MULTIPLIER'] + [str(round(float(x), 2)) for x in archetypes_schedules['month'].values[:12]]
            PROFILE = [DAY, HOUR, occ, appl, light, dhw, hset, cset, pro, server]
            PROFILE_NEW = map(list, zip(*PROFILE))

            filename = os.path.join(path, 'schedules', standard, use + '.csv')
            with open(filename, "wb") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(METADATA)
                csvwriter.writerow(MULTIPLIER)
                csvwriter.writerow(COLUMN_NAMES)
                for row in PROFILE_NEW:
                    csvwriter.writerow(row)


if __name__ == '__main__':
    main()
