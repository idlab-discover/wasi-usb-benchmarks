import matplotlib.pyplot as plt
import pandas as pd

data_wasm = pd.read_csv("./mass-storage/data-pi-wasm.csv")
data_native = pd.read_csv("./mass-storage/data-pi-native.csv")

data_wasm.plot(kind='box', title='boxplot wasm', showmeans=True)
data_native.plot(kind='box', title='boxplot native', showmeans=True)
plt.show()