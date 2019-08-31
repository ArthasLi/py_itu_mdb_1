import numpy as np
from ITU_mdb_query import ITU_mdb_query

def freq_mergByNtcID(id, mdb_id):
    ntf_rsn = 'blank'
    dd = ITU_mdb_query(mdb_id, ntf_rsn)
    fq1_FreqArr = dd.find_fq_arr_int_ID(id)
    a =freq_merg(fq1_FreqArr)
    return freq_merg(fq1_FreqArr)


def freq_merg(freq_array):
    if freq_array.__len__() > 2:
        freq_array=sorted(freq_array, key=lambda x: x[0])
    freq_array = np.array(freq_array)
    fq_shape = np.array(freq_array).shape

    l = fq_shape[0]
    for i in range(0, l-1, 1):
        for j in range(2, l, 1):
            if freq_array[j][0] != 0 and i != j:
                i
                if freq_array[i][0] > freq_array[j][1] or freq_array[i][1] < freq_array[j][0]:
                    j
                else:
                    freq_array[i][0] = min(freq_array[i][0], freq_array[j][0])
                    freq_array[i][1] = max(freq_array[i][1], freq_array[j][1])
                    freq_array[j][0] = 0
                    freq_array[j][1] = 0

    if freq_array.__len__() > 2:
        freq_array= filter(lambda x: x[0] !=0 , freq_array)
    return freq_array

def freq_overlap_by_arr(fq1,fq2):
    # fq1 is ndarray
    fq1_FreqArr = fq1
    #fq1_FreqArr = freq_merg(fq1)
    fq_size = fq1.size
    if fq_size < 3.0:
        fq1_FreqArr = np.array([[1,2],fq1_FreqArr])

    fq1_shape = np.array(fq1_FreqArr).shape
    l1 = fq1_shape[0]
    fq2_FreqArr = freq_merg(fq2)
    fq2_shape = np.array(fq2_FreqArr).shape
    l2 = fq2_shape[0]
    overlappedFreqArr = [[0,0]]
    for i in range(0, (l1), 1):
        for j in range(0, (l2), 1):
            if fq1_FreqArr[i][0] > fq2_FreqArr[j][1] or fq1_FreqArr[i][1] < fq2_FreqArr[j][0]:

               i,j

            else:
                freq_max = min(fq1_FreqArr[i][1], fq2_FreqArr[j][1])
                freq_min = max(fq1_FreqArr[i][0], fq2_FreqArr[j][0])
                overlappedFreqArr.append([freq_min, freq_max])
    return overlappedFreqArr


def freq_overlap_by_id_arr(id, fq2_FreqArr, mdb_id):
    ini = ITU_mdb_query(mdb_id)
    fq1_FreqArr = ini.find_fq_arr(id)
    # fq1 is list of row, while fq2 is list of list , malfunction!!!
    return freq_overlap_by_arr(fq1_FreqArr, fq2_FreqArr)
