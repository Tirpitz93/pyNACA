"""

"""
import pandas
from matplotlib import pyplot as plt
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
        # plt.xlim(0, 1)
        # plt.ylim(-0.5, 0.5)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()


if __name__ == "__main__":
    a = AirfoilToolsDatFile("NACA/tests/data/airfoiltools/NACA2412.dat")
    print(a.df)
    a.plot()