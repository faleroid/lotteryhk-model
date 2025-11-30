class BallUtils:
    COLOR_MAP = {n: 'ball-red' for n in [1, 2, 7, 8, 12, 13, 18, 19, 23, 24, 29, 30, 34, 35, 40, 45, 46]}
    COLOR_MAP.update({n: 'ball-blue' for n in [3, 4, 9, 10, 14, 15, 20, 25, 26, 31, 36, 37, 41, 42, 47, 48]})

    @staticmethod
    def get_color(number):
        return BallUtils.COLOR_MAP.get(number, 'ball-green')

    @staticmethod
    def format_balls_data(balls):
        if not balls: return []
        return [{'num': n, 'color': BallUtils.COLOR_MAP.get(n, 'ball-green')} for n in balls]