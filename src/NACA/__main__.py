from _ctypes import Array

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from . import NACABase, NACA4Digit, NACA5DigitStandard, NACA5DigitReflex

if __name__ == '__main__':
    pass

    foils = [
        NACABase.factory("0005", cs=True,ct=True),
        NACABase.factory("0012", cs=True,ct=True),
        NACA4Digit("2412", cs=True),
        NACA4Digit("3212", cs=True),
        NACA5DigitStandard("24006", cs=True),
        NACA5DigitStandard("24106", cs=True),
        NACA5DigitReflex("24112", cs=True),

    ]
    fig: Figure
    axs: Array[Axes]
    fig, axs = plt.subplots(nrows=len(foils), sharex=True)
    range_y = [pd.concat([f.yl for f in foils]).min()*1.2,pd.concat([f.yu for f in foils]).max()*1.2]
    fig.set_size_inches(6,12)
    fig.set_dpi(300)
    ax: Axes
    for (ax,foil) in zip(axs, foils):
        ax.plot(foil.df["xu"], foil.df["yu"], label=str(foil.n) + " top", linewidth=1)
        ax.plot(foil.df["xl"], foil.df["yl"], label=str(foil.n) + " bottom", linewidth=1)
        ax.plot(foil.df["xc"], foil.df["yc"], label=str(foil.n) + " camber", linewidth=0.5)
        # ax.legend(["Top Surface", "Bottom Surface", "Camber Line"], bbox_to_anchor=(1,1), loc="upper left")
        ax.set_title(f"NACA {foil.n} Airfoil")
        ax.set_aspect("equal")
        ax.set_ylim(range_y)
    plt.tight_layout(pad=1.5)
    plt.show()