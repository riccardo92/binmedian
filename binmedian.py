import math
import itertools
import numpy as np
from time import time

def swap(x, a, b):
	""" Swap elements with indices a and b in x.

	Args:
		x (numpy.ndarray or list): the data
		a (int): a valid index of x
		b (int): a valid index of x

	Returns:
		void
	"""
	x[a], x[b] = x[b], x[a]

def binmedian(x, mean=None, std=None):
	""" This is a Python port of the binmedian 
	algorithm originally written in C as can be found on 
	http://www.stat.cmu.edu/~ryantibs/median/binmedian.c

	Args:
		x (numpy.ndarray or list): the data
		mean (float): the mean of x (optional)
		std (float): the stddev of x (optional)

	Returns:
		The median of x if length of x is odd else 0.
	"""

	n = len(x)

	# Compute mean and stddev if not given
	if mean is None:
		mean = np.mean(x)
	if std is None:
		std = np.std(x)

	bottom_count = 0
	bin_counts = [0] * 1001
	scale_factor = 1000 / (2 * std)
	left_end = mean - std
	right_end = mean + std
	bin_index = 0

	for i, element in enumerate(x):
		if element < left_end:
			bottom_count += 1
		elif element < right_end:
			bin_index = int((element - left_end) * scale_factor)
			bin_counts[bin_index] += 1

	# For odd n
	if n % 2 != 0:

		k = int((n + 1) / 2)
		r = 0
		count = 0
		med_bin = 0
		old_scale_factor = 0
		old_left_end = 0
		old_bin_index = 0
		temp = 0.0

		while True:
			count = bottom_count
			for i in range(1001):
				count += bin_counts[i]
				if count >= k:
					med_bin = i
					k -= count - bin_counts[i]
					break
			
			bottom_count = 0
			bin_counts = [0]*1001

			old_scale_factor = scale_factor
			old_left_end = left_end
			scale_factor = 1000 * old_scale_factor
			left_end = med_bin / old_scale_factor + old_left_end
			right_end = (med_bin + 1) / old_scale_factor + old_left_end

			# Determine which points map to med_bin, and put
      # them in spots r,...n-1
			i = r
			r = n
			
			while i < r:

				old_bin = int((x[i] - old_left_end) * old_scale_factor)

				if old_bin == med_bin:

					r -= 1
					swap(x, i, r)

					if x[i] < left_end:
						bottom_count -= 1
					elif x[i] < right_end:
						bin_index = int((x[i] - left_end) * scale_factor)
						bin_counts[bin_index] += 1
				
				else:
					i += 1

			# Stop if all points in medbin are the same
			same_points = True
			if len(np.unique(x[r+1:])) == 1:
				return x[r]

			# Stop if there's <= 20 points left
			if n - r <= 20:
				print('breaking')
				break
		
		a = 0.0
		j = 0
		for i in range(r + 1, n):
			a = x[i]
			for j in reversed(range(r, i - 1)):
				if x[j] > a:
					break
				x[j + 1] = x[j]
			x[j + 1] = a

		return x[r - 1 + k]

	# For even n (not implemented yet)
	else:
		return 0

if __name__ == '__main__':
	# Example
	arr = list(np.random.randint(3000, size=5001))
	s = time()
	print('binmedian', binmedian(arr))
	print('time in sec {0:.5f}'.format(time() - s))
	s = time()
	print('actual median', np.median(arr))
	print('time in sec {0:.5f}'.format(time() - s))