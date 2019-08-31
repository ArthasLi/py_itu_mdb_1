from freqHandle import freq_mergByNtcID,freq_overlap_by_arr
import numpy

class ntc_fq_band_ana():


    def __init__(self):
        self.fq_dict_ini = dict({'c': 0, 'ku': 0, 'ka': 0, 'qv': 0})


    def fq_ana(self, ntc_id):
        #e.g. id = 109520057
        ntc_fq_band = freq_mergByNtcID(ntc_id)
        BW_dict = dict()
        c_band = numpy.array([[3400, 4200], [5000, 6725]])
        Ku_band = numpy.array([[10700, 12750], [12750, 14500]])
        Ka_band = numpy.array([[17200, 21200], [24650, 27250], [27000, 31000]])
        QV_band = numpy.array([35000, 80000])
        fq_dict = dict(c=c_band,ku=Ku_band,ka=Ka_band,qv=QV_band)


        for key in fq_dict:
            overlap_fq = freq_overlap_by_arr(fq_dict[key],ntc_fq_band)
            BW = self.cal_bandwidth(overlap_fq)
            BW_dict.update({key:BW})

        return BW_dict

    def cal_bandwidth(self, fq):
        bw = 0
        for row in fq:
            bw = bw + row[1] - row[0]
            #print bw
        return bw

#a = ntc_fq_band_ana().fq_dict_ini
