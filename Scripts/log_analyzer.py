# The script analyzes the log near it and outputs performance info to console.
# Place this script near the path_to_file and just double click it
#
# Analyzer requires a specific log that contains:
# - profilegpu command
# - printed to log settings with Overall Scalability Settings
# - printed to log words in the same line: PROFILEGPU and {location_name}PerfCam

path_to_file = 'Example.log'


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

    def calculate_results(self):
        self.l_average_ms = self.l_total_ms / self.l_total_cameras
        self.l_average_fps = int(1000 / self.l_average_ms)

    def print_info(self):
        print(self.l_name, ': \n ', 'Average:', str(self.l_average_ms)[:5], 'ms,', self.l_average_fps, 'fps')


class Main:
    with open(path_to_file, 'r', encoding='utf8') as file:
        total_ms_array = []
        total_cameras_amount = 0
        locations_array = []
        current_location_name = ''
        locations_below_60fps = []
        locations_below_30fps = []
        settings_lines_numbers = [-1, -1]
        settings = []

        for line_number, line in enumerate(file):

            # get settings info
            if 'Overall' in line:
                # get next 9 lines indexes since they contain all settings
                settings_lines_numbers = [line_number+1, line_number + 9]
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

        # check if there is any information to print
        if len(total_ms_array) > 0:
            msTotalSum = 0
            for ms in total_ms_array:
                msTotalSum += ms
            total_average_ms = msTotalSum / len(total_ms_array)

            # print common info
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


input('Press any button to exit...')
