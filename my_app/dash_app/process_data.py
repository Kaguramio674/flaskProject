import pandas as pd


class CrimeData:

    def __init__(self):
        self.borough_data = pd.DataFrame()
        self.crime_data = pd.DataFrame()
        self.minor_class_list = pd.DataFrame()
        self.classified_data = pd.DataFrame()
        self.crime_dataset_area = []
        self.average_data = []
        self.compare_to_ave = 0
        self.compare_month_to_ave = 0
        self.compare_last_month = 0
        self.ratio_total = 0
        self.crime_borough = []
        self.classified_borough = []
        self.area_list = []
        self.major_class_list = []
        self.get_data()
        self.TIME_LIST = ['201910', '201911', '201912', '202001', '202002', '202003', '202004', '202005', '202006',
                          '202007', '202008', '202009', '202010', '202011', '202012', '202101', '202102', '202103',
                          '202104', '202105', '202106', '202107', '202108', '202109']

    def get_data(self):
        try:
            self.borough_data = pd.read_csv('data/Borough_dataset.csv')
            self.crime_data = pd.read_csv('data/cleaned_dataset.csv')
            self.classified_data = pd.read_csv('data/Classified_dataset.csv')
        except FileNotFoundError:
            self.borough_data = pd.read_csv('my_app/data/Borough_dataset.csv')
            self.crime_data = pd.read_csv('my_app/data/cleaned_dataset.csv')
            self.classified_data = pd.read_csv('my_app/data/Classified_dataset.csv')
        self.area_list = self.borough_data["Borough"].unique().tolist()
        self.major_class_list = self.crime_data["Major Class Description"].unique().tolist()

    def process_data_for_area(self, major, borough, time_select):
        self.crime_borough = self.borough_data.loc[self.borough_data['Borough'] == borough]
        self.classified_borough = self.classified_data.loc[self.classified_data['Borough'] == borough]
        self.average_data = self.borough_data.loc[self.borough_data['Borough'] == 'average']
        self.compare_to_ave = (self.crime_borough.iloc[-1, -1] -
                               self.average_data.iloc[-1, -1]) * 100 / self.average_data.iloc[-1, -1]
        self.compare_month_to_ave = (self.crime_borough.iloc[-1, time_select] -
                                     self.average_data.iloc[-1, time_select]) * 100 / self.average_data.iloc[-1, time_select]
        if time_select > 1:
            self.compare_last_month = (self.crime_borough.iloc[-1, time_select] - self.crime_borough.iloc[
                -1, time_select - 1]) * 100 / self.crime_borough.iloc[-1, time_select - 1]
        if major is None or major == 'Total':
            major = "Total"
            self.ratio_total = 'N/A'
        else:
            data_temp = self.classified_borough.loc[self.classified_borough['Major Class Description'] == major]
            self.ratio_total = data_temp.iloc[-1, time_select+1] * 100 / self.crime_borough.iloc[-1, time_select]


