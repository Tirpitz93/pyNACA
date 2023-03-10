# Generated with SMOP  0.41
# matlab_src/naca.m

    ## pyNACA Airfoil Generator
# This function generates a set of points containing the coordinates of a
# pyNACA airfoil from the 4 Digit Series, 5 Digit Series and 6 Series given
# its number and, as additional features, the chordt, the number of points
# to be calculated, spacing type (between linear and cosine spacing),
# opened or closed trailing edge and the angle of attack of the airfoil.
# It also plots the airfoil for further comprovation if it is the required
# one by the user.

    # INPUT DATA
#   n --> pyNACA number (4, 5 or 6 digits)

    # OPTIONAL INPUT DATA
#   alpha --> Angle of attack (º) (0º default)
#   chord_length --> Chord of airfoil (m) (1 m default)
#   s --> Number of points of airfoil (1000 default)
#   cs --> Linear or cosine spacing (0 or 1 respectively) (1 default)
#   cte --> Opened or closed trailing edge (0 or 1 respectively) (0 default)

    # OUTPUT DATA
#   x_e --> Extrados x coordinate of airfoil vector (m)
#   x_i --> Intrados x coordinate of airfoil vector (m)
#   y_e --> Extrados y coordinate of airfoil vector (m)
#   y_i --> Intrados y coordinate of airfoil vector (m)


@function
def NACA(n=None,alpha=None,c=None,s=None,cs=None,cte=None,*args,**kwargs):
    varargin = NACA.varargin
    nargin = NACA.nargin

    #----------------------- COMPROVATION OF AIRFOIL SERIES -------------------
    if floor(n / 10000000.0) == 0:
        if floor(n / 1000000.0) == 0:
            if floor(n / 100000.0) == 0:
                if floor(n / 10000.0) == 0:
                    nc=4
# matlab_src/naca.m:32
                else:
                    nc=5
# matlab_src/naca.m:34
            else:
                nc=6
# matlab_src/naca.m:37
        else:
            nc=7
# matlab_src/naca.m:40
    else:
        nc=8
# matlab_src/naca.m:43

    #----------------------- PREVIOUS CALCULATIONS ----------------------------
    if logical_not(exist('chord_length','var')):
        c=1
# matlab_src/naca.m:47

    if logical_not(exist('s','var')):
        s=1000
# matlab_src/naca.m:50

    if exist('cs','var'):
        if cs == 0:
            x=linspace(0,1,s)
# matlab_src/naca.m:54
        else:
            beta=linspace(0,pi,s)
# matlab_src/naca.m:56
            x=(1 - cos(beta)) / 2
# matlab_src/naca.m:57
    else:
        beta=linspace(0,pi,s)
# matlab_src/naca.m:60
        x=(1 - cos(beta)) / 2
# matlab_src/naca.m:61

    if logical_not(exist('alpha','var')):
        alpha=0
# matlab_src/naca.m:64

    t=rem(n,100) / 100
# matlab_src/naca.m:66

    sym=0
# matlab_src/naca.m:67

    alpha=dot(alpha / 180,pi)
# matlab_src/naca.m:68

    #----------------------- VARIABLE PRELOCATION -----------------------------
    y_c=zeros(1,s)
# matlab_src/naca.m:70

    dyc_dx=zeros(1,s)
# matlab_src/naca.m:71

    #----------------------- THICKNESS CALCULATION ----------------------------
    if exist('cte','var'):
        if cte == 1:
            y_t=dot(t / 0.2,(dot(0.2969,sqrt(x)) - dot(0.126,x) - dot(0.3516,x ** 2) + dot(0.2843,x ** 3) - dot(0.1036,x ** 4)))
# matlab_src/naca.m:75
        else:
            y_t=dot(t / 0.2,(dot(0.2969,sqrt(x)) - dot(0.126,x) - dot(0.3516,x ** 2) + dot(0.2843,x ** 3) - dot(0.1015,x ** 4)))
# matlab_src/naca.m:77
    else:
        y_t=dot(t / 0.2,(dot(0.2969,sqrt(x)) - dot(0.126,x) - dot(0.3516,x ** 2) + dot(0.2843,x ** 3) - dot(0.1015,x ** 4)))
# matlab_src/naca.m:80

    if nc == 4:
        #----------------------- MEAN CAMBER 4 DIGIT SERIES CALCULATION -----------
    #----------------------- CONSTANTS ------------------------------------
        m=floor(n / 1000) / 100
# matlab_src/naca.m:85
        p=rem(floor(n / 100),10) / 10
# matlab_src/naca.m:86
        if m == 0:
            if p == 0:
                sym=1
