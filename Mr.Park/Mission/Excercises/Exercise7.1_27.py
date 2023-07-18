from fraction import Fraction

def main():
    numer = int(input("Enter numerator: "))
    denom = int(input("Enter denominator: "))
    # denom = 0
    # while denom == 0:
    #     denom = int(input("Enter denominator: "))

    frac = Fraction(numer, denom)
    try:
        numer_reduced, denom_reduced = frac.reduce()

        if denom_reduced == 1:
            print('Reduction: {}'.format(numer_reduced))    

        else:
            print('Reduction: {}/{}'.format(numer_reduced, denom_reduced))
    except Exception as exp:
        print(exp)
main()