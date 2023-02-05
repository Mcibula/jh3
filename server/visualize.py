import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
import roboticstoolbox as rbt


class JankoHrasko(DHRobot):
    def __init__(self, **kwargs):
        deg = np.pi / 180

        L1 = RevoluteDH(
            a=0,
            alpha=0,
            d=48
        )

        L2 = RevoluteDH(
            a=0,
            alpha=-90 * deg,
            d=19,
            qlim=[-180 * deg, 0]
        )

        L3 = RevoluteDH(
            a=147,
            alpha=0,
            d=0,
            qlim=[0, 90 * deg]
        )

        L4 = RevoluteDH(
            a=182,
            alpha=0,
            d=0,
            qlim=[0, 147 * deg]
        )

        L5 = RevoluteDH(
            a=56,
            alpha=90 * deg,
            d=0,
            qlim=[0, 125 * deg]
        )

        L6 = RevoluteDH(
            a=58,
            alpha=0,
            d=0
        )

        super().__init__(
            links=[L1, L2, L3, L4, L5, L6],
            name='JankoHrasko',
            **kwargs
        )


if __name__ == '__main__':
    robot = JankoHrasko()
    print(robot)

    deg = np.pi / 180
    q = np.array([0 * deg, 0 * deg, 0 * deg, 45 * deg, 45 * deg, 0 * deg])

    print(robot.islimit(q))
    robot.plot(
        q=q,
        backend='pyplot',
        block=False,
        jointaxes=True,
        eeframe=True,
        shadow=False
    )
