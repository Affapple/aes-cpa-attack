#! /usr/bin/env python3

import unittest
import numpy as np

from scipy.stats import pearsonr


def calculatePearsonCoefficient(x, y):
	from solutions import pearsonr_
	# copy-paste your function definition for calculatePearsonCoefficient()
	# instead of this stub
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
		self.assertEqual(calculatePearsonCoefficient(x, y), -0.21459959410742252)

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculatePearsonCoefficient)
	unittest.TextTestRunner(verbosity = 2).run(suite)
