import numpy as np

class Data_Const():
    '''Collection of statistical constants of the dataset
    '''
    def __init__(self, min_: float, max_: float, avg: float, sd: float) -> None:
        self.min = min_
        self.max = max_
        self.range = max_ - min_
        self.avg = avg
        self.sd = sd

    def scale(self, x):
        return (x - self.min) / self.range

    def invscale(self, x):
        return x * self.range + self.min

    def scale_fn(self):
        return lambda x: (x - self.min) / self.range

    def invscale_fn(self):
        return lambda x: x * self.range + self.min
    
    def scale_np(self):
        return np.vectorize(self.scale_fn())

    def invscale_np(self):
        return np.vectorize(self.invscale_fn())

    def normscale_np(self):
        return np.vectorize(lambda x: (x - self.avg) / self.sd)

valence = Data_Const(
    min_=4,
    max_=97,
    avg=51.431270,
    sd=23.480632
)
danceability = Data_Const(23, 96, 0, 0)

def main() -> None:
    return

if __name__ == "__main__":
    main()
