# binmedian
A Python implementation of the binmedian algorithm originally written in C (and Fortan) that can be found on http://www.stat.cmu.edu/~ryantibs/median/binmedian.c.

Just like the original C code, this code only contains an implementation for uneven n but will later be updated to work even n as well.

It's currently much slower then, for instance, the numpy median function but it has the advantage of having O(1) memory usage and not requiring a full sort of the data. Can also be combined with the numpy.memmap function to avoid having to load the array in memory.