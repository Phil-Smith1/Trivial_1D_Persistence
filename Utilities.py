# Imports.

import numpy as np
from ripser import ripser
from persim import plot_diagrams
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Function definitions.

def Generate_Random_Point( d ):

    return np.random.rand( d )

def Generate_Point_Cloud( dim, num_points ):

    points = []

    while len( points ) < num_points:

        p = Generate_Random_Point( dim )

        points.append( p )

    return np.array( points )

def Num_Rank( rank, k ):

    rank_array = np.where( rank >= k )

    if rank_array[0].any():

        r = rank_array[0][0]

    else:

        r = rank.size

    return r

def Compute_Gap_Ratio( persistences, diagram ):

    persistences.sort() # Sort in increasing persistence.

    if persistences: # List not empty implies at least 1 persistent feature.

        if len( persistences ) == 1: # Only one persistent feature.

            gap_ratio = 0 # Can't compute gap ratio, so set to zero.
            gap_ratio_rank_1 = persistences[0] / diagram[0][len( diagram[0] ) - 2][1] # Extract the gap ratio in the case of only one 1D feature.

        else: # At least two persistent features.

            gaps = [] # Object to contain gap widths in the persistent diagram.

            for k in range( len( persistences ) - 1 ): # Looping over 1D features (which have already been sorted).

                gap = persistences[len( persistences ) - 1 - k] - persistences[len( persistences ) - 2 - k]
                gaps.append( gap ) # Append gap width.

            gaps.append( persistences[0] ) # Append gap width of the gap that borders the diagonal.

            gaps.sort( reverse = True ) # Sort the gap widths so that the widest gap is first.

            if gaps[1] > 0.005: # Avoid case when second widest gap is close to zero.

                gap_ratio = gaps[0] / gaps[1] # Compute gap ratio.
                gap_ratio_rank_1 = 0 # Set gap_ratio_rank_1 to zero since there's more than one persistent feature.

            else: # Second widest gap is close to zero, treat as if there's only one 1D feature.

                gap_ratio = 0 # Can't compute gap ratio, so set to zero.
                gap_ratio_rank_1 = gaps[0] / diagram[0][len( diagram[0] ) - 2][1] # Extract the gap ratio in the case of only one 1D feature.

        return gap_ratio, gap_ratio_rank_1

    else: # No persistent features.

        return 0, 0

def Extract_Rank_Data( rank, overall_ranks, repetitions ):

    rank = np.sort( rank ) # Sort the ranks.

    ranks = np.zeros( 7 )

    # Computing the number of point clouds of rank 0, 1, 2, 3, 4, 5 and >= 6.

    ranks[0] = Num_Rank( rank, 1 )
    ranks[1] = Num_Rank( rank, 2 ) - ranks.sum()
    ranks[2] = Num_Rank( rank, 3 ) - ranks.sum()
    ranks[3] = Num_Rank( rank, 4 ) - ranks.sum()
    ranks[4] = Num_Rank( rank, 5 ) - ranks.sum()
    ranks[5] = Num_Rank( rank, 6 ) - ranks.sum()
    ranks[6] = repetitions - Num_Rank( rank, 6 )

    overall_ranks.append( ranks )

def Extract_GR_Data( dim, start_dim, num, start_num_points, repetitions, output_gap_ratio_plot, gap_ratio_rank_1, gap_ratio, results_gr_rank1, results_gr_rank2 ):

    results_gr_rank1[dim - start_dim][num - start_num_points] = gap_ratio_rank_1.sum() / np.count_nonzero( gap_ratio_rank_1 )

    gap_ratio = np.sort( gap_ratio )
    gap_ratio = gap_ratio[repetitions - np.count_nonzero( gap_ratio ):]

    if output_gap_ratio_plot:

        if len( gap_ratio ) > 0:

            if len( gap_ratio ) % 2 == 1:

                results_gr_rank2[dim - start_dim][num - start_num_points] = gap_ratio[int( (len( gap_ratio ) - 1) / 2 )]

            else:

                results_gr_rank2[dim - start_dim][num - start_num_points] = (gap_ratio[int( (len( gap_ratio ) - 2) / 2 )] + gap_ratio[int( len( gap_ratio ) / 2 )]) / 2

