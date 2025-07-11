import gzip
import numpy as np
import psycopg2
from datetime import datetime
import os
import pandas as pd

input_folder = "D:\\DATN\\2021\\01"
input_station = "./MucNuoc.xlsx"

db_config = {
    "host": "localhost",
    "user": "admin",
    "password": "123456",
    "database": "rainmap"
}

def find_gz_files(root_folder):
    """Recursively find all .dat.gz files in directory and subdirectories"""
    gz_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".dat.gz"):
                full_path = os.path.join(dirpath, filename)
                gz_files.append(full_path)
    return gz_files

def process_file(path, cursor):
    try:
        
        # Read the compressed file
        with gzip.open(path, 'rb') as f:
            file_bytes = f.read()

        # Read the XLSX file (skip 1st column using 'usecols')
        df = pd.read_excel(input_station, usecols=[1,2,3,4,5],  nrows=745)

        # Extract datetime from filename (assuming format: mapYYYYMMDD.HHMM.dat.gz)
        filename = path.split('\\')[-1]  # Get just the filename part
        datetime_str = filename[10:23]  # Extract YYYYMMDDHHMM
        file_datetime = datetime.strptime(datetime_str, "%Y%m%d.%H%M")

        # Convert bytes to a 1D array of floats
        float_array = np.frombuffer(file_bytes, dtype=np.float32).reshape((1200,3600))  # '<f4' also works

        # Mường Xén vĩ độ 19(410)-22(380) kinh độ 102-108 (30x60)
        subset_mx = float_array[380:410, 1020:1080]
        pr_subset_mx = np.where(
            subset_mx <= 0,
            subset_mx.astype(int).astype(str),  # Convert ≤0 to int
            np.round(subset_mx, 1).astype(str)  # Round >0 to 2 decimals
        )

        
        # # Xử lý dữ liệu
        str_mx = np.array2string(pr_subset_mx, separator=' ', threshold=np.inf, max_line_width=np.inf)
        str_mx = str_mx.replace("'", "").replace("[", "").replace("]", "")
        #Insert xlsx data
        for _, row in df.iterrows():
            cols = ','.join([f'"{c}"' for c in df.columns])
            values = ','.join(['%s'] * len(df.columns))
            int_list = [int(x) for x in row]
            
        cursor.execute(
                """INSERT INTO map_muongxen (date_time, data, st_quy_chau, st_muong_lat, st_xa_la, st_cua_dat, st_muong_xen)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,(file_datetime,str_mx, int_list[0],int_list[1],int_list[2],int_list[3],int_list[4],)
        )
            
        return True
    except Exception as e:
        print(f"Error processing {path}: {str(e)}")
        return False


def main():
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
     
    # Find and process files
    all_files = find_gz_files(input_folder)
    print(f"Found {len(all_files)} .dat.gz files to process")
    
    # Process all .dat.gz files in input folder
    processed_files = 0
    for filepath in all_files:
        if process_file(filepath, cursor):
            processed_files += 1
            print(processed_files)

    conn.commit()
    conn.close()
    print(f"Successfully processed {processed_files} files")

if __name__ == "__main__":
    main()
