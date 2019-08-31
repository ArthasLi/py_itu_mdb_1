from ntc_fq_band_ana import ntc_fq_band_ana
from ITU_mdb_query import ITU_mdb_query
import re
from collections import Counter
import csv

# all mdb query need add one more var mdb_idx to identify SRS, AP_30 and SPA_ALL
def dict_test():
    op_bw_dict = {'SES':{'C':'100','Ku':'300'}}
    op_bw_dict['Satcom'] = {'C': '1100', 'Ku': '1300'}
    w = csv.writer(open("output.csv","w"))
    for key, val in op_bw_dict.items():
        w.writerow([key,val])
    op_bw_dict

def op_accmlt_BW_stt(year_start,year_end,OP_lst, ntf_rsn, ntc_type):
    with open(OP_lst) as f:
        con_lst = f.readlines()
    op_counter = find_op_lst(con_lst)
    op_BW_stt_lst = []
    op_accmlt_BW_stt_lst = []

    accmlt_stt_year = str(year_start - 1)

    op_accmlt_bw_dict = dict()

    for i in range(year_start, year_end, 1):
        #cnt = cnt + 100
        year = str(i)
        op_accmlt_bw_dict = dict()
        for op in op_counter:

            [op_ntcid_lst, op_ntc_qnt] = op_accmlt_ntcIDlst_ntcQnt_dict(op, OP_lst, year, ntf_rsn, ntc_type)
            print op_ntcid_lst
            print op_ntc_qnt
            ntc_lst = dict_to_lst(op_ntcid_lst)
            temp_bw = ntclst_BW_stt(ntc_lst)
            op_accmlt_bw_dict.update({op:temp_bw})
            print op_accmlt_bw_dict


        op_accmlt_BW_stt_lst.append(op_accmlt_bw_dict)
    return op_accmlt_BW_stt_lst


def adm_accmlt_BW_stt(year_start, year_end, adm_lst, ntf_rsn, ntc_type):
    with open(adm_lst) as f:
        con_lst = f.readlines()
    adm_counter = find_op_lst(con_lst)
    adm_BW_stt_lst = []
    adm_accmlt_BW_stt_lst = []

    accmlt_stt_year = str(year_start - 1)

    op_accmlt_bw_dict = dict()

    for i in range(year_start, year_end, 1):
        #cnt = cnt + 100
        year = str(i)
        adm_accmlt_bw_dict = dict()
        for adm in adm_counter:
            #adm_ntcid_lst = ITU_mdb_query().find_accmlt_ntc_lst_by_adm(adm, year, ntf_rsn, ntc_type)
            #adm_ntcid_lst = ITU_mdb_query().find_annual_ntc_lst_by_adm(adm, year, ntf_rsn, ntc_type)
            adm_ntcid_lst = ITU_mdb_query().find_lastDec_accmlt_ntc_lst_by_adm(adm, year, ntf_rsn, ntc_type)
            temp_bw = ntc_lst_BW_stt(adm_ntcid_lst)
            adm_accmlt_bw_dict.update({adm:temp_bw})
            print (year,adm,temp_bw)

        adm_accmlt_BW_stt_lst.append(op_accmlt_bw_dict)
    return adm_accmlt_BW_stt_lst



def op_BW_stt(year_start,year_end,OP_lst, ntf_rsn, ntc_type):
    with open(OP_lst) as f:
        con_lst = f.readlines()
    op_counter = find_op_lst(con_lst)
    op_BW_stt_lst = []


    w = csv.writer(open("output.csv", "w"))

    for i in range(year_start, year_end, 1):
        #cnt = cnt + 100
        year = str(i)
        op_bw_dict = dict()
        print i
        for op in op_counter:

            [op_ntcid_lst, op_ntc_qnt_lst] = op_annual_ntcQnt_ntcID(op, OP_lst, year, ntf_rsn, ntc_type)
            print op_ntcid_lst
            temp_bw = ntclst_BW_stt(op_ntcid_lst)

            op_bw_dict.update({op:temp_bw})

        for op in op_bw_dict:
            w.writerow([op, op_bw_dict[op]])
        op_BW_stt_lst.append(op_bw_dict)
    return op_BW_stt_lst

def dict_to_lst(dict):
    ntc_lst = []
    for layer in dict:
        for id in layer:
            ntc_lst.append(id[0])
    return ntc_lst



def ntclst_BW_stt(op_ntcid_lst):
    #using class's gloable var will interfere other key:value, get 2 instance of the same class, and using global var,
    #key:value confusing
    fq_ana = ntc_fq_band_ana()
    op_annual_BW = fq_ana.fq_dict_ini

    for id in op_ntcid_lst:
        bw = fq_ana.fq_ana(id)
        for sub_band in bw:
            new_bw = op_annual_BW[sub_band] + bw[sub_band]
            op_annual_BW.update({sub_band: new_bw})
    return op_annual_BW

