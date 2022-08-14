class Utils:
    @staticmethod
    def roundUp(n, m):
        return (n - 1) + m - (n - 1) % m
