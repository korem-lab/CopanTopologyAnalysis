import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
def load_large_csv(file_path, chunksize=100000):
    chunks = pd.read_csv(file_path, chunksize=chunksize, low_memory=False)
    return pd.concat(chunks, ignore_index=True)

degree_classification = pd.read_csv("workflow/out/node_degrees/sample_1_0_02_node_degrees.csv")
bfs_df = load_large_csv("workflow/out/distance_degree/sample_1_0_02_100Lw150Nw0.1p10.0q120k_distancesWithDegree.csv")
# dfs_df = load_large_csv("workflow/out/distance_degree/sample_1_0_02_100Lw150Nw10.0p0.1q120k_distancesWithDegree.csv")
# nofs_df = load_large_csv("workflow/out/distance_degree/sample_1_0_02_100Lw150Nw1.0p1.0q120k_distancesWithDegree.csv")

# Data wrangling
def classify_degrees(df, strategy):
    df['same_degree'] = df['degree_i'].eq(df['degree_j']).replace({True: 'same_degree', False: 'different_degree'})
    df['pair_degree'] = np.where(df['degree_i'].eq(df['degree_j']), df['degree_i'], np.nan)
    df['pair_degree'] = pd.Categorical(df['pair_degree'], categories=[1, 2, 3, 4, 5, 6], ordered=True)
    df['strategy'] = strategy

    return df

bfs_classes = classify_degrees(bfs_df.copy(), 'bfs')
# dfs_classes = classify_degrees(dfs_df.copy(), 'dfs')
# nofs_classes = classify_degrees(nofs_df.copy(), 'equal_probabilities')

# Make sure that each DataFrame has the strategy column
print(bfs_classes.head())  # Check the 'strategy' column
# print(dfs_classes.head())  # Check the 'strategy' column
# print(nofs_classes.head())  # Check the 'strategy' column

# classes_df = pd.concat([bfs_classes, dfs_classes, nofs_classes], ignore_index=True)

# Box + Violin plots
# sns.set_theme(style="whitegrid")

# # BFS test
# # plt.figure(figsize=(10, 6))
# # sns.violinplot(x='same_degree', y='distance', hue='strategy', data=bfs_classes[bfs_classes['degree_i'].ne(0) | bfs_classes['degree_j'].ne(0)], palette='Set3', width=1.5)
# # sns.boxplot(x='same_degree', y='distance', hue='strategy', data=bfs_classes[bfs_classes['degree_i'].ne(0) | bfs_classes['degree_j'].ne(0)], color='white', width=0.1)
# # plt.xlabel("Same vs. Different Degree Pairs")
# # plt.title("Pairwise Distances for Same vs. Different Degree Pairs by Strategy")
# # plt.legend([], [], frameon=False)
# # plt.show()

# # Pairwise distances for same vs. different degree pairs
# plt.figure(figsize=(10, 6))
# sns.violinplot(x='same_degree', y='distance', hue='strategy', data=classes_df[classes_df['degree_i'].ne(0) | classes_df['degree_j'].ne(0)], palette='Set3', width=1.5)
# sns.boxplot(x='same_degree', y='distance', hue='strategy', data=classes_df[classes_df['degree_i'].ne(0) | classes_df['degree_j'].ne(0)], color='white', width=0.1)
# plt.xlabel("Same vs. Different Degree Pairs")
# plt.title("Euclidean Distances for Same vs. Different Degree Pairs by Strategy")
# plt.legend([], [], frameon=False)
# plt.savefig("workflow/out/plots/distance_v_degreeClass_boxViolin.png", format='png', dpi=150, bbox_inches='tight')

# # Pairwise distances for same degree pairs
# plt.figure(figsize=(10, 6))
# sns.violinplot(x='pair_degree', y='distance', hue='strategy', data=classes_df[classes_df['same_degree'] == 'same_degree'], palette='Pastel2', width=1.5)
# sns.boxplot(x='pair_degree', y='distance', hue='strategy', data=classes_df[classes_df['same_degree'] == 'same_degree'], color='white', width=0.1)
# plt.xlabel("Pair Degree")
# plt.title("Euclidean Distances for Same Degree Pairs by Strategy")
# plt.legend([], [], frameon=False)
# plt.savefig("workflow/out/plots/distance_v_degree_sameDegreePairs_boxViolin.png", format='png', dpi=150, bbox_inches='tight')

# # KDE plots

# # Euclidean distance between same vs. different degree node pairs
# plt.figure(figsize=(10, 6))
# sns.kdeplot(x='distance', hue='strategy', data=classes_df[classes_df['degree_i'].ne(0) | classes_df['degree_j'].ne(0)], palette='Set3', fill=True, alpha = 0.5)
# plt.xlabel("Distance")
# plt.title("Euclidean Distance between Same vs. Different Degree Node Pairs by Strategy")
# sns.move_legend(plt.gca(), 'upper right')
# plt.savefig("workflow/out/plots/distance_v_degreeClass_kde.png", format='png', dpi=150, bbox_inches='tight')

# # Euclidean distances between same degree node pairs by pair degree
# g = sns.FacetGrid(bfs_classes[bfs_classes['same_degree'] == 'same_degree'], col='pair_degree', col_wrap=3, sharex=True, sharey=True, height=4)
# g.map(sns.kdeplot, 'distance', fill=True, hue='strategy', palette='Pastel2', alpha = 0.5)
# g.set_axis_labels("Distance", "Density")
# g.figure.suptitle("Euclidean Distances between Same Degree Node Pairs by Strategy", y=1.02)
# plt.savefig("workflow/out/plots/distance_v_degree_sameDegreePairs_kde.png", format='png', dpi=150, bbox_inches='tight')
