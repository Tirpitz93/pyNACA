"""

"""
import pandas
from pandas import Series


class AirfoilToolsDatFile(object):


    def __init__(self, filename: str):
        self.filename = filename
        self.data = pandas.read_csv(filename, sep='\s+', names=['x', 'y'], skiprows=1, index_col=False)
        # print(self.data)
        self.turning_point = self.data['x'].idxmin()
        self.xl = self.data['x'][self.turning_point:].reset_index()
        self.xu = self.data['x'][:self.turning_point+1][::-1].reset_index()
        self.top= self.data['y'][:self.turning_point+1][::-1].reset_index()
        self.xl.rename(columns={'x': 'xl'}, inplace=True)
        self.top.rename(columns={'y': "yu"}, inplace=True)
        self.bottom = self.data['y'][self.turning_point:].reset_index()
        self.bottom.rename(columns={'y': 'yl'}, inplace=True)
        self.xu.rename(columns={'x': 'xu'}, inplace=True)

        self.df = pandas.concat([self.xu["xu"], self.top["yu"],self.xl["xl"], self.bottom["yl"]], axis=1)
        print(self.df)
        # print(self.turning_point)
        # print(self.x)
        # print(self.top)
        # print(self.bottom)




if __name__ == "__main__":
    a = AirfoilToolsDatFile("src/NACA/tests/data/airfoiltools/NACA0012.dat")
    print(a.df)