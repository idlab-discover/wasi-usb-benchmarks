from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
def add_labels_barplot(y):
    ylim = plt.gca().get_ylim()
    yrange = ylim[1] - ylim[0]
    for i in range(len(y)):
        if i % 2 == 0:
            plt.text(
                i, y[i] + yrange * 0.0075, f"{y[i]:.0f} kB", ha="center", va="bottom"
            )
        else:
            percentage_increase = (y[i] - y[i - 1]) / y[i - 1] * 100
            plt.text(
                i,
                y[i] + yrange * 0.0075,
                f"{y[i]:.0f} kB ({percentage_increase:+.1f}%)",
                ha="center",
                va="bottom",
            )


def add_labels_boxplot(y, unit: str, precision: int = 0):
    ylim = plt.gca().get_ylim()
    yrange = ylim[1] - ylim[0]
    for i in range(len(y)):
        if i % 2 == 0:
            plt.text(
                i + 1.1,
                y[i] + yrange * 0.02,
                f"{y[i]:.{precision}f} {unit}",
                ha="left",
                va="top",
            )
        else:
            percentage_increase = (y[i] - y[i - 1]) / y[i - 1] * 100
            plt.text(
                i + 1.1,
                y[i] + yrange * 0.02,
                f"{y[i]:.{precision}f} {unit}\n({percentage_increase:+.1f}%)",
                ha="left",
                va="top",
            )


plt.figure(figsize=(10, 6))
plt.ylabel("File Size (kB)")
x = [
    "x86 Linux\nBaseline",
    "x86 Linux\nUSB",
    "AArch64 Linux\nBaseline",
    "AArch64 Linux\nUSB",
    "x86 Windows\nBaseline",
    "x86 Windows\nUSB",
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
add_labels_barplot(y)
plt.savefig("figures/filesize.svg")
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

plt.figure(figsize=(10, 6))
plt.ylabel("Memory Usage (kB)")
x = [
    "x86 Linux\nBaseline",
    "x86 Linux\nUSB",
    "AArch64 Linux\nBaseline",
    "AArch64 Linux\nUSB",
    "x86 Windows\nBaseline",
    "x86 Windows\nUSB",
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
add_labels_barplot(y)
plt.savefig("figures/memory.svg")
plt.close()

######### Throughput #########

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


def plot_boxplot(df: pd.DataFrame, title: str, filename: str):
    # fig = plt.figure(figsize=(6, 6))
    df.plot(kind="box", title=title, figsize=(6, 4))
    (ylim_low, ylim_high) = plt.gca().get_ylim()
    plt.gca().set_ylim(0, ylim_high*1.025)
    plt.ylabel("Speed (MB/s)")
    add_labels_boxplot([df["Native"].median(), df["WebAssembly"].median()], "MB/s", 1)
    plt.gca()
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
seq_read_aarch64 = create_df(
    mass_storage_aarch64_native, mass_storage_aarch64_wasm, "SEQ READ"
)
seq_read_windows = create_df(
    mass_storage_windows_native, mass_storage_windows_wasm, "SEQ READ"
)

seq_write_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "SEQ WRITE")
seq_write_aarch64 = create_df(
    mass_storage_aarch64_native, mass_storage_aarch64_wasm, "SEQ WRITE"
)
seq_write_windows = create_df(
    mass_storage_windows_native, mass_storage_windows_wasm, "SEQ WRITE"
)

rnd_read_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "RND READ")
rnd_read_aarch64 = create_df(
    mass_storage_aarch64_native, mass_storage_aarch64_wasm, "RND READ"
)
rnd_read_windows = create_df(
    mass_storage_windows_native, mass_storage_windows_wasm, "RND READ"
)

rnd_write_x86 = create_df(mass_storage_x86_native, mass_storage_x86_wasm, "RND WRITE")
rnd_write_aarch64 = create_df(
    mass_storage_aarch64_native, mass_storage_aarch64_wasm, "RND WRITE"
)
rnd_write_windows = create_df(
    mass_storage_windows_native, mass_storage_windows_wasm, "RND WRITE"
)

plot_boxplot(
    seq_read_x86, "Sequential read speed (x86 Linux)", "figures/seq_read_x86.svg"
)
plot_boxplot(
    seq_read_aarch64,
    "Sequential read speed (AArch64 Linux)",
    "figures/seq_read_aarch64.svg",
)
plot_boxplot(
    seq_read_windows,
    "Sequential read speed (x86 Windows)",
    "figures/seq_read_windows.svg",
)

plot_boxplot(
    seq_write_x86, "Sequential write speed (x86 Linux)", "figures/seq_write_x86.svg"
)
plot_boxplot(
    seq_write_aarch64,
    "Sequential write speed (AArch64 Linux)",
    "figures/seq_write_aarch64.svg",
)
plot_boxplot(
    seq_write_windows,
    "Sequential write speed (x86 Windows)",
    "figures/seq_write_windows.svg",
)

plot_boxplot(rnd_read_x86, "Random read speed (x86 Linux)", "figures/rnd_read_x86.svg")
plot_boxplot(
    rnd_read_aarch64,
    "Random read speed (AArch64 Linux)",
    "figures/rnd_read_aarch64.svg",
)
plot_boxplot(
    rnd_read_windows, "Random read speed (x86 Windows)", "figures/rnd_read_windows.svg"
)

plot_boxplot(
    rnd_write_x86, "Random write speed (x86 Linux)", "figures/rnd_write_x86.svg"
)
plot_boxplot(
    rnd_write_aarch64,
    "Random write speed (AArch64 Linux)",
    "figures/rnd_write_aarch64.svg",
)
plot_boxplot(
    rnd_write_windows,
    "Random write speed (x86 Windows)",
    "figures/rnd_write_windows.svg",
)

