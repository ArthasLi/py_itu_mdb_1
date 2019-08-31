# libraries
import matplotlib.pyplot as plt
import squarify  # pip install squarify (algorithm for treemap)

# If you have 2 lists
squarify.plot(sizes=[13, 22, 35, 5], label=["group A", "group B", "group C", "group D"], alpha=.7)
plt.axis('off')
plt.show()
