import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

score_file = "workflow/out/clustering_accuracy/silhouette_score_allBatches.csv"
df = pd.read_csv(score_file)  # Populate with p, q, and silhouette scores

df = df[df['n_walks'] == 50]
mean_scores = df.groupby(['p', 'q'])['silhouette_score'].mean().reset_index()
pivot_df = mean_scores.pivot(index='p', columns='q', values='silhouette_score')

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_df, annot=True, cmap='viridis')
plt.title("Silhouette Score Heatmap")
plt.xlabel("q")
plt.ylabel("p")
plt.show()
