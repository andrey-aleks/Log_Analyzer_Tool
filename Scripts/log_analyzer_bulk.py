# The same as the log_analyzer, but it outputs a bunch of CSV tables for each log down in folders.
# Place this script near the all specs folders and just double click it.
#
# Analyzer requires a specific log that contains:
# - profilegpu command
# - printed to log settings with Overall Scalability Settings
# - printed to log words in the same line: PROFILEGPU and {location_name}PerfCam
#
# Also it takes the name of the specs & settings folders, so keep it in mind

import os
import csv
from pathlib import Path

filename = 'Example.log'
profile_data_array = []


# class for unique data for each log
class LogData:
    log_specs = ''
    log_settings = ''

    # set log data
    def set_data(self, path):
        self.log_specs = Path(path).parent.parent.parent.name
        self.log_settings = Path(path).parent.parent.name.split('_Saved')[0].split('_')[1]


# class for unique data for each location in log
class LocationData:
    l_name = ''
    l_total_cameras = 0
    l_total_ms = 0
    l_average_ms = 0
    l_average_fps = 0

    def __init__(self, location_name, total_cameras, total_ms):
        self.l_name = location_name
        self.l_total_cameras = total_cameras
        self.l_total_ms = total_ms

    # calculate average MS and FPS for a location
    def calculate_results(self):
        self.l_average_ms = float(str(self.l_total_ms / self.l_total_cameras)[:5])
        self.l_average_fps = int(1000 / self.l_average_ms)

    def print_info(self):
        print(self.l_name, ': \n ', 'Average:', str(self.l_average_ms)[:5], 'ms,', self.l_average_fps, 'fps')


class Main:
    for subdir, dirs, files in os.walk(os.getcwd()):
        for file in files:
            file_path = os.path.join(subdir, file)
            # check if log is in the Logs folder & named properly
            if file == filename and Path(file_path).parent.name == 'Logs':

                # add new log data object & fill it
                profile_data_array.append(LogData())
                current_log_data = profile_data_array[-1]
                current_log_data.set_data(file_path)

                # main parameters for each log
                total_ms_array = []
                total_cameras_amount = 0
                locations_array = []
                current_location_name = ''
                locations_below_60fps = []
                locations_below_30fps = []
                settings_lines_numbers = [-1, -1]
                settings = []

                with open(file_path, "r") as f:
                    for line_number, line in enumerate(f):

                        # get settings info
                        if 'Overall' in line:
                            # get next 9 lines indexes since they contain all settings
                            settings_lines_numbers = [line_number + 1, line_number + 9]
                        if settings_lines_numbers[0] <= line_number <= settings_lines_numbers[1]:
                            settings.append(line)

                        # get all data
                        if 'PerfCam' in line and 'PROFILEGPU' in line:
                            current_location_name = line.split('(')[1].split('PerfCam')[0]
                            total_cameras_amount += 1
                        if "total GPU time " in line:
                            msString = line.split('total GPU time ')[1].split('ms')[0]
                            msFloat = float(msString)
                            total_ms_array.append(msFloat)
                            if len(locations_array) > 0:
                                value_assigned = False
                                for loc in locations_array:
                                    if loc.l_name == current_location_name:
                                        # increase amount of cameras & ms
                                        loc.l_total_cameras += 1
                                        loc.l_total_ms += msFloat
                                        value_assigned = True
                                        break
                                if not value_assigned:
                                    # create new instance of class & add it to array
                                    locations_array.append(LocationData(current_location_name, 1, msFloat))
                            else:
                                # create new instance of class & add it to array
                                locations_array.append(LocationData(current_location_name, 1, msFloat))

                    # check if there is any information to output
                    if len(total_ms_array) > 0:
                        msTotalSum = 0
                        for ms in total_ms_array:
                            msTotalSum += ms
                        total_average_ms = msTotalSum / len(total_ms_array)
                        locations_array.append(LocationData('Total', total_cameras_amount, msTotalSum))

                        # print common info
                        print(current_log_data.log_specs, current_log_data.log_settings)
                        print('Settings:\n 0 - Very Low, 1 - Low, 2 - Medium, 3 - High, 4 - Very High')
                        for set in settings:
                            print(set.strip())
                        print('\n')

                        print('Total amount of cameras:', total_cameras_amount)
                        print('Total average ms:', str(total_average_ms)[:5])
                        print('Total average fps:', int(1000 / total_average_ms))

                        # print locations info
                        for location in locations_array:
                            location.calculate_results()
                            if location.l_average_fps < 60:
                                locations_below_60fps.append(location)
                                if location.l_average_fps < 30:
                                    locations_below_30fps.append(location)
                            location.print_info()
                        print('\n')
                        print('Locations below 60 FPS:', len(locations_below_60fps), '/', len(locations_array))
                        for location in locations_below_60fps:
                            location.print_info()
                        print('\n')
                        print('Locations below 30 FPS:', len(locations_below_30fps), '/', len(locations_array))
                        for location in locations_below_30fps:
                            location.print_info()
                        print('\n')
                    else:
                        print('File doesn`t contain profilegpu information!')

                # create CSV file for each log
                with open(current_log_data.log_specs + '_' + current_log_data.log_settings + '.csv', 'w',
                          encoding='UTF8', newline='') as f:
                    # csv header
                    fieldnames = ['Specs', 'Settings', 'Location', 'Average MS', 'Average FPS']
                    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()

                    # csv data
                    rows = []
                    for loc in locations_array:
                        rows.append({'Specs': current_log_data.log_specs,
                                     'Settings': current_log_data.log_settings,
                                     'Location': loc.l_name,
                                     # replace() is a workaround for Excel
                                     'Average MS': str(loc.l_average_ms).replace('.', ','),
                                     'Average FPS': loc.l_average_fps})
                    writer.writerows(rows)


input('Press any button to exit...')