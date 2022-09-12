import os

from numpy import isclose, round_

from src.NACA import four_digit
from src.NACA.airfoiltools_dat import AirfoilToolsDatFile


class TestFourDigitSym(object):
    def test_0012(self):
        NACA0012 = four_digit("0012", cs=False)
        assert  NACA0012.loc[0.0, "yu"] == 0.0
        assert  NACA0012.loc[0.0, "yl"] == 0.0
        assert NACA0012["yu"][1] == 0.017037073971
        assert NACA0012["yl"][1] == -0.017037073971
        assert all(NACA0012["yu"] == NACA0012["yl"] * -1)
    def test_0012_cs(self):
        NACA0012 = four_digit("0012", cs=True)
        assert  NACA0012.loc[0.0, "yu"] == 0.0
        assert  NACA0012.loc[0.0, "yl"] == 0.0
        assert NACA0012["yu"][1] == 0.002779436649037656
        assert NACA0012["yl"][1] == -0.002779436649037656
        assert all(NACA0012["yu"] == NACA0012["yl"] * -1)

    def test_available_dat_files(self):
        for root, dirs, files in os.walk("NACA/tests/data/airfoiltools/"):
            for file in files:
                if file.endswith(".dat"):
                    full_file_path = os.path.join(root, file)
                    print(full_file_path)
                    digits = os.path.splitext(file)[0][4:4+4]
                    a = AirfoilToolsDatFile(full_file_path)
                    assert a.filename == full_file_path
                    assert a.data["x"][a.turning_point] == 0
                    if os.path.splitext(file)[0].endswith("cs"):
                        # Cosine spacing
                        n = four_digit(n=digits, cs=True)

                    else:
                        # Linear spacing
                        n = four_digit(n=digits, cs=False)
                        # print(n["x"].to_string())
                        # print(a.df["x"].to_string())
                        # print( (a.df["x"] == n["x"]).to_string())+
                        # print(type(a.df["x"]))
                        # print( (a.df["yl"].compare(n["yl"])))
                    print( (a.df["xu"] - n["xu"]).to_string())

                    isclose_x_u = isclose(a.df["xu"], round_(n["xu"], 6), rtol=0.001, atol=1e-16)
                    print(isclose_x_u)
                    assert isclose_x_u.all()
                    isclose_top = isclose(a.df["yu"], n["yu"], rtol=0.001, atol=1e-16)
                    print(isclose_top)
                    print((a.df["yu"] - n["yu"]).to_string())
                    assert isclose_top.all()
                    isclose_bottom = isclose(a.df["yl"], n["yl"], rtol=0.001, atol=1e-16)
                    print(isclose_bottom)
                    print((a.df["yl"] - n["yl"]).to_string())
                    assert isclose_bottom.all()
                    if digits[:2] =="00":
                        isclose_top_bottom = isclose(a.df["yu"], a.df["yl"] * -1, rtol=0.001, atol=1e-16)
                        all(isclose_top_bottom)
