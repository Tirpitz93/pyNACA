"""

"""
import logging
import os
import re
from io import StringIO
from logging import getLogger, basicConfig

import diskcache
import os.path

import pandas
import requests
from matplotlib import pyplot as plt
from pandas import Series
from diskcache import Cache
from pandas import Series, DataFrame
logger = getLogger(__name__)
basicConfig(level=logging.DEBUG)

airfoiltools_cache = Cache(os.path.join(os.path.dirname(__file__), "cache"))

logger.error(airfoiltools_cache.stats())

class AirfoilToolsDatFile(object):

    def __init__(self, filename: str=None, file=None):
        self.designation = "None"
        if file is not None:
            self.populate(file)
            self.designation = filename
        elif filename is not None:
            with open(filename, "r") as f:
                f.readline()
                self.populate(f)
            print(filename)
            self.designation = re.match(r"(.*)?NACA([\d]{4,})(.*)?",filename)[2]
            print(self.designation)

        # self.filename = filename



    def populate(self, file):
        self.data = pandas.read_csv(file, sep='\s+', names=['x', 'y'], skiprows=0, index_col=False)
        # print(self.data)
        self.turning_point = self.data['x'].abs().idxmin()  # Find the index of the turning point (x=0)
        self.xu = self.data['x'][:self.turning_point + 1][::-1].reset_index()
        self.yu = self.data['y'][:self.turning_point + 1][::-1].reset_index()
        # print(self.xu)
        # print(self.yu)
        self.xl = self.data['x'][self.turning_point:].reset_index()
        self.xl.rename(columns={'x': 'xl'}, inplace=True)
        self.yu.rename(columns={'y': "yu"}, inplace=True)
        self.yl = self.data['y'][self.turning_point:].reset_index()
        self.yl.rename(columns={'y': 'yl'}, inplace=True)
        self.xu.rename(columns={'x': 'xu'}, inplace=True)
        self.df = pandas.concat([self.xu["xu"], self.yu["yu"], self.xl["xl"], self.yl["yl"]], axis=1)
        self.s = len(self.df) - 1

    @staticmethod
    # @airfoiltools_cache.memoize("airfoil", expire=None, tag="airfoiltools_dat")
    def load(designation: str, s: int = 100, cs: bool = True, ct: bool = False) -> "AirfoilToolsDatFile":
        """
        Loads an airfoil from the airfoiltools.com database.
        :param designation:
        :return:
        """
        if len(designation) == 4:
            url = f"http://airfoiltools.com/airfoil/naca4digit?MNaca4DigitForm%5Bcamber%5D={designation[0]}&MNaca4DigitForm%5Bposition%5D={int(designation[1]) * 10}&MNaca4DigitForm%5Bthick%5D={designation[2:]}&MNaca4DigitForm%5BnumPoints%5D={s*2}&MNaca4DigitForm%5BcosSpace%5D={int(cs)}&MNaca4DigitForm%5BcosSpace%5D={int(cs)}&MNaca4DigitForm%5BcloseTe%5D={int(ct)}&MNaca4DigitForm%5BcloseTe%5D={int(ct)}&yt0=Plot"
        elif len(designation) == 5:
            url= f"http://airfoiltools.com/airfoil/naca5digit?MNaca5DigitForm%5Bcl%5D={3/20*int(designation[0])}&MNaca5DigitForm%5BposKey%5D={5*int(designation[1])}_{designation[2]}&MNaca5DigitForm%5Bthick%5D={int(designation[3:])}&MNaca5DigitForm%5BnumPoints%5D={s*2}&MNaca5DigitForm%5BcosSpace%5D={int(cs)}&MNaca5DigitForm%5BcosSpace%5D={int(cs)}&MNaca5DigitForm%5BcloseTe%5D={int(ct)}&MNaca5DigitForm%5BcloseTe%5D={int(ct)}&yt0=Plot"

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        # print(url)
        # print(soup)
        # print(soup.find("pre").text)
        text = soup.find("pre").text.strip().split("\n", maxsplit=1)[1]
        print(url)
        try:
            assert soup.find("title").text.find(designation)!=-1
        except AssertionError as e:
            print(soup.find("title").text)
            print(designation)
            print(url)


        # print(text)
        return AirfoilToolsDatFile(file=StringIO(text), filename=designation)


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
        plt.title(f"{self.designation} Airfoil (Loaded from AirfoilTools.com)")
        # plt.xlim(0, 1)
        plt.ylim(-0.2, 0.2)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()


if __name__ == "__main__":
    a = AirfoilToolsDatFile("NACA/tests/data/airfoiltools/NACA2412.dat")
    print(a.df)
    # a.plot()
