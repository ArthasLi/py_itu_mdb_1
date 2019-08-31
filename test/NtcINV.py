from sqlQry import sqlQry
import re


class NtcINV:

    def __init__(self, ntcID):
        self.id = ntcID
        qry = "SELECT DISTINCT " \
              "com_el.adm " \
              "FROM " \
              "com_el,grp,srv_cls " \
              "WHERE com_el.ntf_rsn='N' and com_el.d_rcv>#2010-01-01# " \
              "and com_el.ntc_id = grp.ntc_id and grp.grp_id = srv_cls.grp_id and srv_cls.stn_cls='EW'"



        self.data = sqlQry(qry)
        lst = self.data
       # lst = self.data[0].split(',')
       # lst = self.data[0].encode('utf-8')

        print(lst)




