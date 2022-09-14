from src.NACA import NACA
from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestFiveDigit(object):

    def test_24012(self):
        filename = "NACA/tests/data/airfoiltools/NACA24012.dat"
        a = AirfoilToolsDatFile(filename)
        a.plot()
        NACA24112 = NACA.factory("24012", s=a.s, cs=False, precision=6)
        NACA24112.plot()
        print(NACA24112.df)
        assert a.s == NACA24112.s
        assert NACA24112.df["yu"][1] == a.df["yu"][1]
        assert NACA24112.df["yl"][1] == a.df["yl"][1]

    def test_24012_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA24012_cs.dat"
        a = AirfoilToolsDatFile(filename)
        a.plot()
        print(a.df)
        NACA24112 = NACA.factory("24012", s=a.s, cs=True, precision=6)
        NACA24112.plot()
        print(NACA24112.df)
        assert a.s == NACA24112.s
        assert NACA24112.df["xu"][1] == a.df["xu"][1]
        assert NACA24112.df["xl"][1] == a.df["xl"][1]
        assert NACA24112.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert NACA24112.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert NACA24112.df["yu"][1] == a.df["yu"][1]
        assert NACA24112.df["yl"][1] == a.df["yl"][1]
        assert NACA24112.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert NACA24112.df["yl"][a.s//2] == a.df["yl"][a.s//2]