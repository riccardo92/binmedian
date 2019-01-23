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
	bin_counts = np.zeros(1001, np.int32)
	scale_factor = 1000 / (2 * std)
	left_end = mean - std
	right_end = mean + std
	left_end_right = left_end
	right_end_right = left_end
	bin_index = 0

	for i, element in enumerate(x):
		if element < left_end:
			bottom_count += 1
		elif element < right_end:
			bin_index = int((element - left_end) * scale_factor)
			bin_counts[bin_index] += 1

	# For odd n
	if n & 1:
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
			for i in range(1002):
				count += bin_counts[i]
				if count >= k:
					med_bin = i
					k = k - (count - bin_counts[i])
					break
			
			bottom_count = 0
			bin_counts = np.zeros(1001, np.int32)

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
						bottom_count += 1
					elif x[i] < right_end:
						bin_index = int((x[i] - left_end) * scale_factor)
						bin_counts[bin_index] += 1
				
				else:
					i += 1

			# Stop if all points in medbin are the same
			if len(np.unique(x[r:])) == 1:
				return x[r]

			# Stop if there's <= 20 points left
			if n - r <= 20:
				break
		
		a = 0.0
		i = r + 1
		for i in range(r + 1, n):			
			a = x[i]
			j = i - 1
			while j >= r:
				if x[j] > a:
					break
				x[j + 1] = x[j]
				j -= 1
			x[j + 1] = a
			i += 1

		return x[r - 2 + k]

	# For even n
	else:
		k = int(n / 2)
		k_right = int(n / 2) + 1
		r = 0
		count = 0
		med_bin = 0
		med_bin_right = 0
		old_scale_factor = 0
		old_scale_factor_right = 0
		old_left_end = 0
		old_left_end_right = 0
		old_bin_index = 0
		old_bin_index_right = 0

		while True:
			count = bottom_count
			for i in range(1002):
				count += bin_counts[i]
				break_left = False
				if count >= k and not break_left:
					med_bin = i
					k = k - (count - bin_counts[i])
					break_left = True
				if count >= k_right:
					med_bin_right = i
					k_right -= count - bin_counts[i]
					break
			
			bottom_count = 0
			bottom_count_right = 0
			bin_counts = np.zeros(1001, np.int32)

			old_scale_factor = scale_factor
			old_scale_factor_right = scale_factor
			old_left_end = left_end
			old_left_end_right = left_end_right
			scale_factor = 1000 * old_scale_factor
			scale_factor_right = 1000 * old_scale_factor_right
			left_end = med_bin / old_scale_factor + old_left_end
			left_end_right = med_bin_right / old_scale_factor_right + old_left_end_right
			right_end = (med_bin + 1) / old_scale_factor + old_left_end
			right_end_right = (med_bin_right + 1) / old_scale_factor_right + old_left_end_right
			# Determine which points map to med_bin, and put
      # them in spots r,...n-1
			i = r
			r = n
			i_right = r
			r_right = n
			
			while i < r:

				old_bin = int((x[i] - old_left_end) * old_scale_factor)

				if old_bin == med_bin:

					r -= 1
					swap(x, i, r)

					if x[i] < left_end:
						bottom_count += 1
					elif x[i] < right_end:
						bin_index = int((x[i] - left_end) * scale_factor)
						bin_counts[bin_index] += 1

				elif old_bin == med_bin_right:

					r -= 1

					if x[i] < left_end_right:
						bottom_count_right += 1
					elif x[i] < right_end_right:
						bin_index = int((x[i] - left_end_right) * scale_factor_right)
						bin_counts[bin_index] += 1
				
				else:
					i += 1

			# Stop if all points in medbin are the same
			if len(np.unique(x[r:])) == 1:
				return float(x[r])

			# Stop if there's <= 20 points left
			if n - r <= 20:
				break
		
		a = 0.0
		for i in range(r + 1, n):
			a = x[i]
			# This is equal to C's
			# for (j = i-1; j >= r; j--) 
			for j in reversed(range(r, i - 1)):
				if x[j] > a:
					break
				x[j + 1] = x[j]
			x[j + 1] = a

		return float((x[r - 1 + k] + x[r - 1 + k_right]) / 2)

if __name__ == '__main__':
	# Example
	arr = np.random.uniform(0, 100, 201)
	arr2 = np.array(arr)
	arr3 = np.array(arr)
	n = len(arr)
	if n & 1:
		print('n is odd')
	s = time()
	print('binmedian', binmedian(arr))
	print('time in sec {0:.5f}'.format(time() - s))
	s = time()
	print('actual median')
	sorted_arr = np.sort(arr2)
	if n & 1:
		print(sorted_arr[int((n - 1) / 2)])
	else:
		one = sorted_arr[int(n / 2)]
		two = sorted_arr[int(n / 2) - 1]
		print((one + two) / 2)
	print('time in sec {0:.5f}'.format(time() - s))
	s = time()
	print('numpy median')
	print(np.median(arr3))
	print('time in sec {0:.5f}'.format(time() - s))