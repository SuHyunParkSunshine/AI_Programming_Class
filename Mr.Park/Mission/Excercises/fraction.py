class Fraction:
    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator
    
    @staticmethod
    def GCD(m, n): # Greatest Common Divisor
        while n != 0:
            t = n
            n = m % n
            m = t

        return m
    
    def reduce(self):
        if self._denominator == 0:
            raise ZeroDivisionError("Denomindator = 0")
        gcd = self.GCD(self._numerator, self._denominator)
        return self._numerator // gcd, self._denominator // gcd