from ITU_mdb_query import ITU_mdb_query
from freqHandle import freq_merg
from freqHandle import freq_overlap_by_id_arr
import numpy
import re


class IFIC_handler:

    def __init__(self, adm, agcy_id, wic_no):
        self.adm = adm
        self.agcy_id = agcy_id
        self.wic_no = wic_no

    def find_ntc_list(self):
        find_lst = ITU_mdb_query()

        return find_lst.find_ntc_lst_byOP(self.adm, self.agcy_id)

    def check_prov_9d11(self, ntc_id):
        prov_9d11_band = numpy.loadtxt('911fq').tolist()
        prov_9d11_band = freq_merg(prov_9d11_band)
        #x_band = [(2000, 2041),(17000, 21000)]
        ini = ITU_mdb_query()
        ntc_9d11_band = freq_overlap_by_id_arr(ntc_id, prov_9d11_band)
       #ntc_9d11_band = freq_overlap_by_id_arr(ntc_id, x_band)
        if ntc_9d11_band.__len__() == 1:
            #print ('Yes')
            a = 1
        else:
            #print('No')
            ntc_date = ini.find_d_rcv(ntc_id)
            raw_lst = ini.find_co_ntc_byWIC(self.wic_no, self.adm, ntc_date)
            for row in raw_lst:
                raw_lst



