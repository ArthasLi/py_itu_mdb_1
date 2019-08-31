# import pypyodbc
from sqlQry import sqlQry
import collections
import squarify
import matplotlib.pyplot as plt

if __name__ == "__main__":
    statement = "SELECT adm FROM com_el where ntf_rsn='N' and ntc_type = 'G' "
    data = sqlQry(statement)
    most10 = collections.Counter(data).most_common(10)
    adm = [x[0] for x in most10]
    size = [x[1] for x in most10]
    squarify.plot(sizes=size, label=adm, alpha=.7)
    plt.axis('off')
    plt.show()



