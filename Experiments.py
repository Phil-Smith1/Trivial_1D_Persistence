# Imports.

import numpy as np
from ripser import ripser
from persim import plot_diagrams
import matplotlib.pyplot as plt

import Utilities as util

# Parameters.

output_directory = "/Users/philsmith/Documents/Postdoc/Ripser/" # Where the outputs should be saved.

start_dim = 2 # The smallest dimension considered.

range_dim = 5 # The number of dimensions considered.

start_num_points = 4 # The smallest size of point sets considered.

range_num_points = 17 # The range of the size of the point sets considered.

repetitions = 1000 # The number of repetitions of each configuration of parameters.

output_rank_plot = False # Output a plot of the ranks. "range_dim" should be 1.

output_gap_ratio_plot = True # Output a plot of the gap ratio.

output_gap_ratio_rank1_plot = True # Output a plot of the gap ratio when the rank is 1.

output_persistence_plots = True # Output histograms of persistence at various configurations of the parameters.

np.random.seed( 10 ) # Seeding the random number generator.

dims = [a + start_dim for a in range( range_dim )] # Producing a list of dimensions to consider.
num_points = [a + start_num_points for a in range( range_num_points )] # Producing a list of sizes of point sets to consider.

results_gr_rank1 = np.zeros( (range_dim, range_num_points) ) # Object for storing results of the gap ratio with rank 1.
results_gr_rank2 = np.zeros( (range_dim, range_num_points) ) # Object for storing results of the gap ratio with rank >= 2.

overall_ranks = [] # List for storing data relating to the ranks at each configuration of the parameters.
overall_pers = [] # List of lists of persistences at various configurations of the parameters.

for dim in dims: # Looping over the dimensions.

    for num in num_points: # Looping over the range of the num_points parameter.

        rank = np.zeros( repetitions ) # Object that will contain the rank (number of 1D persistent features) of each repetition.

        overall_persistences = [] # Object that will be a list of the persistences of all 1D persistent features found over all repetitions.

        # FYI: Gap ratio = widest diagonal gap / second widest diagonal gap. Must be at least two 1D features.
        # If computing the gap ratio of a persistent diagram with only one 1D feature, the formula is gap ratio = persistence of 1D feature/longest edge in MST.

        gap_ratio = np.zeros( repetitions ) # Object that will contain the gap raio of each repetition. (Rank >= 2.)
        gap_ratio_rank_1 = np.zeros( repetitions ) # Object that will contain the gap ratio of each repetition if Rank = 1.

        for i in range( repetitions ): # Repeating X times, where X = "repetitions".

            if i == 0:

                print( "Dim: ", dim, " No. Points: ", num )

            points = util.Generate_Point_Cloud( dim, num ) # Generate the point cloud and save it in the numpy array "points".

            diagram = ripser( points, maxdim = 1 )['dgms'] # Compute persistence using Ripser.

            rank[i] = len( diagram[1] ) # Extract the rank of the 1D persistent homology.

            persistences = [] # Object to contain list of persistences of the 1D persistent features

            for j in range( int( rank[i] ) ): # Looping over 1D persistent features.

                persistence = diagram[1][j][1] - diagram[1][j][0]

                overall_persistences.append( persistence )
                persistences.append( persistence )

            gap_ratio[i], gap_ratio_rank_1[i] = util.Compute_Gap_Ratio( persistences, diagram ) # Extracting the gap ratios.

        util.Extract_Rank_Data( rank, overall_ranks, repetitions ) # Extracting data relating to the rank.

        util.Extract_GR_Data( dim, start_dim, num, start_num_points, repetitions, output_gap_ratio_plot, gap_ratio_rank_1, gap_ratio, results_gr_rank1, results_gr_rank2 ) # Extracting data relating to the gap ratio.

        if (dim == 2 or dim == 5 or dim == 8) and (num == 10 or num == 15 or num == 20): # Various configurations of the parameters.

            overall_pers.append( overall_persistences )

if output_rank_plot:

    util.Plot_Rank( overall_ranks, num_points, dims, output_directory )

if output_gap_ratio_plot:

    util.Plot_Gap_Ratio( start_dim, range_dim, num_points, results_gr_rank2, output_directory )

if output_gap_ratio_rank1_plot:

    util.Plot_Gap_Ratio_Rank_1( start_dim, range_dim, num_points, results_gr_rank1, output_directory )

if output_persistence_plots:

    util.Plot_Persistence_Hists( overall_pers, output_directory )
