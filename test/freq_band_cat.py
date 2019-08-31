import numpy
def band_bank(band_type):
    band = None
    if band_type == 'C':
        band = numpy.array([[3400, 4200], [4500, 4800], [5850, 7025]])
    if band_type == 'Ku':
        band = numpy.array([[10700, 12750], [12750, 13250], [13750, 14800], [17300, 17699]])
    if band_type == 'Ka':
        band = numpy.array([[17700, 21200], [24650, 31000]])
    if band_type == 'Unplan Ku R3':
        band = numpy.array([[10950, 11200], [11450, 11700], [12500, 12750], [13400, 13600], [13750, 14750]])
    if band_type == 'QV':
        band = numpy.array([35000, 80000])
    return band