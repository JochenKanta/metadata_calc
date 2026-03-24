# Storage Cluster Metadata Calculator

A lightweight Python command-line utility to calculate the metadata reservation (PTU) and the supported number of 4KiB files for storage clusters. 

This tool works bidirectionally: you can input the **total cluster capacity** to find out how many files it supports, or input a **target number of files** to determine how much cluster capacity you need to build.

## 🧮 The Formula
The script uses the following storage logic to determine metadata limits:
* **Total Metadata Reservation (PTU):** 1% of the total usable space.
* **Storage Calculation Base:** 1 TB = 1,000,000,000,000 Bytes.
* **Safety Margin:** 10% of the PTU is reserved as a safety buffer (multiplier of 0.9).
* **File Size:** Calculations are based on a standard 4KiB (4096 Bytes) file size.

*Equation:* `Supported Files = ((1% of Usable Capacity in Bytes) - 10% Margin) / 4096 Bytes`

## 🚀 Prerequisites
* Python 3.6 or higher
* No external libraries required (uses only the built-in `argparse` module)

## 💻 Usage

Run the script from your terminal. You must provide exactly one of the two flags: `-c` (capacity) or `-f` (files).

### 1. Calculate File Count from Capacity (`-c`, `--capacity`)
If you know your cluster size in Terabytes (TB) and want to know how many 4KiB files it can support:

bash
python metadata_calc.py -c 200

'-------------------------------------------------------
Mode: Calculating file count from capacity
-------------------------------------------------------
Cluster Capacity:       200.00 TB
Metadata Reservation:   2.00 TB (1% PTU)
Supported 4kB Files:    439,453,125
-------------------------------------------------------

### 1. Calculate Capacity from File Count   (`-f`, `--files`)
If you know your number of files and want to know the desired cluster size in Terabytes (TB):

python metadata_calc.py -f 439453125


-------------------------------------------------------
Mode: Calculating capacity from file count
-------------------------------------------------------
Desired 4kB Files:          439,453,125
Required Cluster Capacity:  200.00 TB
Resulting PTU Reservation:  2.00 TB (1%)
-------------------------------------------------------