def Plot_Rank( overall_ranks, num_points, dims, output_directory ):

    trivial = np.array( [x[0] / 10. for x in overall_ranks] )
    rank_1 = np.array( [x[1] / 10. for x in overall_ranks] )
    rank_2 = np.array( [x[2] / 10. for x in overall_ranks] )
    rank_3 = np.array( [x[3] / 10. for x in overall_ranks] )
    rank_4 = np.array( [x[4] / 10. for x in overall_ranks] )
    rank_5 = np.array( [x[5] / 10. for x in overall_ranks] )
    rank_6 = np.array( [x[6] / 10. for x in overall_ranks] )
    ind = [x for x in range( len( num_points ) )]

    plt.figure(figsize=(10,6))
    plt.bar( ind, rank_6, width=0.8, label='rank > 5', bottom=rank_5 + rank_4 + rank_3 + rank_2 + rank_1 + trivial )
    plt.bar( ind, rank_5, width=0.8, label='rank 5', bottom=rank_4 + rank_3 + rank_2 + rank_1 + trivial )
    plt.bar( ind, rank_4, width=0.8, label='rank 4', bottom=rank_3 + rank_2 + rank_1 + trivial )
    plt.bar( ind, rank_3, width=0.8, label='rank 3', bottom=rank_2 + rank_1 + trivial )
    plt.bar( ind, rank_2, width=0.8, label='rank 2', bottom=rank_1 + trivial )
    plt.bar( ind, rank_1, width=0.8, label='rank 1', bottom=trivial )
    plt.bar( ind, trivial, width=0.8, label='rank 0')

    plt.xticks(ind, num_points)
    plt.ylabel("Percentage", fontsize = 18)
    plt.xlabel("Number of Points", fontsize = 18)
    plt.legend(loc="upper right")
    plt.title("Dimension " + str( dims[0] ), fontsize = 18)
    ax = plt.gca()
    ax.legend(bbox_to_anchor=(1.01, 1.02))
    plt.tight_layout()

    plt.savefig( output_directory + "rank_plot.pdf" )

    plt.show()

def Plot_Gap_Ratio( start_dim, range_dim, num_points, results_gr_rank2, output_directory ):

    for i in range( range_dim ):

        plt.plot( num_points, results_gr_rank2[i,:], label = "Dim: " + str( i + start_dim ) )

    plt.xlabel( "Number of Points" )
    plt.yticks( np.arange( 1, 4, 1 ) )
    plt.ylabel( "Median Gap Ratio" )
    ax = plt.gca()
    ax.legend( bbox_to_anchor = ( 1.22, 1.02 ) )
    plt.tight_layout()
    plt.savefig( output_directory + "GR.pdf" )
    plt.show()

def Plot_Gap_Ratio_Rank_1( start_dim, range_dim, num_points, results_gr_rank1, output_directory ):

    for i in range( range_dim ):

        plt.plot( num_points, results_gr_rank1[i,:], label = "Dim: " + str( i + start_dim ) )

    plt.legend()
    plt.xlabel( "Number of Points" )
    plt.ylabel( "Gap Ratio (Rank 1)" )
    plt.savefig( output_directory + "GR1.pdf" )
    plt.show()

def Plot_Persistence_Hists( overall_pers, output_directory ):

    fig, axs = plt.subplots( 3, 3, gridspec_kw = {'wspace':0.1, 'hspace':0.1} )

    for i in range( len( overall_pers ) ):

        axs[int( i / 3 )][i % 3].hist( overall_pers[i], bins = 30, range = (0, 0.3), weights = 100 * np.ones( len( overall_pers[i] ) ) / len( overall_pers[i] ) )
        start, end = axs[int( i / 3 )][i % 3].get_xlim()
        axs[int( i / 3 )][i % 3].xaxis.set_ticks( np.arange( 0, end, 0.1 ) )
        axs[int( i / 3 )][i % 3].yaxis.set_major_formatter( PercentFormatter( ) )
        plt.tight_layout()

    for ax in fig.get_axes():

        ax.label_outer()

    plt.savefig( output_directory + "Hist.pdf" )
    plt.show()
