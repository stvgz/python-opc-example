"""
A rule base prediction?

"""
import pandas as pd


class Detector():

    def __init__(self, spec = 100):
        self.spec = spec
        self.comparator = 'GE'

    def convert_to_float(self,value):

        try:
            value = float(value)
        except ValueError:
            raise ValueError('Input must be able to convert to float')

        return value

    def detect(self,value):

        if self.comparator == 'GE':
            
            value = self.convert_to_float(value)

            return value >= self.spec



if __name__ == '__main__':
    d = Detector(spec = 100)

    print(d.detect(101))

    print(d.detect(99))
