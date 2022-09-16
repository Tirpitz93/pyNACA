import os

from numpy import isclose, round_

from src.NACA import NACABase as NACA
from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestFourDigitSym(object):
    def test_0012(self):
        filename = "NACA/tests/data/airfoiltools/NACA0012.dat"
        a = AirfoilToolsDatFile(filename)
        # a.plot()
        n = NACA.factory("0012", cs=False, precision=6)
        # n.plot()
        # print(n.df.columns.tolist())
        # print(n.df.to_string())
        assert all(n.df["yu"] == n.df["yl"] * -1)
        assert  n.df.loc[0, "yu"] == 0.0
        assert  n.df.loc[0, "yl"] == 0.0
        assert n.df["yu"][50] == a.df["yu"][50]
        assert n.df["xu"][a.s // 2] == a.df["xu"][a.s // 2]
        assert n.df["xl"][a.s // 2] == a.df["xl"][a.s // 2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s // 2] == a.df["yu"][a.s // 2]
        assert n.df["yl"][a.s // 2] == a.df["yl"][a.s // 2]

    def test_c0012_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA0012_cs.dat"
        a = AirfoilToolsDatFile(filename)
        n = NACA.factory("0012", cs=True, precision=6)
        # n.plot()
        # a.plot()
        assert  n.df.loc[0, "yu"] == 0.0
        assert  n.df.loc[0, "yl"] == 0.0
        assert n.df["yu"][1] ==a.df["yu"][1]
        assert n.df["yl"][1] ==a.df["yl"][1]
        assert n.df["yu"][50] == a.df["yu"][50]
        assert n.df["yl"][50] == a.df["yl"][50]
        assert n.df["xu"][a.s // 2] == a.df["xu"][a.s // 2]
        assert n.df["xl"][a.s // 2] == a.df["xl"][a.s // 2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s // 2] == a.df["yu"][a.s // 2]
        assert n.df["yl"][a.s // 2] == a.df["yl"][a.s // 2]


    def test_2412(self):
        filename = "NACA/tests/data/airfoiltools/NACA2412.dat"
        a = AirfoilToolsDatFile(filename)

        assert a.s == 100
        n = NACA.factory("2412", s=a.s, cs=False, precision=6)
        # n.plot()
        # print(n.df)
        assert a.s == n.s
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["xu"][a.s // 2] == a.df["xu"][a.s // 2]
        assert n.df["xl"][a.s // 2] == a.df["xl"][a.s // 2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s // 2] == a.df["yu"][a.s // 2]
        assert n.df["yl"][a.s // 2] == a.df["yl"][a.s // 2]

    def test_2412_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA2412_cs.dat"
        a = AirfoilToolsDatFile(filename)
        # a.plot()
        # print(a.df)
        n = NACA.factory("2412", s=a.s,cs=True, precision=6)
        # n.plot()
        # print(n.df)
        assert a.s == 100
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]


    def test_8412(self):
        filename = "NACA/tests/data/airfoiltools/NACA8412.dat"
        a = AirfoilToolsDatFile(filename)

        assert a.s == 100
        n = NACA.factory("8412", s=a.s, cs=False, precision=6)
        # n.plot()
        # print(n.df)
        assert a.s == n.s
        assert round(n.df["yu"][1], 6) == a.df["yu"][1]
        assert round(n.df["yl"][1], 6) == a.df["yl"][1]

    def test_8412_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA8412_cs.dat"
        a = AirfoilToolsDatFile(filename)
        # a.plot()
        # print(a.df)
        n = NACA.factory("8412", s=a.s,cs=True, precision=6)
        # n.plot()
        # print(n.df)
        assert a.s == 100
        assert a.s == n.s
        assert n.df["xu"][1]== a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]


