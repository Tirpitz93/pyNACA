from matplotlib import pyplot as plt

from src.NACA import NACABase as NACA, NACA5DigitReflex, NACA5DigitStandard, NACA4Digit
from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestFiveDigit(object):

    def test_24012(self):
        filename = "NACA/tests/data/airfoiltools/NACA24012.dat"
        a = AirfoilToolsDatFile(filename)
        # a.plot()
        n = NACA.factory("24012", s=a.s, cs=False, precision=6)
        # n.plot()
        # print(n.df)
        assert a.designation == n.n
        assert a.s == n.s
        # print(NACA.plot_series(n.xu / a.df.xu))
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

    def test_23012(self):

        a = AirfoilToolsDatFile.load("23012", 100, cs=False, ct=True)
        # a.plot()
        n = NACA.factory("23012", s=a.s, cs=False, ct=True, precision=6)
        # n.plot()
        # print(n.df)
        assert a.designation == n.n
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]
        assert all(n.df["yu"] == a.df["yu"])
        assert all(n.df["yl"] == a.df["yl"])


    def test_24012_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA24012_cs.dat"
        a = AirfoilToolsDatFile(filename)
        # a.plot()
        # print(a.df)
        n = NACA.factory("24012", s=a.s, cs=True, precision=6)
        # n.plot()
        # print(n.df)
        assert a.designation == n.n
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

    def test_24116_cs(self):
        # filename = "NACA/tests/data/airfoiltools/NACA24116_cs.dat"
        a = AirfoilToolsDatFile.load("24116", 100, cs=True, ct=True)
        # a.plot()
        # print(a.df)
        n = NACA.factory("24116", s=a.s, cs=True, precision=6)
        # n.plot()
        # print(n.df)
        # print(NACA.plot_series(n.xu / a.df.xu))
        assert a.designation == n.n
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

    def test_44016_cs(self):
        # filename = "NACA/tests/data/airfoiltools/NACA44016_cs.dat"
        a = AirfoilToolsDatFile.load("44016", 100, cs=True, ct=True)
        a.plot()
        print(a.df)
        n:[NACA5DigitStandard] = NACA.factory("44016", s=a.s, cs=True, ct=True, precision=6)
        n.plot()
        print(n.df)
        assert isinstance(n, NACA5DigitStandard)
        ratio = n.xu / a.df.xu
        print(ratio[1:10])
        print(ratio.idxmin(), ratio.min())

        fig, ax = plt.subplots()
        ax.plot(ratio)
        ax.set_title("NACA 44016 ratio")
        ax.aspect = "equal"
        # ax.set_xlabel("Index")
        # ax.set_ylabel("Ratio")
        # ax.grid()
        fig.show()

        assert n.thickness == 0.16
        assert n.design_cl == 0.6
        assert a.designation == n.n
        assert n.max_camber_position == 0.2
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

    def test_44016(self):
        # filename = "NACA/tests/data/airfoiltools/NACA44016_cs.dat"
        a = AirfoilToolsDatFile.load("44016", 100, cs=False, ct=True)
        a.plot()
        print(a.df)
        n:[NACA5DigitStandard] = NACA.factory("44016", s=a.s, cs=False, ct=True, precision=6)
        n.plot()
        print(n.df)
        assert isinstance(n, NACA5DigitStandard)
        ratio = n.xu / a.df.xu
        print(ratio[1:10])
        print(ratio.idxmin(), ratio.min())

        fig, ax = plt.subplots()
        ax.plot(ratio)
        ax.set_title("NACA 44016 ratio")
        ax.aspect = "equal"
        # ax.set_xlabel("Index")
        # ax.set_ylabel("Ratio")
        # ax.grid()
        fig.show()

        assert n.thickness == 0.16
        assert n.design_cl == 0.6
        assert a.designation == n.n
        assert n.max_camber_position == 0.2
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

    def test_24112_cs(self):

        a = AirfoilToolsDatFile.load("24112", 100, cs=True, ct=True)
        # a.plot()
        # print(a.df)
        n = NACA.factory("24112", s=a.s, cs=True,ct=True, precision=6)
        # n.plot()
        # print(n.df)
        assert a.s == n.s
        assert n.df["xu"][1] == a.df["xu"][1]
        assert n.df["xl"][1] == a.df["xl"][1]
        assert n.df["xu"][a.s//2] == a.df["xu"][a.s//2]
        assert n.df["xl"][a.s//2] == a.df["xl"][a.s//2]
        assert n.df["yu"][1] == a.df["yu"][1]
        assert n.df["yl"][1] == a.df["yl"][1]
        assert n.df["yu"][a.s//2] == a.df["yu"][a.s//2]
        assert n.df["yl"][a.s//2] == a.df["yl"][a.s//2]

