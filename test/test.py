from op_BW_stt import op_accmlt_BW_stt
from ITU_mdb_query import ITU_mdb_query
from freqHandle import freq_mergByNtcID
import numpy as np
import freqHandle as fh
import ntc_fq_band_ana
from op_FandO import op_FandO
import datetime
import numpy as np
from scipy.io import loadmat
import fq_orb_consume
from matplotlib import pyplot as plt

if __name__ == "__main__":
     band_res = 10
     a = fq_orb_consume.cal_indx('raw_data',[1,2], 'Unplan Ku R3',band_res)

    # orb_seg = [90,100]
    # OP_lst = 'OP_lst'
    # band_type = 'Ku'
    # y_s = 2000
    # y_e = 2010
    # ntf_rsn = 'N'
    # a = freq_orb_ind(orb_seg, band_type,y_s,y_e,ntf_rsn,0.5,50)
     # opName = 'EUTELSAT'
     # a = op_FandO(opName, 2000, 2010, 'N')
     # data = a.FO_orb_seg_ana(12)
     # a.xls_output(data, opName+'2010')

     #print freq_mergByNtcID(114560008,2)
    # a = ITU_mdb_query()
    # data = a.find_adm_opID_by_ntcID(111570002)
    # print data

    # year_s = 1990
    # year_d = [2000, 2005, 2010, 2015, 2019]
    # name = 'INTELSAT'
    # for year in year_d:
    #     a = op_FandO(name, year_s, year, 'N')
    #     data = a.FO_orb_seg_ana(12)
    #     print name + str(year)
    #     a.xls_output(data, name + str(year))

    # dict_test()
    #fq = freq_mergByNtcID(92500137)
   # fq1 = freq_mergByNtcID(109500200)
   #  lst = op_accmlt_BW_stt(2007, 2018, 'OP_lst', 'N', 'G')
   #  lst
    # op_BW_stt(2008,2009,'OP_lst', 'N', 'G')
    # op_ntcid_dict, op_ntc_qnt_dict = op_annual_ntcQnt_ntcID('SES', 'OP_lst',2011, 'C', 'G')
    #bw_data = op_BW_stt(2006, 2012, 'OP_lst', 'N', 'G')
    #bw_data