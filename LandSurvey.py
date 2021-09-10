import os
import csv
from nmea.nmea_data import TALKER_ID, SENTENCE_ID
from nmea.sentences import parse_gga, parse_rmc, parse_gst

"""
Project:    PostProcessor
File:       Landsurvey.py
By:         JOR
Version:    0.1     25JUN21     Branch from Bathymetry tools, origins 2013
            0.2     07SEP21     Cut down for specific RTK processing only

This programme does post-processing of NMEA text files, extracting GPS data only
"""

this_programme = '[LandSurvey]'
output_file_name = ""


def save_csv(date_of_fix, gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3,sog, cmg, sigma_latitude, sigma_longitude, sigma_altitude):
    # First check if a CSV file has already been opened
    global output_file_name
    if output_file_name == "":
        output_file_name = './ProcessedData/summary.csv'
        print(f'[{this_programme}] Saving data as ' + output_file_name)
        # Now create the CSV file and headers
        output_file = open(output_file_name, 'w', newline='')
        with output_file:
            file_header = ['Date', 'UTC', 'Longitude', 'Latitude', 'Altitude', 'SOG', 'CMG', 'Sigma Latitude', 'Sigma Longitude', 'Sigma Altitude']
            writer = csv.writer(output_file)
            writer.writerow(file_header)

    # We have both a position data, append the line
    output_file = open(output_file_name, 'a', newline='')
    with output_file:
        line_data = [date_of_fix, gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3,sog, cmg, sigma_latitude, sigma_longitude, sigma_altitude]
        writer = csv.writer(output_file)
        writer.writerow(line_data)


def main():

    print('Utility to process NMEA 0183 v. 4.11 sentences for land survey')
    print('Expects sentences without $ symbol')
    print('GGA is processed for XYZ positions')
    print('RMC is processed for COG, SOG and date')
    print('GST is processed for XYZ accuracy')
    input('Press ENTER to continue...')

    # Set flags
    gga_valid = False
    rmc_valid = False
    gst_valid = False

    # Look through the raw data file
    directory = './RawData'
    # Open every file in sequence
    for file in os.listdir(directory):
        input_filename = './RawData/' + file
        print("Found" + input_filename)
        # Process each file individually
        with open(input_filename) as nmea_file:
            # one line at a time, parse
            for CurrentNMEAString in nmea_file:
                # Its a comma delimited file, split values into a list
                list_of_values = CurrentNMEAString.split(',')
                # Get the talker ID
                talker_id = list_of_values[0][0:-3]
                # Check to see if its in the list of valid talker IDs
                if talker_id in TALKER_ID:
                    sentence_id = list_of_values[0][2:]
                    # Check to see if its in the list of valid sentences for processing
                    if sentence_id in SENTENCE_ID:
                        try:
                            if sentence_id == 'GGA':
                                # Call a parsing function to get the required values
                                gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3, fix_quality = parse_gga(CurrentNMEAString)
                                # Only process RTK sentences
                                if fix_quality == '4':
                                    gga_valid = True
                            if sentence_id == 'RMC':
                                # Call a parsing function to get the required values
                                sog, cmg, date_of_fix, data_validity, pos_mode_indicator = parse_rmc(CurrentNMEAString)
                                # Only process RTK sentences
                                if pos_mode_indicator == 'R':
                                    rmc_valid = True
                            if sentence_id == 'GST':
                                # Call a parsing function to get the required values
                                sigma_latitude, sigma_longitude, sigma_altitude = parse_gst(CurrentNMEAString)
                                gst_valid = True
                        except ValueError:
                            print('[GPS-parse] Error parsing sentence')
                        finally:
                            if gga_valid and rmc_valid and gst_valid:
                                print(date_of_fix, gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3,sog, cmg, sigma_latitude, sigma_longitude, sigma_altitude, hdg)
                                save_csv(date_of_fix, gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3,sog, cmg, sigma_latitude, sigma_longitude, sigma_altitude)
                                # Reset flags
                                gga_valid = False
                                rmc_valid = False
                                gst_valid = False

                else:
                    print(f'Bad talker ID{talker_id}')


if __name__ == "__main__":
    main()
