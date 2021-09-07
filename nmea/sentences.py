def parse_gga(sentence):
    # GNGGA,120113.00,5510.0019168,N,00726.0946454,W,4,12,0.60,109.635,M,53.911,M,1.0,0000*73
    #
    # 1 - Fix taken at in UTC as hhmmss.ss
    # 2 - Latitude (Northing) in DM
    # 3 - NS Hemisphere
    # 4 - Longitude (Easting) in DM
    # 5 - EW Hemisphere
    # 6 - Fix quality, see GGA_Quality
    # 7 - Number of satellites being tracked
    # 8 - Horizontal dilution of position (HDOP)
    # 9 - Altitude, Metres, above mean sea level
    # 10 - Altitude Unit
    # 11 - Separation of geoid between mean sea level and WGS84 ellipsoid()
    # 12 - Separation Unit
    # 13 - Time in seconds since last DGPS update, SC104
    # 14 - DGPS station ID number

    # Default, invalid fix
    fix_quality = '0'
    gps_time = ''
    dd_longitude_degrees = 0
    dd_latitude_degrees = 0
    altitude3 = 0

    try:
        list_of_values = sentence.split(',')
        gps_time = list_of_values[1]

        # Get the decimal degree values of position
        latitude_dm = (list_of_values[2])
        dd_latitude_degrees = latitude_dm_to_dd(latitude_dm)

        # Longitude converts to negative, edit this if working east of Greenwich
        longitude_dm = (list_of_values[4])
        dd_longitude_degrees = longitude_dm_to_dd(longitude_dm)

        # To get the true altitude, add height above MSL to HoG and then convert to OSGM15 externally.
        msl = list_of_values[9]
        hog = list_of_values[11]
        altitude = float(msl) + float(hog)
        # Limit to 3 decimal places (mm)
        altitude3 = round(altitude, 3)

        # Verify the quality of the solution
        number_satellites_tracked = list_of_values[7]
        fix_quality = list_of_values[6]

    except ValueError:
        print(f'[GGA] Error parsing {sentence}')

    return gps_time, dd_longitude_degrees, dd_latitude_degrees, altitude3, fix_quality


def parse_rmc(sentence):
    # RMC - Recommended minimum specific GPS/Transit data
    # GNRMC,120112.00,A,5510.0019172,N,00726.0946444,W,0.017,,070921,,,R,V*1E
    # 1 - Fix taken at in UTC as hhmmss.ss
    # 2 - Data validity, A=Valid, V=Invalid
    # 2 - Latitude (Northing) in DM
    # 3 - NS Hemisphere
    # 4 - Longitude (Easting) in DM
    # 5 - EW Hemisphere
    # 7 - Speed over ground in Knots
    # 8 - Course Made Good in Degrees, True
    # 9 - Date of fix DDMMYY
    # 10 - Magnetic variation
    # 11 - Magnetic variation hemisphere
    # 12 - posMode indicator (from NMEA 2.3 onwards)
    # 13 - navStatus, fixed field (from NMEA 4.1 onwards), always V

    # Default, invalid fix
    data_validity = 'V'

    # Return values
    pos_mode_indicator = 'N'
    sog = '0'
    cmg = '0'
    date_of_fix = ''

    try:
        list_of_values = sentence.split(',')
        data_validity = list_of_values[2]
        sog = (list_of_values[7])
        cmg = (list_of_values[8])
        date_of_fix = (list_of_values[9])
        pos_mode_indicator = (list_of_values[12])
    except ValueError:
        print(f'[RMC] Error parsing {sentence}')

    return sog, cmg, date_of_fix, data_validity, pos_mode_indicator


def parse_gst(sentence):
    # GNSS pseudorange error statistics
    # GNGST, 120112.00, 34, 0.011, 0.0065, 38, 0.010, 0.010, 0.010 * 76
    # 1 - Fix taken at in UTC as hhmmss.ss
    # 2 - RMS value of the standard deviation of the ranges
    # 3 - Standard deviation of semi-major axis
    # 4 - Standard deviation of semi-minor axis
    # 5 - Orientation of semi-major axis
    # 6 - Standard deviation of latitude error
    # 7 - Standard deviation of longitude error
    # 8 - Standard deviation of altitude error

    # Return values
    sigma_latitude = '0'
    sigma_longitude = '0'
    sigma_altitude = '0'

    try:
        list_of_values = sentence.split(',')
        sigma_latitude = list_of_values[6]
        sigma_longitude = list_of_values[7]
        sigma_altitude_and_crc = list_of_values[8].split('*')
        sigma_altitude = sigma_altitude_and_crc[0]
    except ValueError:
        print(f'[GST] Error parsing {sentence}')

    return sigma_latitude, sigma_longitude, sigma_altitude


def longitude_dm_to_dd(longitude_dm):
    '''
    Convert position in the format DDMM.mmmmmm to DD.ddddddd
    :param longitude_dm:
    :return: longitude in decimal degrees
    '''
    dm_longitude_degrees = int(longitude_dm[0:3])
    dm_longitude_minutes = float(longitude_dm[3:])
    dm_longitude_minutes_fraction = float(dm_longitude_minutes / 60)
    return round(-dm_longitude_degrees - dm_longitude_minutes_fraction, 8)


def latitude_dm_to_dd(latitude_dm):
    '''
    Convert position in the format DDMM.mmmmmm to DD.ddddddd
    :param latitude_dm:
    :return: latitude in decimal degrees
    '''
    dm_latitude_degrees = int(latitude_dm[0:2])
    dm_latitude_minutes = float(latitude_dm[2:])
    dm_latitude_minutes_fraction = float(dm_latitude_minutes / 60)
    return round(dm_latitude_degrees + dm_latitude_minutes_fraction, 8)
