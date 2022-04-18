import pandas as pd

TIME_LIST = ['201910', '201911', '201912', '202001', '202002', '202003', '202004', '202005', '202006', '202007',
             '202008', '202009', '202010', '202011', '202012', '202101', '202102', '202103', '202104', '202105',
             '202106', '202107', '202108', '202109']


def prepare_data(df):
    pd.set_option('display.max_rows', df.shape[0] + 1)
    pd.set_option('display.max_columns', df.shape[1] + 1)
    # replace blank with 0
    df.fillna({'202103': 0, '202104': 0, '202105': 0, '202106': 0, '202107': 0, '202108': 0, '202109': 0},
              inplace=True)
    print(df.isna().sum().sum())
    # delete useless figures in this project
    for x in df.index:
        if df.loc[x, 'Minor Class Description'] == 'Murder':
            df.drop(x, inplace=True)
        elif df.loc[x, 'Minor Class Description'] == 'Snatches':
            df.drop(x, inplace=True)
        elif df.loc[x, 'Minor Class Description'] == 'Going Equipped':
            df.drop(x, inplace=True)
        elif df.loc[x, 'Major Class Description'] == 'Fraud or Forgery':
            df.loc[x, 'Minor Class Description'] = 'Fraud or Forgery'
        elif df.loc[x, 'Minor Class Description'] == 'Burglary - Business and Community':
            df.loc[x, 'Minor Class Description'] = 'Business and Community'
        elif df.loc[x, 'Minor Class Description'] == 'Burglary - Residential':
            df.loc[x, 'Minor Class Description'] = 'Residential'
        elif df.loc[x, 'Minor Class Description'] == 'Criminal Damage To M/V':
            df.loc[x, 'Minor Class Description'] = 'Damage To M/V'
        elif df.loc[x, 'Minor Class Description'] == 'Criminal Damage To Other Bldg':
            df.loc[x, 'Minor Class Description'] = 'Damage To Other Bldg'
    for m in df.index:
        if df.loc[m, 'Borough'] == 'Aviation Security(SO18)':
            for n in df.index:
                if df.loc[n, 'Borough'] == 'Hillingdon' \
                        and df.loc[n, 'Minor Class Description'] == df.loc[m, 'Minor Class Description']:
                    for time in TIME_LIST:
                        df.loc[n, time] = df.loc[n, time] + df.loc[m, time]
            df.drop(m, inplace=True)
    # Total number of crime with month and class
    df['Total'] = df.sum(axis=1, numeric_only=True)
    df2 = df.groupby('Borough')[TIME_LIST].sum()
    df2['Total'] = df2.sum(axis=1, numeric_only=True)
    df2.loc['average'] = round(df2.mean(numeric_only=True))
    df2.to_csv("data/Borough_dataset.csv")

    df.loc["total by month"] = df.sum(numeric_only=True)
    df.loc["total by month", 'Borough'] = 'Total By Month'
    df.loc["total by month", 'Major Class Description'] = 'Total'
    df.loc["total by month", 'Minor Class Description'] = 'Total'
    df.to_csv("data/cleaned_dataset.csv", index=False)

    df3 = df.groupby(['Borough','Major Class Description'])[TIME_LIST].sum()
    df3['Total'] = df3.sum(axis=1, numeric_only=True)
    df3.to_csv("data/Classified_dataset.csv")

if __name__ == '__main__':
    df_raw = pd.read_csv('../data/Business Crime Borough Level.csv')
    prepare_data(df_raw)
