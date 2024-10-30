import numpy as np
import pandas as pd
import sys

DIST_DEG_F = sys.argv[1]
DISTRIBUTION_F = sys.argv[2]
STATS_F = sys.argv[3]
DIMENSIONS=sys.argv[4]
WALK_LENGTH = sys.argv[5]
N_WALKS = sys.argv[6]
P_VAL = sys.argv[7]
Q_VAL = sys.argv[8]
GRAPH_ID = sys.argv[9]

def main():
    dist_deg_df = pd.read_csv(DIST_DEG_F)

    dist_deg_df['same_degree'] = dist_deg_df['degree_i'] == dist_deg_df['degree_j']

    stats_overall = dist_deg_df['distance'].describe()
    stats_same_degree = dist_deg_df[dist_deg_df['same_degree']]['distance'].describe()
    stats_diff_degree = dist_deg_df[~dist_deg_df['same_degree']]['distance'].describe()

    stats_overall['median'] = dist_deg_df['distance'].median()
    stats_same_degree['median'] = dist_deg_df[dist_deg_df['same_degree']]['distance'].median()
    stats_diff_degree['median'] = dist_deg_df[~dist_deg_df['same_degree']]['distance'].median()

    stats_overall['degree_class'] = "all_connected_nodes"
    stats_same_degree['degree_class'] = "same_degree"
    stats_diff_degree['degree_class'] = "diff_degree"    
    
    overall_df = stats_overall.to_frame(name='value').reset_index()
    same_deg_df = stats_same_degree.to_frame(name='value').reset_index()
    diff_deg_df = stats_diff_degree.to_frame(name='value').reset_index()

    overall_df.rename(columns={'index': 'variable'}, inplace=True)
    overall_wide = overall_df.set_index('variable').T

    same_deg_df.rename(columns={'index': 'variable'}, inplace=True)
    same_deg_wide = same_deg_df.set_index('variable').T

    diff_deg_df.rename(columns={'index': 'variable'}, inplace=True)
    diff_deg_wide = diff_deg_df.set_index('variable').T

    df = pd.concat([overall_wide, same_deg_wide, diff_deg_wide])
    df['dimensions'] = DIMENSIONS
    df['walk_length'] = WALK_LENGTH
    df['n_walks'] = N_WALKS
    df['p'] = P_VAL
    df['q'] = Q_VAL
    df['graph_id'] = GRAPH_ID
    df['run'] = DIST_DEG_F

    df.to_csv(DISTRIBUTION_F, index=False)
    
if __name__ == '__main__':
    main()
