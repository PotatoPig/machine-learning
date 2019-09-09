import numpy as np
import math


def calculate_kernel_element(vec1, vec2, kernel='linear', d=2, sigma=1, beta=1, theta=1):
    kernel_calculator = KernelMethod(vec1, vec2, kernel=kernel, d=d, sigma=sigma, beta=beta, theta=theta)
    return kernel_calculator.kernel_method()


class KernelMethod(object):
    def __init__(self, vec1, vec2, kernel='linear', d=2, sigma=1, beta=1, theta=1):
        self.vec1 = vec1
        self.vec2 = vec2
        self.kernel = kernel
        self.d = d
        self.sigma = sigma
        self.beta = beta
        self.theta = theta

    def kernel_method(self):
        if self.kernel == 'linear':
            return linear_kernel(self.vec1, self.vec2)
        elif self.kernel == 'polynomial':
            return polynomial_kernel(self.vec1, self.vec2, self.d)
        elif self.kernel == 'gaussian':
            return gaussian_kernel(self.vec1, self.vec2, self.sigma)
        elif self.kernel == 'laplace':
            return laplace_kernel(self.vec1, self.vec2, self.sigma)
        elif self.kernel == 'sigmoid':
            return sigmoid_kernel(self.vec1, self.vec2, self.beta, self.theta)


# linear kernel: vector inner value
def linear_kernel(v1, v2):
    x1 = np.array(v1)
    x2 = np.array(v2)
    return np.inner(x1, x2)


# polynomial kernel
def polynomial_kernel(v1, v2, d):
    x1 = np.array(v1)
    x2 = np.array(v2)
    linear_res = np.inner(x1, x2)
    return linear_res**d


# gaussian kernel
def gaussian_kernel(v1, v2, sigma):
    x1 = np.array(v1)
    x2 = np.array(v2)
    dist = np.sqrt(np.sum(np.square(x1 - x2)))
    return math.exp(-(dist**2)/(2*(sigma**2)))


# laplace kernel
def laplace_kernel(v1, v2, sigma):
    x1 = np.array(v1)
    x2 = np.array(v2)
    dist = np.sqrt(np.sum(np.square(x1 - x2)))
    return math.exp(-(dist/sigma))


# sigmoid kernel
def sigmoid_kernel(v1, v2, beta, theta):
    x1 = np.array(v1)
    x2 = np.array(v2)
    scalar = np.inner(x1, x2)
    return math.tanh(beta*scalar+theta)


if __name__ == "__main__":
    v1 = [0.697, 0.460]
    v2 = [0.774, 0.376]
    result = calculate_kernel_element(v1, v2)
    print(result)