print("x86 Linux webassembly vs native median")
print(f"Delta: {np.median(seq_read_x86['Native']) - np.median(seq_read_x86['WebAssembly']):.2f} MB/s")
print("AArch64 Linux webassembly vs native median")
print(f"Delta: {np.median(seq_read_aarch64['Native']) - np.median(seq_read_aarch64['WebAssembly']):.2f} MB/s")
print("Windows webassembly vs native median")
print(f"Delta: {np.median(seq_read_windows['Native']) - np.median(seq_read_windows['WebAssembly']):.2f} MB/s")

######### Latency #########


def load_latency_file(filename):
    return np.array([float(i) for i in Path(filename).read_text().splitlines()])


# In milliseconds
latency_bulk_x86_native_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_x86_native_32bytes.txt"
)
latency_bulk_x86_wasm_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_x86_wasm_32bytes.txt"
)
latency_bulk_aarch64_native_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_aarch64_native_32bytes.txt"
)
latency_bulk_aarch64_wasm_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_aarch64_wasm_32bytes.txt"
)
latency_bulk_windows_native_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_windows_native_32bytes.txt"
)
latency_bulk_windows_wasm_32bytes = load_latency_file(
    "./ping-bulk/latencies_in_ms_windows_wasm_32bytes.txt"
)

latency_interrupt_x86_native_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_x86_native_32bytes.txt"
)
latency_interrupt_x86_wasm_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_x86_wasm_32bytes.txt"
)
latency_interrupt_aarch64_native_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_aarch64_native_32bytes.txt"
)
latency_interrupt_aarch64_wasm_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_aarch64_wasm_32bytes.txt"
)
latency_interrupt_windows_native_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_windows_native_32bytes.txt"
)
latency_interrupt_windows_wasm_32bytes = load_latency_file(
    "./ping-interrupt/latencies_in_ms_windows_wasm_32bytes.txt"
)

latency_isochronous_x86_native_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_x86_native_32bytes.txt"
)
latency_isochronous_x86_wasm_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_x86_wasm_32bytes.txt"
)
latency_isochronous_aarch64_native_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_aarch64_native_32bytes.txt"
)
latency_isochronous_aarch64_wasm_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_aarch64_wasm_32bytes.txt"
)
latency_isochronous_windows_native_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_windows_native_32bytes.txt"
)
latency_isochronous_windows_wasm_32bytes = load_latency_file(
    "./ping-isochronous/latencies_in_ms_windows_wasm_32bytes.txt"
)


def plot_latencies(latencies: list[np.ndarray], title: str, filename: str):
    plt.figure(figsize=(6, 4))
    plt.boxplot(latencies, labels=["Native", "WebAssembly"])
    (ylim_low, ylim_high) = plt.gca().get_ylim()
    plt.gca().set_ylim(0, ylim_high*1.025)
    add_labels_boxplot([np.median(l) for l in latencies], "ms", 3)
    plt.title(title)
    plt.ylabel("Latency (ms)")
    plt.savefig(filename)
    plt.close()


plot_latencies(
    [latency_bulk_x86_native_32bytes, latency_bulk_x86_wasm_32bytes],
    "Bulk Endpoint Latency, 32-byte packet (x86 Linux)",
    "figures/latency_32bytes_bulk_x86.svg",
)
plot_latencies(
    [latency_bulk_aarch64_native_32bytes, latency_bulk_aarch64_wasm_32bytes],
    "Bulk Endpoint Latency, 32-byte packet (AArch64 Linux)",
    "figures/latency_32bytes_bulk_aarch64.svg",
)
plot_latencies(
    [latency_bulk_windows_native_32bytes, latency_bulk_windows_wasm_32bytes],
    "Bulk Endpoint Latency, 32-byte packet (x86 Windows)",
    "figures/latency_32bytes_bulk_windows.svg",
)

plot_latencies(
    [latency_interrupt_x86_native_32bytes, latency_interrupt_x86_wasm_32bytes],
    "Interrupt Endpoint Latency, 32-byte packet (x86 Linux)",
    "figures/latency_32bytes_interrupt_x86.svg",
)
plot_latencies(
    [latency_interrupt_aarch64_native_32bytes, latency_interrupt_aarch64_wasm_32bytes],
    "Interrupt Endpoint Latency, 32-byte packet (AArch64 Linux)",
    "figures/latency_32bytes_interrupt_aarch64.svg",
)
plot_latencies(
    [latency_interrupt_windows_native_32bytes, latency_interrupt_windows_wasm_32bytes],
    "Interrupt Endpoint Latency, 32-byte packet (x86 Windows)",
    "figures/latency_32bytes_interrupt_windows.svg",
)

plot_latencies(
    [latency_isochronous_x86_native_32bytes, latency_isochronous_x86_wasm_32bytes],
    "Isochronous Endpoint Latency, 32-byte packet (x86 Linux)",
    "figures/latency_32bytes_isochronous_x86.svg",
)
plot_latencies(
    [
        latency_isochronous_aarch64_native_32bytes,
        latency_isochronous_aarch64_wasm_32bytes,
    ],
    "Isochronous Endpoint Latency, 32-byte packet (AArch64 Linux)",
    "figures/latency_32bytes_isochronous_aarch64.svg",
)
plot_latencies(
    [
        latency_isochronous_windows_native_32bytes,
        latency_isochronous_windows_wasm_32bytes,
    ],
    "Isochronous Endpoint Latency, 32-byte packet (x86 Windows)",
    "figures/latency_32bytes_isochronous_windows.svg",
)
