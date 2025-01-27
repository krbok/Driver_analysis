import pandas as pd

def get_processed_data():
    # Your preprocessing code from the notebook
    file_path = '/content/dataset_1.csv'
    df = pd.read_csv(file_path)
    
    # Preprocessing steps
    df['Date'] = df['Date'].fillna(method='ffill')
    df['datetime'] = pd.to_datetime(df['Date'], format='%d-%b-%y') + pd.to_timedelta(df['Time (Local)'])
    df.columns = df.columns.str.strip()
    df = df.sort_values(by='datetime').reset_index(drop=True)
    
    return df