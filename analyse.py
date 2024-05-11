import matplotlib.pyplot as plt
import pandas as pd

# Colors
color_x86_nousb = "#ed7700"
color_x86_usb = "#fa9632"
color_aarch64_nousb = "#e61515"
color_aarch64_usb = "#f74a36"
color_windows_nousb = "#0e67ed"
color_windows_usb = "#3aa8fc"

######### File sizes #########
x86_nousb = 14612  # KB
x86_usb = 14772  # KB
aarch64_nousb = 12964  # KB
aarch64_usb = 13184  # KB
windows_nousb = 14175  # KB
windows_usb = 14450  # KB


# function to add value labels
def add_labels_kilobyte(y):
    ylim = plt.gca().get_ylim()
    yrange = ylim[1] - ylim[0]
    for i in range(len(y)):
        plt.text(i, y[i] + yrange*0.0075, f"{y[i]:.0f} kB", ha="center", va="bottom")


def add_labels_megabyte_per_second(y):
    ylim = plt.gca().get_ylim()
    yrange = ylim[1] - ylim[0]
    for i in range(len(y)):
        plt.text(i + 1.25, y[i] - yrange*0.02, f"{y[i]:.0f} MB/s", ha="center", va="bottom")


plt.figure(figsize=(16, 6))
plt.ylabel("File Size (kB)")
x = [
    "x86 Linux Baseline",
    "x86 Linux USB",
    "AArch64 Linux Baseline",
    "AArch64 Linux USB",
    "x86 Windows Baseline",
    "x86 Windows USB",
]
y = [x86_nousb, x86_usb, aarch64_nousb, aarch64_usb, windows_nousb, windows_usb]
colors = [
    color_x86_nousb,
    color_x86_usb,
    color_aarch64_nousb,
    color_aarch64_usb,
    color_windows_nousb,
    color_windows_usb,
]
plt.bar(x, y, color=colors)
add_labels_kilobyte(y)
plt.savefig("figures/filesize.png")
plt.close()

######### Memory usage #########
x86_nousb_mem = [26208, 27156, 26880, 26344, 27016, 27020, 26988, 27864, 26940, 27184]
x86_usb_mem = [27004, 27236, 26956, 27024, 27364, 27672, 27184, 28140, 27656, 27952]
aarch64_nousb_mem = [
    18960,
    19820,
    19012,
    19632,
    19164,
    18932,
    19548,
    19396,
    19012,
    18896,
]
aarch64_usb_mem = [
    20132,
    18980,
    19920,
    19576,
    19172,
    19880,
    19660,
    19108,
    19692,
    19196,
]
windows_nousb_mem = [12720, 12748, 13712, 12828, 12636]
windows_usb_mem = [14288, 14484, 14808, 13224, 14976]

avg_x86_nousb_mem = sum(x86_nousb_mem) / len(x86_nousb_mem)
avg_x86_usb_mem = sum(x86_usb_mem) / len(x86_usb_mem)
avg_aarch64_nousb_mem = sum(aarch64_nousb_mem) / len(aarch64_nousb_mem)
avg_aarch64_usb_mem = sum(aarch64_usb_mem) / len(aarch64_usb_mem)
avg_windows_nousb_mem = sum(windows_nousb_mem) / len(windows_nousb_mem)
avg_windows_usb_mem = sum(windows_usb_mem) / len(windows_usb_mem)

plt.figure(figsize=(16, 6))
plt.ylabel("Memory Usage (kB)")
x = [
    "x86 Linux Baseline",
    "x86 Linux USB",
    "AArch64 Linux Baseline",
    "AArch64 Linux USB",
    "x86 Windows Baseline",
    "x86 Windows USB",
]
y = [
    avg_x86_nousb_mem,
    avg_x86_usb_mem,
    avg_aarch64_nousb_mem,
    avg_aarch64_usb_mem,
    avg_windows_nousb_mem,
    avg_windows_usb_mem,
]
plt.bar(x, y, color=colors)
add_labels_kilobyte(y)
plt.savefig("figures/memory.png")
plt.close()

