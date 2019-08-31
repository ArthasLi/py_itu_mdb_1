from freqHandle import freq_mergByNtcID,freq_overlap_by_arr
import numpy



def fq_ana(ntc_id, long_nom, mdb_idx):
    #e.g. id = 109520057
    fq_dict_ini = dict({'c': 0, 'ku': 0, 'ka': 0, 'qv': 0})
    ntc_fq_band = freq_mergByNtcID(ntc_id, mdb_idx)
    BW_dict = dict()
    c_band = numpy.array([[3400, 4200], [4500, 4800], [5850, 7025]])
    Ku_band = numpy.array([[10700, 12750], [12750, 13250], [13750, 14800], [17300, 17699]])
    Ka_band = numpy.array([[17700, 21200], [24650, 31000]])
    QV_band = numpy.array([35000, 80000])
    # if mdb_idx == 2:
    #     c_band = numpy.array([[3400, 4200], [5000, 6725]])
    #     Ku_band = numpy.array([[10700, 12750], [12750, 13250], [13750, 14800], [17300, 17800]])
    #     Ka_band = numpy.array([[17800, 21200], [24650, 27250], [27000, 31000]])
    #     QV_band = numpy.array([35000, 80000])
    #     # c_BW = 2525
    #     # Ku_BW = 3800
    #     # Ka_BW = 10600
    #     # QV_BW = 45000
    # else:
    #     c_band = numpy.array([[3400, 4200], [5000, 6725]])
    #     Ku_band = numpy.array([[10700, 12750], [12750, 13250], [13750, 14800]])
    #     Ka_band = numpy.array([[17200, 21200], [24650, 27250], [27000, 31000]])
    #     QV_band = numpy.array([35000, 80000])
    #     # c_BW = 2425
    #     # Ku_BW = 3800
    #     # Ka_BW = 10600
    #     # QV_BW = 45000

    fq_dict = dict(c=c_band, ku=Ku_band, ka=Ka_band, qv=QV_band)
    # fq_BW_dic = dict(c=c_BW, ku=Ku_BW, ka=Ka_BW, qv=QV_BW)
    for key in fq_dict:
        overlap_fq = freq_overlap_by_arr(fq_dict[key],ntc_fq_band)
        BW = cal_bandwidth(overlap_fq)
        # BW_percentage = round(BW/fq_BW_dic[key],4)
        BW_dict.update({key:BW})

    BW_dict['ntc_id'] = ntc_id
    BW_dict['long_nom'] = long_nom
    array = (BW_dict['long_nom'],BW_dict['c'],BW_dict['ku'],BW_dict['ka'],BW_dict['qv'])
    # BW_dict contains long_nom, ntc_id, c, ku, ka, qv
    return BW_dict

def cal_bandwidth(fq):
    bw = 0
    for row in fq:
        bw = bw + row[1] - row[0]
        #print bw
    return bw

#a = ntc_fq_band_ana().fq_dict_ini


