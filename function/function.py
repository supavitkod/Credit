def select_first_month(df):
    df = df[df['STATUS'] != 'X'].groupby('ID').first().reset_index()
    return df
    
    