import os

from numpy import isclose, round_

from src.NACA import NACA
from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestFourDigitSym(object):
    def test_0012(self):
        filename = "NACA/tests/data/airfoiltools/NACA0012.dat"
        a = AirfoilToolsDatFile(filename)
        NACA0012 = NACA.factory("0012", cs=False)
        # print(NACA0012.df.to_string())
        assert  NACA0012.df.loc[0.0, "yu"] == 0.0
        assert  NACA0012.df.loc[0.0, "yl"] == 0.0
        assert NACA0012.df["yu"][1] == 0.017037073971
        assert NACA0012.df["yl"][1] == -0.017037073971
        assert round(NACA0012.df["yu"][50], 6) == 0.052940
        assert all(NACA0012.df["yu"] == NACA0012.df["yl"] * -1)
    def test_0012_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA0012.dat"
        a = AirfoilToolsDatFile(filename)
        NACA0012 = NACA.factory("0012", cs=True)
        assert  NACA0012.df.loc[0.0, "yu"] == 0.0
        assert  NACA0012.df.loc[0.0, "yl"] == 0.0
        assert NACA0012.df["yu"][1] == 0.002779436649037656
        assert NACA0012.df["yl"][1] == -0.002779436649037656
        assert round(NACA0012.df["yu"][50],6) == 0.052940
        assert all(NACA0012.df["yu"] == NACA0012.df["yl"] * -1)


    def test_2412(self):
        filename = "NACA/tests/data/airfoiltools/NACA2412.dat"
        a = AirfoilToolsDatFile(filename)

        assert a.s == 100
        NACA2412 = NACA.factory("2412", s=a.s, cs=False)
        NACA2412.plot()
        print(NACA2412.df)
        assert a.s == NACA2412.s
        assert round(NACA2412.df["yu"][1],6) == a.df["yu"][1]
        assert round(NACA2412.df["yl"][1],6) == a.df["yl"][1]

    def test_2412_cs(self):
        filename = "NACA/tests/data/airfoiltools/NACA2412_cs.dat"
        a = AirfoilToolsDatFile(filename)
        a.plot()
        print(a.df)
        NACA2412 = NACA.factory("2412", s=a.s,cs=True)
        NACA2412.plot()
        print(NACA2412.df)
        assert a.s == 100
        assert a.s == NACA2412.s
        assert round(NACA2412.df["xu"][1],6) == a.df["xu"][1]
        assert round(NACA2412.df["xl"][1],6) == a.df["xl"][1]
        assert round(NACA2412.df["xu"][a.s//2],6) == a.df["xu"][a.s//2]
        assert round(NACA2412.df["xl"][a.s//2],6) == a.df["xl"][a.s//2]
        assert round(NACA2412.df["yu"][1],6) == a.df["yu"][1]
        assert round(NACA2412.df["yl"][1],6) == a.df["yl"][1]
        assert round(NACA2412.df["yu"][a.s//2],6) == a.df["yu"][a.s//2]
        assert round(NACA2412.df["yl"][a.s//2],6) == a.df["yl"][a.s//2]


    # def test_available_dat_files(self):
    #     for root, dirs, files in os.walk("NACA/tests/data/airfoiltools/"):
    #         for file in files:
    #             if file.endswith(".dat"):
    #                 full_file_path = os.path.join(root, file)
    #                 print(full_file_path)
    #                 digits = os.path.splitext(file)[0][4:4+4]
    #                 a = AirfoilToolsDatFile(full_file_path)
    #                 assert a.filename == full_file_path
    #                 assert a.data["x"][a.turning_point] == 0
    #                 if os.path.splitext(file)[0].endswith("cs"):
    #                     # Cosine spacing
    #                     n = NACA.factory(n=digits, cs=True)
    #
    #                 else:
    #                     # Linear spacing
    #                     n = NACA.factory(n=digits, cs=False)
    #                     # print(n.df["x"].to_string())
    #                     # print(a.df["x"].to_string())
    #                     # print( (a.df["x"] == n.df["x"]).to_string())+
    #                     # print(type(a.df["x"]))
    #                     # print( (a.df["yl"].compare(n.df["yl"])))
    #                 # print( (a.df["xu"] - n.df["xu"]).to_string())
    #
    #                 isclose_x_u = isclose(a.df["xu"], round_(n.df["xu"], 6), rtol=0.001, atol=1e-16)
    #
    #                 print(isclose_x_u)
    #                 assert isclose_x_u.all()
    #                 isclose_top = isclose(a.df["yu"], n.df["yu"], rtol=0.001, atol=1e-16)
    #                 # print(isclose_top)
    #                 # print((a.df["yu"] - n.df["yu"]).to_string())
    #                 assert isclose_top.all()
    #                 isclose_bottom = isclose(a.df["yl"], n.df["yl"], rtol=0.001, atol=1e-16)
    #                 # print(isclose_bottom)
    #                 # print((a.df["yl"] - n.df["yl"]).to_string())
    #                 assert isclose_bottom.all()
    #                 if digits[:2] =="00":
    #                     isclose_top_bottom = isclose(a.df["yu"], a.df["yl"] * -1, rtol=0.001, atol=1e-16)
    #                     assert all(isclose_top_bottom)
