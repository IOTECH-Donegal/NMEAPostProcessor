'''
Various tables of data from UBlox documentation
'''

TALKER_ID = {
    'GN': 'GNSS Device'
}

SENTENCE_ID = {
    'RMC': 'Recommended minimum data',
    'GGA': 'Global positioning system fix data',
    'GST': 'GNSS pseudorange error statistics'
}

GGA_Quality = {
    '0': 'No position',
    '4': 'RTK Fixed',
    '5': 'RTK Float',
    '6': 'Dead Reckoning'
}

RMC_PosMode = {
    'N': 'No fix',
    'E': 'Estimated/dead reckoning fix',
    'A': 'autonomous GNSS fix',
    'D': 'Differential GNSS fix',
    'F': 'RTK float',
    'R': 'RTK fixed'
}