# matlab_src/naca.m:89
            else:
                sym=2
# matlab_src/naca.m:91
        #----------------------- CAMBER ---------------------------------------
        for i in arange(1,s,1).reshape(-1):
            if x(i) < p:
                y_c[i]=dot(dot(m,x(i)) / p ** 2,(dot(2,p) - x(i))) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:97
                dyc_dx[i]=dot(dot(2,m) / p ** 2,(p - x(i))) / cos(alpha) - tan(alpha)
# matlab_src/naca.m:98
            else:
                y_c[i]=dot(dot(m,(1 - x(i))) / (1 - p) ** 2,(1 + x(i) - dot(2,p))) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:100
                dyc_dx[i]=dot(dot(2,m) / (1 - p) ** 2,(p - x(i))) / cos(alpha) - tan(alpha)
# matlab_src/naca.m:101
    else:
        if nc == 5:
            #----------------------- MEAN CAMBER 5 DIGIT SERIES CALCULATION -----------
    #----------------------- CONSTANTS ------------------------------------
            p=rem(floor(n / 1000),10) / 20
# matlab_src/naca.m:107
            rn=rem(floor(n / 100),10)
# matlab_src/naca.m:108
            if rn == 0:
                #----------------------- STANDARD CAMBER ------------------------------
        #----------------------- CONSTANTS --------------------------------
                r=dot(3.33333333333212,p ** 3) + dot(0.700000000000909,p ** 2) + dot(1.19666666666638,p) - 0.00399999999996247
# matlab_src/naca.m:112
                k1=dot(1514933.33335235,p ** 4) - dot(1087744.00001147,p ** 3) + dot(286455.266669048,p ** 2) - dot(32968.4700001967,p) + 1420.18500000524
# matlab_src/naca.m:113
                #----------------------- CAMBER -----------------------------------
                for i in arange(1,s,1).reshape(-1):
                    if x(i) < r:
                        y_c[i]=dot(k1 / 6,(x(i) ** 3 - dot(dot(3,r),x(i) ** 2) + dot(dot(r ** 2,(3 - r)),x(i)))) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:117
                        dyc_dx[i]=dot(k1 / 6,(dot(3,x(i) ** 2) - dot(dot(6,r),x(i)) + dot(r ** 2,(3 - r)))) / cos(alpha) - tan(alpha)
# matlab_src/naca.m:118
                    else:
                        y_c[i]=dot(dot(k1,r ** 3) / 6,(1 - x(i))) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:120
                        dyc_dx[i]=dot(- k1,r ** 3) / (dot(6,cos(alpha))) - tan(alpha)
# matlab_src/naca.m:121
            else:
                if rn == 1:
                    #----------------------- REFLEXED CAMBER ------------------------------
        #----------------------- CONSTANTS --------------------------------
                    r=dot(10.6666666666861,p ** 3) - dot(2.00000000001601,p ** 2) + dot(1.73333333333684,p) - 0.0340000000002413
# matlab_src/naca.m:127
                    k1=dot(- 27973.3333333385,p ** 3) + dot(17972.8000000027,p ** 2) - dot(3888.40666666711,p) + 289.076000000022
# matlab_src/naca.m:128
                    k2_k1=dot(85.5279999999984,p ** 3) - dot(34.9828000000004,p ** 2) + dot(4.80324000000028,p) - 0.21526000000003
# matlab_src/naca.m:129
                    #----------------------- CAMBER -----------------------------------
                    for i in arange(1,s,1).reshape(-1):
                        if x(i) < r:
                            y_c[i]=dot(k1 / 6,((x(i) - r) ** 3 - dot(dot(k2_k1,(1 - r) ** 3),x(i)) - dot(r ** 3,x(i)) + r ** 3)) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:133
                            dyc_dx[i]=dot(k1 / 6,(dot(3,(x(i) - r) ** 2) - dot(k2_k1,(1 - r) ** 3) - r ** 3)) / cos(alpha) - tan(alpha)
# matlab_src/naca.m:134
                        else:
                            y_c[i]=dot(k1 / 6,(dot(k2_k1,(x(i) - r) ** 3) - dot(dot(k2_k1,(1 - r) ** 3),x(i)) - dot(r ** 3,x(i)) + r ** 3)) + dot((1 / 2 - x(i)),sin(alpha))
# matlab_src/naca.m:136
                            dyc_dx[i]=dot(k1 / 6,(dot(dot(3,k2_k1),(x(i) - r) ** 2) - dot(k2_k1,(1 - r) ** 3) - r ** 3)) / cos(alpha) - tan(alpha)
