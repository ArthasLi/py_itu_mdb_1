from sqlQry import sqlQry
import numpy as np
import re
import collections
from collections import Counter


class srvNtcStt:

    def __init__(self, rsn, orb_type, srv, d_s, d_e):
        self.adm = None
        self.orb_type = orb_type
        self.rsn = rsn
        self.srv = srv
        self.d_s = str(d_s)+"-01-01"
        self.d_e = str(d_e) + "-12-31"
        self.satNbrData = None
        self.op_sat_nbr_data = None
        self.adm_sat_nbr_data = None
        self.adm_op_sat_nbr_data = None
        self.main_adm_list = [['USA'], ['CHN'], ['RUS'], ['F'], ['G'], ['J'], ['IND']]

    def ntc_nbr_world_count(self):
        qry = "SELECT DISTINCT " \
              "com_el.adm, com_el.ntc_id " \
              "FROM " \
              "com_el,grp,srv_cls " \
              "WHERE com_el.ntc_type='"+self.orb_type+"' and com_el.ntf_rsn='"+self.rsn+"' and com_el.d_rcv>=#" + self.d_s + "# and com_el.d_rcv<=#" + self.d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='"+self.srv+"'"
        data = sqlQry(qry)
        nbr = 0
        if data == None:
            nbr = 0
        else:
            nbr = data.__len__()
        return nbr

    def sat_nbr_world_count(self):
        qry = "SELECT DISTINCT " \
              "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl, com_el.sat_name " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE orbit.ntc_id=com_el.ntc_id and com_el.ntc_type='"+self.orb_type + "' and com_el.ntf_rsn = '"+self.rsn+"' and com_el.d_rcv>=#" + self.d_s + "# and com_el.d_rcv<=#" + self.d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='"+self.srv+"'"
        data = sqlQry(qry)
        totalNbr = 0
        for x in range(0, (data.__len__()-1)):
           # print (data[x][2])
            if data[x][2] is None:
                totalNbr += 0
            else:
                totalNbr += data[x][2]
            #print (data.__len__(), x, data[x][2])
        #print (totalNbr)

        return totalNbr

    def ntc_nbr_main_adm_count(self):
        adm_data = self.main_adm_list
        count = 0
        ntc_nbr_info = 0
        if adm_data == None:
            ntc_nbr_info = 0
        else:
            for x in adm_data:
                qry = "SELECT DISTINCT " \
                      "com_el.ntc_id " \
                      "FROM " \
                      "com_el,grp,srv_cls " \
                      "WHERE com_el.adm='" + x[0] + "' and com_el.ntf_rsn='" + self.rsn + "' and com_el.d_rcv>=#" + self.d_s + \
                      "# and com_el.d_rcv<=#" + self.d_e + "#" \
                      "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + self.srv + "'"
                data = sqlQry(qry)
                if count == 0:
                    ntc_nbr_info = [x[0], data.__len__()]
                else:
                    ntc_nbr_info.append([x[0], data.__len__()])
                count += 1

        return ntc_nbr_info

    def ntc_nbr_adm_count(self):
        adm_data = self.adm_sat_nbr_data
        count = 0
        ntc_nbr_info = 0
        if adm_data == None:
            ntc_nbr_info = 0
        else:
            for x in adm_data:
                qry = "SELECT DISTINCT " \
                      "com_el.ntc_id " \
                      "FROM " \
                      "com_el,grp,srv_cls " \
                      "WHERE com_el.adm='"+x[0]+"' and com_el.ntf_rsn='"+self.rsn+"' and com_el.d_rcv>=#" + self.d_s + \
                      "# and com_el.d_rcv<=#" + self.d_e + "#" \
                      "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='"+self.srv+"'"
                data = sqlQry(qry)
                if count == 0:
                    ntc_nbr_info = [x[0], data.__len__()]
                else:
                    ntc_nbr_info.append([x[0], data.__len__()])
                count += 1



        return ntc_nbr_info


    def get_sat_nbr_info(self):
        qry = "SELECT DISTINCT " \
              "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl, com_el.sat_name, com_el.adm " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE orbit.ntc_id=com_el.ntc_id and com_el.ntc_type='" + self.orb_type + "' and com_el.ntf_rsn = '" \
              + self.rsn + "' and com_el.d_rcv>=#" + self.d_s + "# and com_el.d_rcv<=#" + self.d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + self.srv + "'"
        self.satNbrData = sqlQry(qry)



    def adm_ntc_type_check(self,ntf_rsn, ntc_type, srv_cls, d_s, d_e):
        self.rsn = ntf_rsn
        self.orb_type = ntc_type
        self.srv = srv_cls
        self.d_s = d_s
        self.d_e = d_e

        qry = "SELECT DISTINCT " \
              "com_el.adm " \
              "FROM " \
              "com_el,grp,srv_cls " \
              "WHERE " \
              "com_el.ntc_type='" + ntc_type + "' and com_el.ntf_rsn = '" \
              + ntf_rsn + "' and com_el.d_rcv>=#" + d_s + "# and com_el.d_rcv<=#" + d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + srv_cls + "'"
        self.adm_sat_nbr_data = sqlQry(qry)

    def op_ntc_type_check(self, adm, ntf_rsn, ntc_type, srv_cls, d_s, d_e ):

        qry = "SELECT DISTINCT " \
              "grp.op_agcy " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE " \
              "com_el.adm='"+adm+"' and com_el.ntc_type='" + ntc_type + "' and com_el.ntf_rsn = '" \
              + ntf_rsn + "' and com_el.d_rcv>=#" + d_s + "# and com_el.d_rcv<=#" + d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + srv_cls + "'"
        data = sqlQry(qry)
        self.adm_op_sat_nbr_data = data

    def count_adm_satNbr(self, adm, ntf_rsn, ntc_type, srv_cls, d_s, d_e ):
        qry = "SELECT DISTINCT " \
              "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE " \
              "com_el.adm='" + adm + "' and orbit.ntc_id=com_el.ntc_id and " \
              "com_el.ntc_type='" + ntc_type + "' and com_el.ntf_rsn = '" \
              + ntf_rsn + "' and com_el.d_rcv>=#" + d_s + "# and com_el.d_rcv<=#" + d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + srv_cls + "'"
        data = sqlQry(qry)
        count = 0
        for x in data:
            if x[2] is None:
                count += 0
            else:
                count += x[2]
        return count

    def count_op_satNbr(self, adm, op_agcy, ntf_rsn, ntc_type, srv_cls, d_s, d_e ):
        qry = "SELECT DISTINCT " \
              "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE " \
              "grp.op_agcy=" + str(op_agcy) + " and com_el.adm='" + adm + "' and orbit.ntc_id=com_el.ntc_id and " \
              "com_el.ntc_type='" +ntc_type + "' and com_el.ntf_rsn = '" \
              + ntf_rsn + "' and com_el.d_rcv>=#" + d_s + "# and com_el.d_rcv<=#" + d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + srv_cls + "'"
        data = sqlQry(qry)
        count = 0
        ntcLst = [x[0] for x in data]
        C = Counter(ntcLst)

        #distNtcLst = list(C)

        for x in data:
            if x[2] is None:
                count += 0
            else:
                count += x[2]
        return [C.__len__(), count]

    def sat_nbr_op_ana(self):
        # run  adm_ntc_type_check "com_el.adm
        data = self.adm_sat_nbr_data
        #  "grp.op_agcy "
       # satNbrArr = [x[4] for x in self.satNbrData]
        admArr = [x[0] for x in data]
        admCount = 0
        opCount = 0
        op_info =0
        for x in data:
            self.op_ntc_type_check(x[0], self.rsn, self.orb_type, self.srv, self.d_s, self.d_e)
            op_data = self.adm_op_sat_nbr_data
            #  "grp.op_agcy "
            for y in op_data:
                satNbr = self.count_op_satNbr(x[0], y[0], self.rsn, self.orb_type, self.srv, self.d_s, self.d_e)
                if admCount == 0 and opCount == 0:
                    op_info = [x[0], y[0], satNbr]
                else:
                    op_info.append([x[0], y[0], satNbr])
                opCount += 1
            admCount += 1
        return op_info

    def sat_nbr_adm_ana(self):
        # run  adm_ntc_type_check "com_el.adm
        data = self.adm_sat_nbr_data
        #  "grp.op_agcy "
       # satNbrArr = [x[4] for x in self.satNbrData]
        admArr = [x[0] for x in data]
        admCount = 0
        adm_info=0
        for x in data:
            # "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl, com_el.sat_name, grp.op_agcy, com_el.d_rcv "
            satNbr = self.count_adm_satNbr(x[0], self.rsn, self.orb_type, self.srv, self.d_s, self.d_e)
            if admCount == 0:
                adm_info = [x[0], satNbr]
            else:
                adm_info.append([x[0], satNbr])
            admCount += 1

        return (adm_info)

    def sat_nbr_main_adm_ana(self):
        # run  adm_ntc_type_check "com_el.adm
        data = self.main_adm_list
        #  "grp.op_agcy "
       # satNbrArr = [x[4] for x in self.satNbrData]
        admArr = [x[0] for x in data]
        admCount = 0
        adm_info = 0
        for x in data:
            # "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl, com_el.sat_name, grp.op_agcy, com_el.d_rcv "
            satNbr = self.count_adm_satNbr(x[0], self.rsn, self.orb_type, self.srv, self.d_s, self.d_e)
            if admCount == 0:
                adm_info = [x[0], satNbr]
            else:
                adm_info.append([x[0], satNbr])
            admCount += 1

        return (adm_info)

    def sat_nbr_world_ana(self):
        qry = "SELECT DISTINCT " \
              "orbit.ntc_id, orbit.orb_id, orbit.nbr_sat_pl " \
              "FROM " \
              "com_el,grp,srv_cls,orbit " \
              "WHERE " \
              "orbit.ntc_id=com_el.ntc_id and " \
              "com_el.ntc_type='" + self.orb_type + "' and com_el.ntf_rsn = '" \
              + self.rsn + "' and com_el.d_rcv>=#" + self.d_s + "# and com_el.d_rcv<=#" + self.d_e + "#" \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='" + self.srv + "'"
        data = sqlQry(qry)
        count = 0

        for x in data:
            if x[2] is None:
                count += 0
            else:
                count += x[2]
        return (count)
