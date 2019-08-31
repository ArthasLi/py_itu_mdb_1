from sqlQry import sqlQry
import numpy
from op_BW_stt import find_ntc_id,dict_to_lst
from ntc_fq_band_ana_beta import fq_ana
from collections import Counter
import xlwt



class op_FandO:

    op_adm_qnt = None
    orb_var = None
    ntc_type = 'G'
    OP_lst = 'OP_lst'
    ntc_id_lst = []
    ntcId_long_data_pair = []
    full_data = []
    mdb_quant = 3

    def __init__(self,OP_name,y_s,y_e,ntf_rsn):
        self.op_adm_qnt = None
        self.orb_var = None
        self.OP_name = OP_name
        self.y_s = y_s
        self.y_e = y_e
        self.ntf_rsn = ntf_rsn
        self.ntc_type = 'G'
        self.OP_lst = 'OP_lst'
        self.ntc_id_lst = []
        self.ntcId_long_data_pair = []
        self.full_data = []


    def update_ntc_id_long_lst(self, mdb_idx):
        self.ntc_id_lst = []
        self.ntc_id_lst = find_ntc_id(self.OP_name, self.OP_lst, self.y_s, self.y_e, self.ntf_rsn, self.ntc_type, mdb_idx)
        print 'connected mdb file: mdb#'+str(mdb_idx)
        print 'ntc_id captured:'
        print self.ntc_id_lst
        self.ntc_id_lst = dict_to_lst(self.ntc_id_lst)
        self.find_ntc_long(self.ntc_id_lst, mdb_idx)

    def find_ntc_long(self, ntc_id_lst, mdb_idx):
        self.ntcId_long_data_pair = []
        for id in ntc_id_lst:
            qry = "SELECT  " \
                  "ntc_id, long_nom " \
                  "FROM " \
                  "com_el " \
                  "WHERE ntc_id = " + str(id)
            data = sqlQry(qry, mdb_idx)
            self.ntcId_long_data_pair.append(data)

    def cal_orb_seg_bw(self, seg_quant, mdb_idx):
        self.update_ntc_id_long_lst(mdb_idx)
        kk = self.ntcId_long_data_pair
        f_o_seg_info = []
        # f_o_HHI_info = dict(a_long_nom=1000, b_c=0, c_ku=0, d_ka=0, e_qv=0)
        # f_o_accBW_info = dict(a_long_nom=1001, b_c=0, c_ku=0, d_ka=0, e_qv=0)
        step = 360 / seg_quant

        for orb in range(-180, 180, step):
            f_o_seg_info.append(dict(a_long_nom=orb, b_c=0, c_ku=0, d_ka=0, e_qv=0))

        if kk.__len__() > 0:
            print '**********calculate mdb#:'+str(mdb_idx)+'  segment bw********'
            for info in f_o_seg_info:
                for item in self.ntcId_long_data_pair:
                    pair = item[0]
                    sample_orb_bw_info = fq_ana(pair[0], pair[1], mdb_idx)
                    if (sample_orb_bw_info['long_nom'] >= info['a_long_nom']) and (
                            sample_orb_bw_info['long_nom'] < (info['a_long_nom'] + step)):
                        print pair[0], pair[1]
                        info.update({'b_c': (info['b_c'] + sample_orb_bw_info['c'])})
                        info.update({'c_ku': (info['c_ku'] + sample_orb_bw_info['ku'])})
                        info.update({'d_ka': (info['d_ka'] + sample_orb_bw_info['ka'])})
                        info.update({'e_qv': (info['e_qv'] + sample_orb_bw_info['qv'])})
            print '********** mdb#:' + str(mdb_idx) + '  segment bw   completed!********'
        # add_dict = self.cal_HHI_accBW(f_o_seg_info, f_o_HHI_info, f_o_accBW_info)
        # for i in range(0, add_dict.__len__(), 1):
        #     f_o_seg_info.append(add_dict[i])
        return f_o_seg_info

    def merg_bw_all_mdb(self, bw_ini, bw_data):

        for ini_key in bw_ini:
            for bw_key in bw_data:
                for seg_bw_key in bw_key:
                    if ini_key['a_long_nom'] == seg_bw_key['a_long_nom']:
                        ini_key.update({'b_c': (ini_key['b_c'] + seg_bw_key['b_c'])})
                        ini_key.update({'c_ku': (ini_key['c_ku'] + seg_bw_key['c_ku'])})
                        ini_key.update({'d_ka': (ini_key['d_ka'] + seg_bw_key['d_ka'])})
                        ini_key.update({'e_qv': (ini_key['e_qv'] + seg_bw_key['e_qv'])})
        return bw_ini


    def FO_orb_seg_ana(self, seg_quant):
        f_o_seg_bw_ini = []
        f_o_seg_bw_srsPercent = []
        f_o_seg_mutli_mdb = []
        f_o_seg_info_all_mdb = []
        f_o_seg_bw_all_mdb = []
        for orb in range(-180, 180, 360/seg_quant):
            f_o_seg_bw_ini.append(dict(a_long_nom=orb, b_c=0, c_ku=0, d_ka=0, e_qv=0))
            f_o_seg_bw_srsPercent.append(dict(a_long_nom=orb, b_c=0, c_ku=0, d_ka=0, e_qv=0))

        for mdb_idx in range(0,self.mdb_quant,1):
            temp_seg_info = self.cal_orb_seg_bw(seg_quant, mdb_idx)
            f_o_seg_mutli_mdb.append(temp_seg_info)
            f_o_accBW_info = dict(a_long_nom='mdb_type'+str(mdb_idx), b_c=0, c_ku=0, d_ka=0, e_qv=0)
            f_o_seg_bw_all_mdb.append(self.cal_accBW(temp_seg_info,f_o_accBW_info))
        f_o_seg_info_all_mdb = self.merg_bw_all_mdb(f_o_seg_bw_ini, f_o_seg_mutli_mdb)


        f_o_HHI_info = dict(a_long_nom='HHI', b_c=0, c_ku=0, d_ka=0, e_qv=0)
        f_o_accBW = dict(a_long_nom='acc_BW', b_c=0, c_ku=0, d_ka=0, e_qv=0)
        f_o_seg_bw_srsPercent = self.cal_srs_percent(f_o_seg_mutli_mdb[0], f_o_seg_bw_srsPercent, f_o_seg_mutli_mdb)
        add_dict = self.cal_HHI_accBW(f_o_seg_info_all_mdb, f_o_HHI_info, f_o_accBW)
        for i in range(0, add_dict.__len__(),1):
            f_o_seg_info_all_mdb.append(add_dict[i])
        for item in f_o_seg_bw_all_mdb:
            #kk = self.cal_bw_type_percent(item,add_dict[0])
            f_o_seg_info_all_mdb.append(self.cal_bw_type_percent(item,add_dict[0]))
        for item in f_o_seg_bw_srsPercent:
            f_o_seg_info_all_mdb.append(item)
        return f_o_seg_info_all_mdb
    def cal_srs_percent(self, srs_data, multi_mdb_bw_ini, multi_mdb_data):
        print 'calculate srs percent dict matrix'
        for multi_mdb_bw in multi_mdb_bw_ini:
            for bw_key in multi_mdb_data:
                for seg_bw_key in bw_key:
                    cnt = 0
                    if multi_mdb_bw['a_long_nom'] == seg_bw_key['a_long_nom']:
                        multi_mdb_bw.update({'b_c': (multi_mdb_bw['b_c'] + seg_bw_key['b_c'])})
                        multi_mdb_bw.update({'c_ku': (multi_mdb_bw['c_ku'] + seg_bw_key['c_ku'])})
                        multi_mdb_bw.update({'d_ka': (multi_mdb_bw['d_ka'] + seg_bw_key['d_ka'])})
                        multi_mdb_bw.update({'e_qv': (multi_mdb_bw['e_qv'] + seg_bw_key['e_qv'])})
            for item in srs_data:
                if item['a_long_nom'] == multi_mdb_bw['a_long_nom']:
                    for srs_key in item:
                        if (srs_key != 'a_long_nom') and (item[srs_key] > 0):
                            item[srs_key] = item[srs_key]/multi_mdb_bw[srs_key]
                # for srs_key in item:
                #     if multi_mdb_bw['a_long_nom'] == srs_key['a_long_nom']:
                #         if srs_key['b_c'] > 0:
                #             srs_key['b_c'] = srs_key['b_c']/multi_mdb_bw['b_c']
                #         if srs_key['c_ku'] > 0:
                #             srs_key['c_ku'] = srs_key['c_ku']/multi_mdb_bw['c_ku']
                #         if srs_key['d_ka'] > 0:
                #             srs_key['d_ka'] = srs_key['b_c']/multi_mdb_bw['d_ka']
                #         if srs_key['e_qv'] > 0:
                #             srs_key['e_qv'] = srs_key['b_c']/multi_mdb_bw['e_qv']


        return srs_data


    def cal_bw_type_percent(self,sub_bw,all_bw):
        for key in sub_bw:
            if key != 'a_long_nom':
                if sub_bw[key] > 0:
                    sub_bw[key] = sub_bw[key]/all_bw[key]
        return sub_bw

    def cal_HHI_accBW(self, data, f_o_HHI_info, f_o_accBW_info):
        cnt = 0
        HHI_entry = []
        HHI = [0, 0, 0, 0]
        acc_BW = [0, 0, 0, 0]
        for item in data:
            acc_BW[0] = item['b_c'] + acc_BW[0]
            acc_BW[1] = item['c_ku'] + acc_BW[1]
            acc_BW[2] = item['d_ka'] + acc_BW[2]
            acc_BW[3] = item['e_qv'] + acc_BW[3]
            HHI_entry.append([item['b_c'],item['c_ku'],item['d_ka'],item['e_qv']])
        HHI_entry = numpy.array(HHI_entry)
        for i in range(0, HHI.__len__(),1):
            clm = HHI_entry[:,i]
            print clm
            if acc_BW[i] == 0:
                clm = [0, 0, 0, 0]
            else:
                clm = clm/acc_BW[i]*100
            HHI[i] = sum([x*y for x,y in zip(clm,clm)])
        f_o_HHI_info['b_c'] = HHI[0]
        f_o_HHI_info['c_ku'] = HHI[1]
        f_o_HHI_info['d_ka'] = HHI[2]
        f_o_HHI_info['e_qv'] = HHI[3]

        f_o_accBW_info['b_c'] = acc_BW[0]
        f_o_accBW_info['c_ku'] = acc_BW[1]
        f_o_accBW_info['d_ka'] = acc_BW[2]
        f_o_accBW_info['e_qv'] = acc_BW[3]

        return [f_o_accBW_info, f_o_HHI_info]

    def cal_accBW(self, data, f_o_accBW_info):
        cnt = 0
        acc_BW = [0, 0, 0, 0]
        for item in data:
            acc_BW[0] = item['b_c'] + acc_BW[0]
            acc_BW[1] = item['c_ku'] + acc_BW[1]
            acc_BW[2] = item['d_ka'] + acc_BW[2]
            acc_BW[3] = item['e_qv'] + acc_BW[3]
        f_o_accBW_info['b_c'] = acc_BW[0]
        f_o_accBW_info['c_ku'] = acc_BW[1]
        f_o_accBW_info['d_ka'] = acc_BW[2]
        f_o_accBW_info['e_qv'] = acc_BW[3]

        return f_o_accBW_info

    def FO_ana(self):
        long_lst = self.dict_to_lst_n_col(self.ntcId_long_data_pair, 1)
        C = Counter(long_lst)
        f_o_info = []
        for orb in C:
            f_o_info.append(dict(a_long_nom=orb, b_c=0, c_ku=0, d_ka=0, e_qv=0))

        for item in self.ntcId_long_data_pair:
            pair = item[0]
            self.full_data.append(fq_ana(pair[0], pair[1]))

        for info in f_o_info:
            for item in self.full_data:
                a = info
                aa = item
                if info['a_long_nom'] == item['long_nom']:
                    info.update({'b_c': (info['b_c'] + item['c'])})
                    info.update({'c_ku': (info['c_ku'] + item['ku'])})
                    info.update({'d_ka': (info['d_ka'] + item['ka'])})
                    info.update({'e_qv': (info['e_qv'] + item['qv'])})
        return f_o_info
    def dict_to_lst_n_col(self,dict,n):
        lst = []
        for layer in dict:
            for id in layer:
                lst.append(id[n])
        return lst
    def xls_output(self, data, sheetName):
        if data.__len__() != 0:
            key_lst = list(data[0].keys())
            key_lst.sort()
            bk = xlwt.Workbook(encoding='utf-8')
            newsh = bk.add_sheet(sheetName)
            xls_count = 0
            for item in key_lst:
                newsh.write(0,xls_count,item)
                xls_count = xls_count + 1
            xls_count = 0

            for item in data:
                tuple_item = sorted(item.iteritems(), key=lambda d: d[0], reverse=False)

                for i in range(0,tuple_item.__len__(),1):
                    a = tuple_item[i][1]
                    newsh.write(xls_count+1, i, tuple_item[i][1])
                xls_count = xls_count + 1
            bk.save(sheetName+'.xls')


# a = op_FandO('SES',2013,2014,'N')
# a.FO_orb_seg_ana(12)
# for i in range (2003,2019,3):
#     a = op_FandO('SES',1990,i,'N')
#     a.find_ntc_long(a.ntc_id_lst)
#     data = a.FO_orb_seg_ana(12)
#     print 'SES seg '+str(i)
#     a.xls_output(data,'SES'+str(i))
