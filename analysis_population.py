# Import libraries for data manipulation, visualization, and 3D plotting
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the color mapping for populations
population_colors = {
    'EUR': 'blue',
    'EAS': 'red',
    'AMR': 'green',
    'SAS': 'purple',
    'AFR': 'yellow',
    'nan': 'gray'  # 'nan' is a label for some populations
}

# Define file paths
populations_file = '/Users/ar/Documents/bioin/output/Populations.txt'
reference_populations_file = '/Users/ar/Documents/bioin/input/1000G_reference_populations.txt'
output_dir = '/Users/ar/Documents/bioin/output'

# Load the populations data
study_populations = pd.read_csv(populations_file, sep='\t')
reference_populations = pd.read_csv(reference_populations_file, sep='\t')

# Merge both datasets to have a common structure
combined_data = pd.concat([study_populations, reference_populations])

# Map population labels to colors
combined_data['COLOR'] = combined_data['POPULATION'].apply(lambda x: population_colors.get(x, 'black'))

# Function to plot PCA
def plot_pca(data, pcx, pcy, pcz=None, filename='pca_plot.png'):
    fig = plt.figure()
    
    if pcz is None:
        ax = fig.add_subplot(111)
        scatter = ax.scatter(data[pcx], data[pcy], c=data['COLOR'])
    else:
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(data[pcx], data[pcy], data[pcz], c=data['COLOR'])
        
    ax.set_xlabel(pcx)
    ax.set_ylabel(pcy)
    if pcz:
        ax.set_zlabel(pcz)
        
    # Create a legend
    populations = list(population_colors.keys())
    colors = [population_colors[pop] for pop in populations]
    plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=pop,
                          markerfacecolor=color) for pop, color in zip(populations, colors)],
               title='Population')

    plt.savefig(output_dir + filename)
    plt.show()

# Plot 2D and 3D PCA
plot_pca(combined_data, 'PC1', 'PC2', filename='PC1_vs_PC2.png')
plot_pca(combined_data, 'PC2', 'PC3', filename='PC2_vs_PC3.png')
plot_pca(combined_data, 'PC3', 'PC4', filename='PC3_vs_PC4.png')
plot_pca(combined_data, 'PC1', 'PC2', 'PC3', filename='PC1_PC2_PC3.png')
