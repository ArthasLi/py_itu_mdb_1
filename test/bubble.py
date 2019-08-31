import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
def DrawBubble(read_name):
    sns.set(style = "whitegrid")
    fp = pd.read_csv(read_name)
    x = fp.people
    y = fp.price
    z = fp.people
    cm = plt.cm.get_cmap('RdYlBu')
    fig,ax = plt.subplots(figsize = (12,10))

    bubble = ax.scatter(x, y , z, c = z**2, alpha = 0.5)
    ax.grid()
    fig.colorbar(bubble)
    ax.set_xlabel('people of cities', fontsize = 15)
    ax.set_ylabel('price of something', fontsize = 15)
    plt.show()
if __name__=='__main__':
    DrawBubble("PeopleNumber.csv")
