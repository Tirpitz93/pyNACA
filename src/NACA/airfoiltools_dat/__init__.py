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
        self.x = self.data['x'][self.turning_point:].reset_index()
        self.top= self.data['y'][:self.turning_point+1][::-1].reset_index()
        self.top.rename(columns={'y': 'top'}, inplace=True)
        self.bottom = self.data['y'][self.turning_point:].reset_index()
        self.bottom.rename(columns={'y': 'bottom'}, inplace=True)
        self.df = pandas.concat([self.x["x"], self.top["top"], self.bottom["bottom"]], axis=1)
        # print(self.turning_point)
        # print(self.x)
        # print(self.top)
        # print(self.bottom)




if __name__ == "__main__":
    a = AirfoilToolsDatFile("src/NACA/tests/data/airfoiltools/NACA0012.dat")
    print(a.df)