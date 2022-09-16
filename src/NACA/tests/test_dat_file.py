import string
from random import randint, choice
from timeit import timeit

from numpy import isclose

from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestAirfoilToolsDatFile():
    def testAirfoilToolsDatFile(self):
        filename = "NACA/tests/data/airfoiltools/NACA0012.dat"
        a = AirfoilToolsDatFile(filename)
        assert a.s ==100
        assert a.designation == "0012"
        assert  all(isclose(a.df["yu"],a.df["yl"]*-1))
        assert a.data["x"][a.turning_point] == 0


class TestScraper():
    def testScraper(self):
        a = AirfoilToolsDatFile.load("0012", 100, cs=False, ct=True)
        filename = "NACA/tests/data/airfoiltools/NACA0012.dat"
        a2 = AirfoilToolsDatFile(filename)

        assert a.s == a2.s
        assert a.df["yu"][1] == a2.df["yu"][1]
        assert a.df["yl"][1] == a2.df["yl"][1]
        assert a.df["xu"][a.s // 2] == a2.df["xu"][a.s // 2]
        assert a.df["xl"][a.s // 2] == a2.df["xl"][a.s // 2]
        assert all(a.df["yu"] == a2.df["yu"])
        assert all(a.df == a2.df)


    def testScraper2(self):
        a = AirfoilToolsDatFile.load("0012", 100, cs=True, ct=True)
        filename = "NACA/tests/data/airfoiltools/NACA0012_cs.dat"
        a2 = AirfoilToolsDatFile(filename)

        assert a.s == a2.s
        assert a.df["yu"][1] == a2.df["yu"][1]
        assert a.df["yl"][1] == a2.df["yl"][1]
        assert a.df["xu"][a.s // 2] == a2.df["xu"][a.s // 2]
        assert a.df["xl"][a.s // 2] == a2.df["xl"][a.s // 2]
        assert all(a.df["yu"] == a2.df["yu"])
        assert all(a.df == a2.df)

    def testScraper_caching(self):
        from src.NACA.airfoiltools_dat import airfoiltools_cache
        hits, misses = airfoiltools_cache.stats()
        a= AirfoilToolsDatFile.load("0012", 100, cs=True, ct=True)

        hits2, misses2 = airfoiltools_cache.stats()
        assert hits2 == hits + 1

        print(timeit( "AirfoilToolsDatFile.load('2222', 100, cs=True, ct=True)", globals=globals(), number=1))
        print(timeit( "AirfoilToolsDatFile.load('2222', 100, cs=True, ct=True)", globals=globals(), number=1))


