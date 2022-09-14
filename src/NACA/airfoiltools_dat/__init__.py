"""

"""
import os

import diskcache
import os.path

import pandas
from matplotlib import pyplot as plt
from pandas import Series
from diskcache import Cache
from pandas import Series, DataFrame

airfoiltools_cache = Cache(os.path.join(os.path.dirname(__file__), "cache"))

class AirfoilToolsDatFile(object):


    def __init__(self, filename: str):
        self.filename = filename
        self.data = pandas.read_csv(filename, sep='\s+', names=['x', 'y'], skiprows=1, index_col=False)
        # print(self.data)
        self.turning_point = self.data['x'].abs().idxmin() # Find the index of the turning point (x=0)


        self.xu = self.data['x'][:self.turning_point+1][::-1].reset_index()
        self.yu= self.data['y'][:self.turning_point + 1][::-1].reset_index()

        # print(self.xu)
        # print(self.yu)
        self.xl = self.data['x'][self.turning_point:].reset_index()
        self.xl.rename(columns={'x': 'xl'}, inplace=True)
        self.yu.rename(columns={'y': "yu"}, inplace=True)
        self.yl = self.data['y'][self.turning_point:].reset_index()
        self.yl.rename(columns={'y': 'yl'}, inplace=True)
        self.xu.rename(columns={'x': 'xu'}, inplace=True)

        self.df = pandas.concat([self.xu["xu"], self.yu["yu"], self.xl["xl"], self.yl["yl"]], axis=1)
        self.s = len(self.df)-1
        # print(self.df)
        # print(self.turning_point)
        # print(self.x)
        # print(self.yu)
        # print(self.yl)

    @staticmethod
    @airfoiltools_cache.memoize("airfoil",expire=0, tag="airfoiltools_dat")
    def load(designation: str) -> DataFrame:
        #todo: load dat file from airfoiltools.com
        raise NotImplementedError
    def plot(self) -> None:
        """
        Plots the airfoil.
        :return: None
        """

        fig, ax = plt.subplots()
        ax.plot(self.df["xu"], self.df["yu"])
        ax.plot(self.df["xl"], self.df["yl"])
        if "xc" in self.df.columns.tolist() and "yc" in self.df.columns.tolist():
            ax.plot(self.df["xc"], self.df["yc"])
        # ax.plot(self.df["xc"], self.df["yc"])
        fig.legend(["Upper Surface", "Lower Surface", "Camber Line"])
        plt.title(f"{os.path.splitext(os.path.basename(self.filename))[0]} Airfoil (Loaded from AirfoilTools.com)")
        # plt.xlim(0, 1)
        # plt.ylim(-0.5, 0.5)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()


if __name__ == "__main__":
    a = AirfoilToolsDatFile("NACA/tests/data/airfoiltools/NACA2412.dat")
    print(a.df)
    # a.plot()