# In megabytes/second
mass_storage_x86_native = pd.read_csv(
    "./mass-storage/raw_benchmark_report_x86_native.csv"
) / (1024 * 1024)
mass_storage_x86_wasm = pd.read_csv(
    "./mass-storage/raw_benchmark_report_x86_wasm.csv"
) / (1024 * 1024)
mass_storage_aarch64_native = pd.read_csv(
    "./mass-storage/raw_benchmark_report_aarch64_native.csv"
) / (1024 * 1024)
mass_storage_aarch64_wasm = pd.read_csv(
    "./mass-storage/raw_benchmark_report_aarch64_wasm.csv"
) / (1024 * 1024)
mass_storage_windows_native = pd.read_csv(
    "./mass-storage/raw_benchmark_report_windows_native.csv"
) / (1024 * 1024)
mass_storage_windows_wasm = pd.read_csv(
    "./mass-storage/raw_benchmark_report_windows_wasm.csv"
) / (1024 * 1024)

# mass_storage_x86_native.plot(kind="box", title="boxplot native (x86)", showmeans=True)
# mass_storage_x86_wasm.plot(kind="box", title="boxplot wasm (x86)", showmeans=True)
# mass_storage_aarch64_native.plot(kind="box", title="boxplot native (aarch64)", showmeans=True)
# mass_storage_aarch64_wasm.plot(kind="box", title="boxplot wasm (aarch64)", showmeans=True)
# mass_storage_windows_native.plot(kind="box", title="boxplot native (windows)", showmeans=True)
# mass_storage_windows_wasm.plot(kind="box", title="boxplot wasm (windows)", showmeans=True)


def plot_boxplot(df: pd.DataFrame, title: str, filename: str):
    # fig = plt.figure(figsize=(6, 6))
    df.plot(kind="box", title=title, figsize=(6, 4))
    plt.ylabel("Speed (MB/s)")
    add_labels_megabyte_per_second([df["Native"].median(), df["WebAssembly"].median()])
    plt.savefig(filename)
    plt.close()

def create_df(native_df, wasm_df, key):
    return pd.DataFrame(
        [
            native_df[key].rename("Native"),
            wasm_df[key].rename("WebAssembly"),
        ]
    ).transpose()

seq_read_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "SEQ READ")
seq_read_aarch64 = create_df(mass_storage_aarch64_native, mass_storage_aarch64_wasm, "SEQ READ")
seq_read_windows = create_df(mass_storage_windows_native, mass_storage_windows_wasm, "SEQ READ")

seq_write_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "SEQ WRITE")
seq_write_aarch64 = create_df(mass_storage_aarch64_native, mass_storage_aarch64_wasm, "SEQ WRITE")
seq_write_windows = create_df(mass_storage_windows_native, mass_storage_windows_wasm, "SEQ WRITE")

rnd_read_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "RND READ")
rnd_read_aarch64 = create_df(mass_storage_aarch64_native, mass_storage_aarch64_wasm, "RND READ")
rnd_read_windows = create_df(mass_storage_windows_native, mass_storage_windows_wasm, "RND READ")

rnd_write_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "RND WRITE")  
rnd_write_aarch64 = create_df(mass_storage_aarch64_native, mass_storage_aarch64_wasm, "RND WRITE")
rnd_write_windows = create_df(mass_storage_windows_native, mass_storage_windows_wasm, "RND WRITE")

plot_boxplot(seq_read_x86, "Sequential read speed (x86 Linux)", "figures/seq_read_x86.png")
plot_boxplot(seq_read_aarch64, "Sequential read speed (AArch64 Linux)", "figures/seq_read_aarch64.png")
plot_boxplot(seq_read_windows, "Sequential read speed (x86 Windows)", "figures/seq_read_windows.png")

plot_boxplot(seq_write_x86, "Sequential write speed (x86 Linux)", "figures/seq_write_x86.png")
plot_boxplot(seq_write_aarch64, "Sequential write speed (AArch64 Linux)", "figures/seq_write_aarch64.png")
plot_boxplot(seq_write_windows, "Sequential write speed (x86 Windows)", "figures/seq_write_windows.png")

plot_boxplot(rnd_read_x86, "Random read speed (x86 Linux)", "figures/rnd_read_x86.png")
plot_boxplot(rnd_read_aarch64, "Random read speed (AArch64 Linux)", "figures/rnd_read_aarch64.png")
plot_boxplot(rnd_read_windows, "Random read speed (x86 Windows)", "figures/rnd_read_windows.png")   

plot_boxplot(rnd_write_x86, "Random write speed (x86 Linux)", "figures/rnd_write_x86.png")
plot_boxplot(rnd_write_aarch64, "Random write speed (AArch64 Linux)", "figures/rnd_write_aarch64.png")
plot_boxplot(rnd_write_windows, "Random write speed (x86 Windows)", "figures/rnd_write_windows.png")