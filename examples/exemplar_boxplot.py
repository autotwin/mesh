# from turtle import position
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

path_file_in = Path(__file__)
stem = path_file_in.stem
fig_extension = ".png"
path_file_out = stem + fig_extension

n_studies = 6  # define once-and-for-all, avoid magic numbers later

rand_nums = np.zeros([100, n_studies])
medians = np.zeros(n_studies)

for iii in range(n_studies):
    rand_nums[:, iii] = np.random.randint(0, 10001, 100) / 10000
    medians[iii] = np.median(rand_nums[:, iii])

# Sort the distributions based on median
indeces = np.argsort(medians)
sorted_numbers = np.zeros([100, n_studies])
for iii in range(6):
    sorted_numbers[:, iii] = rand_nums[:, indeces[iii]]
plt.boxplot(sorted_numbers)
# plt.xticks([1, 2, 3, 4, 5, 6], indeces)
plt.xticks(np.arange(n_studies) + 1, indeces)
plt.title("Randomly Generated Distributions Sorted by Median")
plt.xlabel("Case Number")
plt.ylabel("Value")
# plt.savefig("boxplot_example.png") # instead of hard code, make it reflect the .py file name
plt.savefig(path_file_out)  # automatically reflect the .py file source name
