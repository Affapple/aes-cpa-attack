#! /usr/bin/env python3

import unittest
import numpy as np

from scipy.stats import pearsonr


def calculatePearsonCoefficient(x, y):
	N = x.shape[0]
	x = x.astype(np.float64)
	y = y.astype(np.float64)

	numerator = N * (x.T @ y) - x.sum(axis=0).reshape(-1, 1) * y.sum(axis=0).reshape(1, -1)  # (K, T)
	std_a = np.sqrt(N * (x**2).sum(axis=0) - x.sum(axis=0)**2).reshape(-1, 1)  # (K, 1)
	std_b = np.sqrt(N * (y**2).sum(axis=0) - y.sum(axis=0)**2).reshape(1, -1)  # (1, T)
	denom = std_a * std_b  # (K, T)

	with np.errstate(invalid='ignore', divide='ignore'):
		return np.where(denom != 0, numerator / denom, 0.0).item()

	return pearsonr_(x,y)[0]

class TestCalculatePearsonCoefficient(unittest.TestCase):

	def test_pearson_equal(self):
		x = np.arange(8)
		y = x
		self.assertEqual(calculatePearsonCoefficient(x, y), 1.0)

	def test_pearson_opposite(self):
		x = np.arange(8)
		y = -1*x
		self.assertEqual(calculatePearsonCoefficient(x, y), -1.0)

	def test_pearson_uncorrelated(self):
		x = np.arange(8)
		y = np.array([186, 218, 15, 225, 1, 226, 118, 102])
		self.assertAlmostEqual(calculatePearsonCoefficient(x, y), -0.21459959410742252, places=16)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculatePearsonCoefficient)
	unittest.TextTestRunner(verbosity = 2).run(suite)
