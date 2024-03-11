# Trivial_1D_Persistence

Code to perform the experiments as described in the paper "Families of point sets with identical 1D persistence".

We start by specifying a range of dimensions and point set sizes. Then for each pair (point set size, dimension), a collection of point sets of this (point set size, dimension) specification are produced. The size of the collection of point sets is determined by the "repetitions" parameter.

The code has four possible outputs:

Plot_Rank shows how the ratios of ranks of persistent features changes as the point set size increases (a single dimension must be specified for this experiment).

Plot_Gap_Ratio shows how the median gap ratio changes as the point set size and dimension change (for point sets with more than one persistent feature).

Plot_Gap_Ratio_Rank_1 shows how the mean gap ratio changes as the point set size and dimension change (for point sets with only one persistent feature).

Plot_Persistent_Hists shows histograms of the persistences of features for a selection of dimensions and point set sizes.
