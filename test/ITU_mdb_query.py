from sqlQry import sqlQry
import time
import datetime
import re


class ITU_mdb_query:
    def __init__(self,mdb_id,ntf_rsn):
        # 0 for SRS, 1 for AP_30B, 2 for SPS_ALL
        self.mdb_idx = mdb_id
        self.ntf_rsn = ntf_rsn
        if mdb_id == 1 and ntf_rsn == 'C':
            self.ntc_rsn = 'P'
        if mdb_id == 2 and ntf_rsn == 'C':
            self.ntf_rsn = 'B'



    def find_adm_opID_by_ntcID(self, ntc_id):
        qry = "SELECT DISTINCT " \
              "com_el.adm, grp.op_agcy " \
              "FROM " \
              "com_el, grp " \
              "WHERE com_el.ntc_id="+str(ntc_id)+" and grp.ntc_id = " +str(ntc_id)
        data = sqlQry(qry, self.mdb_idx)
        return data

    def find_ntc_lst_byOP(self, adm, agcy_id):
        qry = "SELECT DISTINCT " \
              "com_el.ntc_id " \
              "FROM " \
              "com_el, grp " \
              "WHERE com_el.adm='"+adm+"' and grp.op_agcy = " +str(agcy_id)+" and com_el.ntc_id = grp.ntc_id"
        data = sqlQry(qry, self.mdb_idx)
        return data

    def find_accmlt_ntc_lst_by_adm(self, adm, year,ntc_type):
        # year : int
        d_end = (str(year)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el " \
                "WHERE com_el.adm='" + adm + "' and com_el.d_rcv<=#" + d_end + "#" +\
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_lastDec_accmlt_ntc_lst_by_adm(self, adm, year,ntc_type):
        # year : int
        year = int(year)
        d_end = (str(year)+'-12-31')
        d_start = (str(year-10) + '-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el " \
                "WHERE com_el.adm='" + adm + "' and com_el.d_rcv>=#" + d_start + "#" + " and com_el.d_rcv<=#" + d_end + "#" + \
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_annual_ntc_lst_by_adm(self, adm, year,ntc_type):
        # year : int
        d_start = (str(year)+'-01-01')
        d_end = (str(year)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el " \
                "WHERE com_el.adm='" + adm + "' and com_el.d_rcv>=#" + d_start + "#" + " and com_el.d_rcv<=#" + d_end + "#" + \
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_accmlt_ntc_lst_byOP_date(self, adm, agcy_id,y_s , y_e,ntc_type):
        # year : int
        d_start = (str(y_s) + '-01-01')
        d_end = (str(y_e)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el, grp " \
                "WHERE com_el.adm='" + adm + "' and grp.op_agcy = " + str(agcy_id) + " and com_el.ntc_id = grp.ntc_id" +\
                " and com_el.d_rcv<=#" + d_end + "#" + " and com_el.d_rcv>=#" + d_start + "#" +\
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_ntc_lst_byOP_date(self, adm, agcy_id,year_s, year_e,ntc_type):
        # year : int
        d_start = (str(year_s)+'-01-01')
        d_end = (str(year_e)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el, grp " \
                "WHERE com_el.adm='" + adm + "' and grp.op_agcy = " + str(agcy_id) + " and com_el.ntc_id = grp.ntc_id" +\
                " and com_el.d_rcv>=#" + d_start + "#" + " and com_el.d_rcv<=#" + d_end + "#" +\
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        #qry = 'SELECT DISTINCT com_el.ntc_id FROM com_el, grp WHERE com_el.adm=\'LUX\' and grp.op_agcy = 10 and com_el.ntc_id = grp.ntc_id and com_el.d_rcv>=#2011-01-01# and com_el.d_rcv<=#2011-12-31# and com_el.ntf_rsn=\'C\' and com_el.ntc_type=\'G\''
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_ntc_lst_byOP_date_fq_orb(self, adm, agcy_id,year_s, year_e,fq_pnt,orb_l,orb_h):
        # year : int
        ntc_type = 'G'
        d_start = (str(year_s)+'-01-01')
        d_end = (str(year_e)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el, grp " \
                "WHERE com_el.adm='" + adm + "' and grp.op_agcy = " + str(agcy_id) + " and com_el.ntc_id = grp.ntc_id" +\
                " and com_el.d_rcv>=#" + d_start + "#" + " and com_el.d_rcv<=#" + d_end + "#" +\
                " and grp.freq_min<=" + str(fq_pnt) + " and grp.freq_max>" + str(fq_pnt) +\
                " and com_el.long_nom>=" +str(orb_l) + " and com_el.long_nom<" + str(orb_h) +\
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        #qry = 'SELECT DISTINCT com_el.ntc_id FROM com_el, grp WHERE com_el.adm=\'LUX\' and grp.op_agcy = 10 and com_el.ntc_id = grp.ntc_id and com_el.d_rcv>=#2011-01-01# and com_el.d_rcv<=#2011-12-31# and com_el.ntf_rsn=\'C\' and com_el.ntc_type=\'G\''
        # print 'find_ntc_lst_byOP_date_fq_orb'
        # print qry
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_ntc_lst_date_fq_orb(self,year_s, year_e,fq_pnt,orb_l,orb_h):
        # year : int
        ntc_type = 'G'
        d_start = (str(year_s)+'-01-01')
        d_end = (str(year_e)+'-12-31')
        qry = "SELECT DISTINCT " \
                "com_el.ntc_id " \
                "FROM " \
                "com_el, grp " \
                "WHERE com_el.ntc_id = grp.ntc_id" +\
                " and com_el.d_rcv>=#" + d_start + "#" + " and com_el.d_rcv<=#" + d_end + "#" +\
                " and grp.freq_min<=" + str(fq_pnt) + " and grp.freq_max>" + str(fq_pnt) +\
                " and com_el.long_nom>=" +str(orb_l) + " and com_el.long_nom<" + str(orb_h) +\
                " and com_el.ntf_rsn='" + self.ntf_rsn + "' and com_el.ntc_type='" + ntc_type + "'"
        #qry = 'SELECT DISTINCT com_el.ntc_id FROM com_el, grp WHERE com_el.adm=\'LUX\' and grp.op_agcy = 10 and com_el.ntc_id = grp.ntc_id and com_el.d_rcv>=#2011-01-01# and com_el.d_rcv<=#2011-12-31# and com_el.ntf_rsn=\'C\' and com_el.ntc_type=\'G\''
        # print 'find_ntc_lst_byOP_date_fq_orb'
        # print qry
        data = sqlQry(qry, self.mdb_idx)

        return data

    def find_co_ntc_byWIC(self, wic_no, adm, date):

        d_rcv = date[0][0].date().strftime("%Y-%m-%d")
        qry = "SELECT " \
              "ntc_id, prov, adm, sat_name, long_nom, ntf_rsn, d_rcv, ntc_type " \
              "FROM " \
              "com_el " \
              "WHERE " \
              "wic_no= " +str(wic_no) + " and adm<>'" + adm + "' and d_rcv>=#" + d_rcv + "#"
        return sqlQry(qry, self.mdb_idx)

    def find_d_rcv(self, ntc_id):
        qry = "SELECT d_rcv from com_el WHERE ntc_id= " + str(ntc_id[0])
        return sqlQry(qry, self.mdb_idx)

    def find_fq_arr(self, ntc_id):
        qry = "SELECT freq_min, freq_max from freq WHERE ntc_id= " + str(ntc_id[0])
        return sqlQry(qry, self.mdb_idx)
    def find_fq_arr_int_ID(self, ntc_id):
        qry = "SELECT freq_min, freq_max from freq WHERE ntc_id= " + str(ntc_id)
        return sqlQry(qry, self.mdb_idx)


