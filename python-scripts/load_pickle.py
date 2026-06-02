import numpy
import pickle


def load(filename: str) -> tuple[list[int], numpy.ndarray]:
    fd = open(filename, "rb")
    T, M = pickle.load(fd)
    fd.close()
    return T, numpy.array(M)


if __name__ == "__main__":
    T, M = load("./testsca.pickle")
    print(T)
    print(M)
