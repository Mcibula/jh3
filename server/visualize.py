import math

from roboticstoolbox import DHRobot, RevoluteDH


class JankoHrasko(DHRobot):
    def __init__(self, **kwargs):
        deg = math.pi / 180

        # L1 = RevoluteDH(
            # a=0,
            # alpha=0,
            # d=48
        # )

        # L2 = RevoluteDH(
            # a=0,
            # alpha=-90 * deg,
            # d=125,
            # qlim=[-180 * deg, 0]
        # )

        # L3 = RevoluteDH(
            # a=147,
            # alpha=0,
            # d=0,
            # qlim=[0, 90 * deg]
        # )

        # # L4 = RevoluteDH(
            # # a=182,
            # # alpha=0,
            # # d=0,
            # # qlim=[0, 147 * deg]
        # # )

        # L5 = RevoluteDH(
            # a=56,
            # alpha=90 * deg,
            # d=0,
            # qlim=[0, 125 * deg]
        # )

        # L6 = RevoluteDH(
            # a=58,
            # alpha=0,
            # d=0
        # )
        
        L1 = RevoluteDH(
            a=0,
            alpha=90 * deg,
            d=75
        )

        L2 = RevoluteDH(
            a=125,
            alpha=0,
            d=0,
            # qlim=[-180 * deg, 0]
        )

        L3 = RevoluteDH(
            a=118,
            alpha=0,
            d=0
            # qlim=[0, 90 * deg]
        )

        L4 = RevoluteDH(
            a=45,
            alpha=0,
            d=0
            # qlim=[0, 147 * deg]
        )


        super().__init__(
            links=[L1, L2, L3, L4],
            name='JankoHrasko',
            **kwargs
        )


if __name__ == '__main__':
    robot = JankoHrasko()
    print(robot)

    deg = math.pi / 180
    q = [0 * deg, 45 * deg, -45 * deg, -45 * deg]

    print(robot.islimit(q))
    robot.plot(
        q=q,
        backend='pyplot',
        block=False,
        jointaxes=True,
        eeframe=True,
        shadow=False
    )
