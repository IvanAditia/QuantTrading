def clean_data(df):

    # rename columns
    df = df.rename(columns={
        'Datetime'  : 'time',   
        'High' : 'high',
        'Low' : 'low',
        'Open' : 'open',
        'Close' : 'close',
        'Volume' : 'tick_volume'
    })

    # memilih kolom yang diperlukan
    df = df[
        ['time', 'high', 'low', 'open', 'close', 'tick_volume']
    ]

    return df