import random


class HelperNumerical:

    @staticmethod
    def get_weighted_random(minimum, maximum):
        """
        Get weighted random number
        :param minimum: Minimum value
        :param maximum: Maximum value
        :return: Weighted random number
        """
        weight = random.random()
        return int(weight * (maximum - minimum) + minimum)