def ntc_lst_BW_stt(op_ntcid_lst):
    fq_ana = ntc_fq_band_ana()
    op_annual_BW = fq_ana.fq_dict_ini
    if op_ntcid_lst.__len__()>0:
        for id in op_ntcid_lst:
            bw = fq_ana.fq_ana(id[0])
            for sub_band in bw:
                new_bw = op_annual_BW[sub_band] + bw[sub_band]
                op_annual_BW.update({sub_band: new_bw})



    return op_annual_BW

def op_annual_ntcQnt_ntcID(key, OP_lst,year,ntf_rsn,ntc_type):
    op_ntcid_dict = dict()
    op_ntc_qnt_dict = dict()
    op_ntcid_dict.update({key:find_ntc_id(key,OP_lst,year,ntf_rsn,ntc_type)})
    if op_ntcid_dict[key].__len__() > 0:
        op_ntc_qnt_dict.update({key: op_ntcid_dict[key][0].__len__()})
    else:
        op_ntc_qnt_dict.update({key: 0})

    return op_ntcid_dict[key], op_ntc_qnt_dict[key]

def op_accmlt_ntcIDlst_ntcQnt_dict(key, OP_lst,year,ntf_rsn,ntc_type):
    op_ntcid_dict = dict()
    op_ntc_qnt = 0
    op_ntcid_dict.update({key:find_accmlt_ntc_id(key,OP_lst,year,ntf_rsn,ntc_type)})
    if op_ntcid_dict[key].__len__() > 0:
        for item in op_ntcid_dict[key]:
            op_ntc_qnt = item.__len__() + op_ntc_qnt
            #print op_ntc_qnt


    return op_ntcid_dict[key], op_ntc_qnt


def find_accmlt_ntc_id(c,con_lst,year,ntf_rsn,ntc_type,mdb_idx):
    year_s = 1990
    ntc_id_lst = []
    with open(con_lst) as f:
        con_lst = f.readlines()
    for row in con_lst:
        pattern = (c+',(\w+),(\d+)')
        match = re.match(pattern, row)
        if match != None:
            adm = match.group(1)
            op_id = match.group(2)
            adm_op_ntc_id = ITU_mdb_query(mdb_idx).find_accmlt_ntc_lst_byOP_date(adm,op_id,year_s,year,ntf_rsn,ntc_type)
            if adm_op_ntc_id.__len__() > 0:
                ntc_id_lst.append(adm_op_ntc_id)


    return ntc_id_lst



def find_ntc_id(c,con_lst,y_s,y_e,ntf_rsn,ntc_type, mdb_idx):
    ntc_id_lst = []
    with open(con_lst) as f:
        con_lst = f.readlines()
    for row in con_lst:
        pattern = (c+',(\w+),(\d+)')
        match = re.match(pattern, row)
        if match != None:
            adm = match.group(1)
            op_id = match.group(2)
            adm_op_ntc_id = ITU_mdb_query(mdb_idx, ntf_rsn).find_ntc_lst_byOP_date(adm,op_id,y_s,y_e,ntc_type)
            if adm_op_ntc_id.__len__() > 0:
                ntc_id_lst.append(adm_op_ntc_id)


    return ntc_id_lst


def find_ntc_id_by_opName_fq_orb(c,con_lst,y_s,y_e,ntf_rsn, mdb_idx,fq_pnt,orb_l,orb_h):
    ntc_id_lst = []
    with open(con_lst) as f:
        con_lst = f.readlines()
    for row in con_lst:
        pattern = (c+',(\w+),(\d+)')
        match = re.match(pattern, row)
        if match != None:
            adm = match.group(1)
            op_id = match.group(2)
            adm_op_ntc_id = ITU_mdb_query(mdb_idx, ntf_rsn).find_ntc_lst_byOP_date_fq_orb(adm, op_id, y_s, y_e, fq_pnt, orb_l, orb_h)
            if adm_op_ntc_id.__len__() > 0:
                ntc_id_lst.append(adm_op_ntc_id)


    return ntc_id_lst

def find_op_lst(lst):
    op_lst = []
    cnt = 0
    for row in lst:
        p = '(\w+)'
        match = re.match(p,row)
        if match == None:
            print('None')
        else:
            match = re.match(p,row).group(0)
            op_lst.append(match)
            cnt = cnt + 1
        C = Counter(op_lst)

    return C

