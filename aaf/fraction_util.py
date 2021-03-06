from fractions import Fraction, _RATIONAL_FORMAT
from decimal import Decimal
import numbers
Rational = numbers.Rational



class AAFFraction(Fraction):
    """
    Subclass of fractions.Fraction from the standard library. Behaves exactly the same, except
    doesn't round to the Greatest Common Divisor at the end.
    """
    
    def __new__(cls, numerator=0, denominator=None):
        
        self = super(AAFFraction, cls).__new__(cls)

        if denominator is None:
            if isinstance(numerator, Rational):
                self._numerator = numerator.numerator
                self._denominator = numerator.denominator
                return self

            elif isinstance(numerator, float):
                # Exact conversion from float
                value = Fraction.from_float(numerator)
                self._numerator = value._numerator
                self._denominator = value._denominator
                return self

            elif isinstance(numerator, Decimal):
                value = Fraction.from_decimal(numerator)
                self._numerator = value._numerator
                self._denominator = value._denominator
                return self

            elif isinstance(numerator, str):
                # Handle construction from strings.
                m = _RATIONAL_FORMAT.match(numerator)
                if m is None:
                    raise ValueError('Invalid literal for Fraction: %r' %
                                     numerator)
                numerator = int(m.group('num') or '0')
                denom = m.group('denom')
                if denom:
                    denominator = int(denom)
                else:
                    denominator = 1
                    decimal = m.group('decimal')
                    if decimal:
                        scale = 10**len(decimal)
                        numerator = numerator * scale + int(decimal)
                        denominator *= scale
                    exp = m.group('exp')
                    if exp:
                        exp = int(exp)
                        if exp >= 0:
                            numerator *= 10**exp
                        else:
                            denominator *= 10**-exp
                if m.group('sign') == '-':
                    numerator = -numerator

            else:
                raise TypeError("argument should be a string "
                                "or a Rational instance")

        elif (isinstance(numerator, Rational) and
            isinstance(denominator, Rational)):
            numerator, denominator = (
                numerator.numerator * denominator.denominator,
                denominator.numerator * numerator.denominator
                )
        else:
            raise TypeError("both arguments should be "
                            "Rational instances")

        if denominator == 0:
            raise ZeroDivisionError('Fraction(%s, 0)' % numerator)
        # don't find the gcd
        #g = gcd(numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self