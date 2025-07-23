import gzip
import numpy as np
import pandas as pd
import os
from datetime import datetime

input_filename = "D:\\DATN\\2021"
output_filename = "test-quychau-area-2021.xlsx"

dfs = []

def find_gz_files(root_folder):
    """Recursively find all .dat.gz files in directory and subdirectories"""
    gz_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".dat.gz"):
                full_path = os.path.join(dirpath, filename)
                gz_files.append(full_path)
    return gz_files

# Convert bytes to a 1D array of floats
def process_file(path):
# read the compressed file
    with gzip.open(path, 'rb') as f:
        file_bytes = f.read()
    float_array = np.frombuffer(file_bytes, dtype=np.float32).reshape((1200,3600))  # '<f4' also works

    # extract datetime from filename (assuming format: mapyyyymmdd.hhmm.dat.gz)
    filename = path.split('\\')[-1]  # get just the filename part
    datetime_str = filename[10:23]  # extract yyyymmddhhmm
    file_datetime = datetime.strptime(datetime_str, "%Y%m%d.%H%M")

# reshape into a 2d array 1200 rows 3600 columns
# f = float_array.reshape((1200, 3600))
    subset = float_array[380:410, 1010:1060]
    processed_subset = np.where(
        subset <= 0,
        subset.astype(int),  # convert ≤0 to int
        np.round(subset, 2),  # round >0 to 2 decimals
    )
    total_subs = processed_subset.sum()
    print(total_subs) #numpy.ndarray
#code ngu hoc start here $$$$$$$$$$$$$$$$$
    # str_mx = np.array2string(processed_subset, separator=' ', threshold=np.inf, max_line_width=np.inf)
    # # print(str_mx) # class str
    #
    # str_mxa = str_mx.replace("'", "").replace("[", "").replace("]", "")
    # print(str_mxa)

# (optional) save to a text file
# np.savetxt(output_filename, str_mxa, fmt='%s', delimiter=' ')  # fmt='%f' ensures float format
    # with open(output_filename, 'w') as f:
    #     f.write(str_mxa)
#excel
    df = pd.DataFrame({'Time':[file_datetime],'Total rain':[total_subs]})
    dfs.append(df)

def main():
    all_files = find_gz_files(input_filename)
    print(f"Found {len(all_files)} .dat.gz files to process")

    for filepath in all_files:
        process_file(filepath)

    final_df = pd.concat(dfs, ignore_index=True)
    final_df.to_excel(output_filename, index=True, header=False)
    print("Success !!")
if __name__ == "__main__":
    main()
