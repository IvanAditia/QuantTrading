from tabulate import tabulate

def indicator(df):

    df['mean'] =  df['close'].rolling(14).mean()

    df['sd'] = df['close'].rolling(14).std()

    print(
        tabulate(
            df[['mean', 'sd']].tail(10),
            headers='keys',
            tablefmt='grid'
        )
    )
    return df