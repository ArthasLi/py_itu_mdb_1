from scipy.io import loadmat
from freq_band_cat import band_bank
import numpy

def cal_indx(band_density_map_file_name, map_fq_pnts, wanted_band, band_res):
    map = loadmat(band_density_map_file_name)
    # wanted_fq_pnts = find_wanted_pnts(wanted_band, band_res)
    wanted_fq_pnts = map_fq_pnts

    re = cal_bw_den(map[band_density_map_file_name])


def cal_bw_den(map):
    map
    c = map[:,1]
    a = numpy.std(c)
    map_dim = map.shape
    density = []
    for orb_i in range(map_dim[0]):
        density_i = 0
        for fq_j in range(map_dim[1]):
            density_i = density_i + map[orb_i,fq_j]
        density.append(density_i)
    min = pow(pow(density[0],2) + pow(numpy.std(map[0,:]),2), 0.5)
    min_i = 0
    for i in range(density.__len__()):
        if density[i]:
            ind_i = pow(pow(density[i],2) + pow(numpy.std(map[i,:]),2), 0.5)
            if min > ind_i:
                min = ind_i
                print min, min_i
                min_i = i
    density = numpy.ndarray(density)
    map

def find_wanted_pnts(band_type, band_res):
    band_seg = band_bank(band_type)
    seg_shape = band_seg.shape.__len__()
    fq_pnts = []
    final_fq_pnts = []
    if seg_shape > 1:
        for i in range(0, seg_shape + 1):
            max_min_pair = band_seg[i]
            fq_pnts = numpy.arange(max_min_pair[0], max_min_pair[1] + band_res, band_res)
            final_fq_pnts = numpy.concatenate((final_fq_pnts, fq_pnts), axis=None)

    else:
        final_fq_pnts = numpy.arange(band_seg[0], band_seg[1] + band_res, band_res)
    return final_fq_pnts