# matlab_src/naca.m:137
                else:
                    error('Incorrect pyNACA number. Third digit must be either 0 or 1')
        else:
            if nc == 6:
                #----------------------- MEAN CAMBER 6 DIGIT SERIES CALCULATION -----------
    #----------------------- CONSTANTS ------------------------------------
                ser=floor(n / 100000)
# matlab_src/naca.m:146
                a=rem(floor(n / 10000),10) / 10
# matlab_src/naca.m:147
                c_li=rem(floor(n / 100),10) / 10
# matlab_src/naca.m:148
                g=dot(- 1 / (1 - a),(dot(a ** 2,(dot(1 / 2,log(a)) - 1 / 4)) + 1 / 4))
# matlab_src/naca.m:149
                h=dot(1 / (1 - a),(dot(dot(1 / 2,(1 - a) ** 2),log(1 - a)) - dot(1 / 4,(1 - a) ** 2))) + g
# matlab_src/naca.m:150
                if ser == 6:
                    #----------------------- CAMBER ---------------------------------------
                    y_c=dot(c_li / (dot(dot(2,pi),(a + 1))),(dot(1 / (1 - a),(dot(dot(1 / 2,(a - x) ** 2.0),log(abs(a - x))) - dot(dot(1 / 2,(1 - x) ** 2.0),log(1 - x)) + dot(1 / 4,(1 - x) ** 2) - dot(1 / 4,(a - x) ** 2))) - multiply(x,log(x)) + g - dot(h,x))) + dot((1 / 2 - x),sin(alpha))
# matlab_src/naca.m:153
                    dyc_dx=- (dot(c_li,(h + log(x) - (x / 2 - a / 2 + (multiply(log(1 - x),(dot(2,x) - 2))) / 2 + (multiply(log(abs(a - x)),(dot(2,a) - dot(2,x)))) / 2 + (multiply(sign(a - x),(a - x) ** 2)) / (dot(2,abs(a - x)))) / (a - 1) + 1))) / (dot(dot(dot(2,pi),(a + 1)),cos(alpha))) - tan(alpha)
# matlab_src/naca.m:154
                else:
                    error('pyNACA 6 Series must begin with 6')
            else:
                error(concat(['pyNACA ',num2str(nc),' Series has not been yet implemented']))

    #----------------------- FINAL CALCULATIONS -------------------------------
    theta=atan(dyc_dx)
# matlab_src/naca.m:162

    x=1 / 2 - dot((1 / 2 - x),cos(alpha))
# matlab_src/naca.m:163

    #----------------------- COORDINATE ASSIGNATION ---------------------------
    x_e=dot((x - multiply(y_t,sin(theta))),c)
# matlab_src/naca.m:165

    x_i=dot((x + multiply(y_t,sin(theta))),c)
# matlab_src/naca.m:166

    y_e=dot((y_c + multiply(y_t,cos(theta))),c)
# matlab_src/naca.m:167

    y_i=dot((y_c - multiply(y_t,cos(theta))),c)
# matlab_src/naca.m:168

    #----------------------- pyNACA PLOT ----------------------------------------
    ep=plot(x_e,y_e,'b')
# matlab_src/naca.m:170

    hold

    plot(x_i,y_i,'b')

    mclp=plot(x,y_c,'r')
# matlab_src/naca.m:173

    clp=plot(concat([dot(c / 2,(1 - cos(alpha))),dot(c / 2,(1 + cos(alpha)))]),concat([dot(c / 2,sin(alpha)),dot(- c / 2,sin(alpha))]),'g')
# matlab_src/naca.m:174

    grid

    axis('equal')

    if sym == 1:
        title(concat(['pyNACA 00',num2str(n),' Airfoil Plot (',num2str(dot(alpha / pi,180)),'º)']))
        legend(concat([ep,mclp,clp]),concat(['pyNACA 00',num2str(n),' Airfoil']),'Mean camber line','Chord line')
    else:
        if sym == 2:
            title(concat(['pyNACA 0',num2str(n),' Airfoil Plot (',num2str(dot(alpha / pi,180)),'º)']))
            legend(concat([ep,mclp,clp]),concat(['pyNACA 0',num2str(n),' Airfoil']),'Mean camber line','Chord line')
        else:
            title(concat(['pyNACA ',num2str(n),' Airfoil Plot (',num2str(dot(alpha / pi,180)),'º)']))
            legend(concat([ep,mclp,clp]),concat(['pyNACA ',num2str(n),' Airfoil']),'Mean camber line','Chord line')

    xlabel('X (m)')

    ylabel('Y (m)')

    return x_e,x_i,y_e,y_i

if __name__ == '__main__':
    print(naca("0012", 1, 1))
