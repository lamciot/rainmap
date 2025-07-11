import pandas as pd

def calculate_depend(df):
    """
    Implements the Excel formula from column D:
    =IF(C>0, IF(B_next>B,1,0), IF(B_next=B,1,0))
    """
    df['is_rain_quy_chau'] = pd.NA # Initialize column
    for i in range(len(df) - 1):
        if pd.notna(df.at[i, 'rain_quy_chau']) and pd.notna(df.at[i+1, 'rain_quy_chau']):
            if df.at[i, 'rain_quy_chau'] > 0:
                df.at[i, 'is_rain_quy_chau'] = 1 if df.at[i+1, 'st_quy_chau'] > df.at[i, 'st_quy_chau'] else 0
            else:
                df.at[i, 'is_rain_quy_chau'] = 1 if df.at[i+1, 'st_quy_chau'] == df.at[i, 'st_quy_chau'] else 0
    return df

def calculate_ratios(df):
    """
    Calculates the ratios from column E:
    =COUNTIF(D2:D11,1)/SUM(D2:D11) and similar for 0
    """
    # Filter out empty rows in 'depend' column
    depend_values = df['is_rain_quy_chau'].dropna()
    
    count_1 = (depend_values == 1).sum()
    count_0 = (depend_values == 0).sum()
    total = count_1 + count_0
    
    ratio_1 = count_1 / total if total > 0 else 0
    ratio_0 = count_0 / total if total > 0 else 0
    
    return count_1, count_0, ratio_1, ratio_0

def main():
    # Read the Excel file
    try:
        df = pd.read_excel('MucNuoc-2021.xlsx', sheet_name='Sheet1', nrows=8760) #Dem so dong !!!!
        
        # Clean the data - remove empty rows and reset index
        df = df.dropna(how='all').reset_index(drop=True)
        
        # Calculate the 'depend' column
        df = calculate_depend(df)
        
        # Calculate the ratios
        count_1, count_0, ratio_1, ratio_0 = calculate_ratios(df)
        
        # Print results
        print("Processed Data:")
        # print(df[['st_quy_chau', 'rain_quy_chau', 'is_rain_quy_chau']])
        print("Depend 1:", count_1)
        print("Depend 0:", count_0)
        print(f"Ratio of 1s: {ratio_1:.4f}")
        print(f"Ratio of 0s: {ratio_0:.4f}")
        
        
    except FileNotFoundError:
        print("Error: File '*.xlsx' not found. Please ensure it's in the same directory.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()