def fak_1(t, params):
    return params[0] * t + params[1]


def fak_2(t, params):
    return params[1] * params[0] * t ** 2 + params[1] * t + params[2]


def fak_3(t, params):
    return params[2]


def fak_4(t, params):
    return -params[0] * t + params[1]


def fak_6(t, params):
    return params[0] * t + params[1]


def fak_7(t, params):
    return params[0] * t + params[2]


def pend(u, t, faks, f):
    seq = list(range(317))
    fxu = lambda x: fx(u[x], f[seq.pop(0)])

    dudt = [
        # 0
        (
                (1 / u[0]) *
                fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_4(t, faks[3])) -
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(14) * fxu(15) * fxu(16) *
                fxu(17) * fxu(19) * fxu(20) * fak_3(t, faks[2])
        ),

        # 1
        (
                (1 / u[1]) *
                fxu(2) * fxu(3) * fak_1(t, faks[0]) -
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(13) * fxu(18)
        ),

        # 2
        (
                (1 / u[2]) *
                fxu(0) * fxu(1) * fxu(3) * fxu(4) * fak_1(t, faks[0]) -
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(16) * fxu(19) * fak_3(t, faks[2])
        ),

        # 3
        (
                (1 / u[3]) *
                fxu(0) * fxu(2) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1])) -
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(14) * fxu(15) * fxu(17) *
                fxu(18) * fxu(22) * fak_3(t, faks[2])
        ),

        # 4
        (
                (1 / u[4]) *
                fxu(3) * fxu(5) -
                fxu(1) * fxu(2) * fxu(6) * fxu(7) * fxu(11) * fxu(12) * fxu(13) * fxu(14) * fxu(15)
        ),

        # 5
        (
                (1 / u[5]) *
                fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(11) * fxu(12) * fxu(13) * fxu(14) *
                fxu(15) * fxu(16) * fxu(17) * fxu(18) * fxu(19) * fxu(20) * fxu(21) * fxu(22) * fak_3(t, faks[2]) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1]))
        ),

        # 6
        (
                (1 / u[6]) *
                fxu(5) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(19) * fxu(21) *
                fak_3(t, faks[2]) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * (fak_1(t, faks[0]) + fak_2(t, faks[1]))
        ),

        # 7
        (
                (1 / u[7]) *
                fxu(5) * fxu(6) * fxu(8) * fxu(9) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(22) * fak_3(t,
                                                                                                            faks[2]) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * fak_1(t, faks[0])
        ),

        # 8
        (
                (1 / u[8]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(9) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(22) * fak_3(t,
                                                                                                            faks[2]) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1]))
        ),

        # 9
        (
                (1 / u[9]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(22) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1]))
        ),

        # 10
        (
                (1 / u[10]) *
                fxu(5) * fxu(12) * fxu(13) * fxu(16) * fxu(17) * fxu(20) * fxu(21) * fxu(22) * fak_3(t, faks[2]) -
                fxu(2) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1]) + fak_6(t, faks[4]) + fak_7(t, faks[5]))
        ),

        # 11
        (
                (1 / u[11]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(12) * fxu(13) * fxu(14) *
                fxu(15) * fxu(16) * fxu(17) * fxu(18) * fxu(19) * fxu(22) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 12
        (
                (1 / u[2]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(11) * fxu(13) * fxu(15) * fxu(22) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fak_1(t, faks[0])
        ),

        # 13
        (
                (1 / u[3]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(17) * fxu(18) *
                fxu(19) * fxu(20) * fxu(21) * fxu(22) -
                fxu(2) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 14
        (
                (1 / u[4]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(12) * fxu(16) * fxu(17) * fxu(18) * fxu(22) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 15
        (
                (1 / u[1]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(12) * fxu(13) * fxu(14) * fxu(17) * fxu(18) *
                fxu(22) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_2(t, faks[1]) + fak_3(t, faks[2]))
        ),

        # 16
        (
                (1 / u[16]) *
                fxu(6) * fxu(8) * fxu(10) * fxu(12) * fxu(19) * fxu(20) * fxu(21) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) *
                (fak_1(t, faks[0]) + fak_2(t, faks[1]) + fak_3(t, faks[2]) + fak_6(t, faks[4]))
        ),

        # 17
        (
                (1 / u[17]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(12) * fxu(14) * fxu(15) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 18
        (
                (1 / u[18]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(17) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 19
        (
                (1 / u[19]) *
                fxu(5) * fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(10) * fxu(11) * fxu(12) * fxu(14) * fxu(15) * fxu(17) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * (fak_1(t, faks[0]) + fak_3(t, faks[2]))
        ),

        # 20
        (
                (1 / u[20]) *
                fxu(5) * fxu(7) * fxu(8) * fxu(11) * fxu(16) * fxu(19) -
                fxu(2) * fxu(3) * (fak_1(t, faks[0]) + fak_2(t, faks[1]) + fak_3(t, faks[2]))
        ),

        # 21
        (
                (1 / u[21]) *
                fxu(6) * fxu(7) * fxu(8) * fxu(9) * fxu(11) * fxu(14) * fxu(15) * fxu(17) -
                fak_1(t, faks[0])
        ),

        # 22
        (
                (1 / u[22]) *
                fxu(6) * fxu(7) * fxu(8) * fxu(11) * fxu(13) * fxu(16) * fxu(17) * fxu(20) -
                fxu(0) * fxu(1) * fxu(2) * fxu(3) * fxu(4) * fak_1(t, faks[0])
        )
    ]
    return dudt


def fx(x, params):
    return (params[0] * x) ** 3 + (params[1] * x) ** 2 + (params[2] * x) + params[3]
