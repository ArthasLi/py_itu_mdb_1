import numpy
from op_BW_stt import dict_to_lst,find_ntc_id_by_opName_fq_orb
from ITU_mdb_query import ITU_mdb_query
from freq_band_cat import band_bank


class freq_orb_ind:

    def __init__(self, orb_seg, band_type,y_s,y_e,ntf_rsn, orb_seg_res, band_res):
        self.orb_seg_res = orb_seg_res
        self.band_res = band_res
        self.y_s = y_s
        self.y_e = y_e
        self.ntf_rsn = ntf_rsn
        self.orb_seg = orb_seg
        self.OP_cntant_lst = 'OP_lst'
        self.OP_lst = ['SES','EUTELSAT','INTELSAT','CHINASATCOM','HISPASAT','THAICOM']
        self.band_type = band_type
        # self.band_map = self.cal_band_map(self.orb_seg, self.OP_lst, self.band_type)
        self.band_map = self.cal_band_map_adm(self.orb_seg, self.band_type)
        numpy.savetxt("band_map.txt", self.band_map, fmt="%f", delimiter=",")
        self.band_map

    def cal_band_map_adm(self, orb_seg, band_type):
        # band_seg = self.find_band_seg(band_type)
        fq_pnt_arr = self.fq_pnt_mapping(band_type)
        orb_seg_m = int((orb_seg[1] - orb_seg[0])/self.orb_seg_res + 1)
        band_seg_n = fq_pnt_arr.__len__()
        band_map = numpy.zeros((orb_seg_m, band_seg_n))
        for m in range(0,orb_seg_m,1):
            for n in range(0, band_seg_n,1):
                orb_pnt = orb_seg[0] + m*self.orb_seg_res
                fq_pnt = fq_pnt_arr[n]
                # print 'cal_band_map loop: '+ str(m)+str(n)
                # print 'fq:' + str(fq_pnt) + '   orb:' + str(orb_pnt)
                band_map = self.update_map(m,n,orb_seg_m,band_map,band_type,orb_pnt,fq_pnt,self.orb_seg_res)

        return band_map

    def fq_pnt_mapping(self, band_type):
        # band_type = 'QV'
        band_seg = band_bank(band_type)
        seg_shape = band_seg.shape.__len__()
        fq_pnts = []
        final_fq_pnts = []
        if seg_shape > 1:
            for i in range(0,seg_shape+1):
                max_min_pair = band_seg[i]
                fq_pnts = numpy.arange(max_min_pair[0],max_min_pair[1]+self.band_res,self.band_res)
                final_fq_pnts = numpy.concatenate((final_fq_pnts,fq_pnts), axis=None)

        else:
            final_fq_pnts = numpy.arange(band_seg[0], band_seg[1]+self.band_res, self.band_res)
        return final_fq_pnts

    def cal_band_map(self, orb_seg, OP_lst, band_type):
        band_seg = self.find_band_seg(band_type)
        orb_seg_m = int((orb_seg[1] - orb_seg[0])/self.orb_seg_res + 1)
        band_seg_n = (max(band_seg) - min(band_seg))/self.band_res + 1
        band_map = numpy.zeros((orb_seg_m, band_seg_n))

        for m in range(0,orb_seg_m,1):
            for n in range(0, band_seg_n,1):
                orb_pnt = orb_seg[0] + m*self.orb_seg_res
                fq_pnt = min(band_seg)+ n*self.band_res
                # print 'cal_band_map loop: '+ str(m)+str(n)
                # print 'fq:' + str(fq_pnt) + '   orb:' + str(orb_pnt)
                band_map = self.update_map(m,n,orb_seg_m,band_map,band_type,orb_pnt,fq_pnt,self.orb_seg_res)
        return band_map



    def update_map(self,m,n,orb_seg_m,band_map,band_type,orb_pnt,fq_pnt,orb_seg_res):
        a = band_map[1,1]
        mask = self.roll_off_mask(band_type)*self.band_density_all_adm(orb_pnt, fq_pnt,orb_seg_res)
        if max(mask) > 0:
            len = int((mask.size - 1)/2)
            for i in range(0,len + 1, 1):
                if m>=i:
                    band_map[m -i, n] = band_map[m-i, n] + mask[len +i]
                    # band_map[m, n] = band_map[m, n] + mask[i]*self.band_density(orb_pnt,fq_pnt,orb_seg_res)
                    # print band_map[m, n]
                    if band_map[m, n]:
                        print 'update_map hit'
                        print m,n,i
                        print band_map[m, n]
                if ((m + i + 1)<=orb_seg_m) and i != 0:
                    # print m,n,i
                    band_map[m +i, n] = band_map[m+i, n] + mask[len +i]
                    # band_map[m, n] = band_map[m, n] + mask[i]*self.band_density(orb_pnt,fq_pnt,orb_seg_res)
                    # print band_map[m, n]
                    if band_map[m, n]:
                        print 'update_map hit'
                        print m,n,i
                        print band_map[m, n]
        return band_map

    def band_density(self,orb_pnt,fq_pnt,orb_seg_res):
        density = 0
        ntc_id_lst = []
        orb_l = orb_pnt - 0.5*orb_seg_res
        orb_h = orb_pnt + 0.5*orb_seg_res
        # print 'checking band_density'
        # print fq_pnt, orb_pnt
        for c in self.OP_lst:
            for mdb_idx in range(0,3,1):
                op_id_lst = find_ntc_id_by_opName_fq_orb(c,self.OP_cntant_lst,self.y_s,self.y_e,self.ntf_rsn, mdb_idx,fq_pnt,orb_l,orb_h)
                if op_id_lst:
                    print 'band_density hit'
                    ntc_id_lst.append(dict_to_lst(op_id_lst))

        return ntc_id_lst.__len__()

    def band_density_all_adm(self,orb_pnt,fq_pnt,orb_seg_res):
        density = 0
        ntc_id_lst = []
        orb_l = orb_pnt - 0.5*orb_seg_res
        orb_h = orb_pnt + 0.5*orb_seg_res
        # print 'checking band_density_all_adm'
        # print fq_pnt, orb_pnt

        for mdb_idx in range(0,3,1):
            mdb = ITU_mdb_query(mdb_idx, self.ntf_rsn)
            op_id_lst = mdb.find_ntc_lst_date_fq_orb(self.y_s,self.y_e,fq_pnt, orb_l, orb_h)
            if op_id_lst:
                print 'band_density_all_adm hit'
                for id in op_id_lst:
                    ntc_id_lst.append(id)
        return ntc_id_lst.__len__()

    def roll_off_mask(self, band_type):
        if band_type == 'C':
            mu = 0
            sig = 2
            roll_off_seg = 3
            pnts_width = int(roll_off_seg / self.orb_seg_res)
            mask = numpy.zeros(2*pnts_width+1)
            sample_pnts_x = numpy.arange(0, roll_off_seg+self.orb_seg_res, self.orb_seg_res)
            for offset in range(0, pnts_width+1):
                mask[offset + pnts_width] = pow(self.gaussian(sample_pnts_x[offset], mu, sig), 2.5)
                mask[-offset + pnts_width] = pow(self.gaussian(sample_pnts_x[offset], mu, sig), 2.5)

        if band_type == 'Ku':
            mu = 0
            sig = 1
            roll_off_seg = 2
            pnts_width = int(roll_off_seg / self.orb_seg_res)
            mask = numpy.zeros(2*pnts_width+1)
            sample_pnts_x = numpy.arange(0, roll_off_seg+self.orb_seg_res, self.orb_seg_res)
            for offset in range(0, pnts_width+1):
                a = mask[0]
                mask[offset + pnts_width] = self.gaussian(sample_pnts_x[offset], mu, sig)
                mask[-offset + pnts_width] = self.gaussian(sample_pnts_x[offset], mu, sig)

        if band_type == 'Ka':
            mu = 0
            sig = 0.8
            roll_off_seg = 1.8
            pnts_width = int(roll_off_seg / self.orb_seg_res)
            mask = numpy.zeros(2*pnts_width+1)
            sample_pnts_x = numpy.arange(0, roll_off_seg+self.orb_seg_res, self.orb_seg_res)
            for offset in range(0, pnts_width+1):
                mask[offset + pnts_width] = self.gaussian(sample_pnts_x[offset], mu, sig)
                mask[-offset + pnts_width] = self.gaussian(sample_pnts_x[offset], mu, sig)

        return mask


    def gaussian(self, x, mu, sig):
        return numpy.exp(-numpy.power(x - mu, 2.)/(2*numpy.power(sig, 2.)))

    def find_band_seg(self, band_type):
        band_seg = []
        if band_type == 'C':
            band_seg = [3400,7025]
        if band_type =='Ku':
            band_seg = [10700, 17699]
        if band_type == 'Ka':
            band_seg = [17700, 31000]

        return band_seg
