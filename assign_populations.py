# Import modules for file system interaction, data structures, and mathematical operations
import os
from dataclasses import dataclass
import math

# Define a dataclass to represent individuals with their sample name and principal components.
@dataclass
class Individual:
    sample: str
    pc1: float = None
    pc2: float = None
    pc3: float = None
    pc4: float = None
    population: str = None

# Set directories and file paths for input and output data.
ancestry_dir = "output/"
contamination_dir = "output/"
reference_populations_file = "input/1000G_reference_populations.txt"
reference_pcs_file = "/Users/ar/Documents/bioin/VerifyBamID/resource/1000g.phase3.100k.b38.vcf.gz.dat.V"
contamination_file = "output/Contamination.txt"
populations_file = "output/Populations.txt"

# Function to parse ancestry files and extract principal components.
def parse_ancestry_file(filename):
    with open(filename) as f:
        for line in f:
            if line.startswith("IntendedSample"):
                parts = line.strip().split()
                if len(parts) >= 5:
                    _, pc1, pc2, pc3, pc4 = parts
                    return float(pc1), float(pc2), float(pc3), float(pc4)
    return 0.0, 0.0, 0.0, 0.0

# Function to parse reference population data and create Individual objects.
def parse_reference_populations(filename):
    reference_individuals = []
    with open(filename) as f:
        for line in f:
            sample, population = line.strip().split()
            reference_individuals.append(Individual(sample, None, None, None, None, population))
    return reference_individuals
# Function to parse reference PC data and populate PC values in Individual objects.
def parse_reference_pcs(filename, reference_individuals):
    with open(filename) as f:
        for line in f:
            data = line.strip().split()
            sample = data[0]
            for individual in reference_individuals:
                if individual.sample == sample:
                    individual.pc1, individual.pc2, individual.pc3, individual.pc4 = map(float, data[1:5])
                    break

# Function to calculate the Euclidean distance between two individuals based on their PCs.
def calculate_euclidean_distance(individual1, individual2):
    return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(
        [individual1.pc1, individual1.pc2, individual1.pc3, individual1.pc4],
        [individual2.pc1, individual2.pc2, individual2.pc3, individual2.pc4])))

# Function to assign the most likely population to a study individual based on Euclidean distance to reference individuals.
def assign_population(study_individual, reference_individuals):
    closest_distance = float("inf")
    closest_population = None
    for reference_individual in reference_individuals:
        distance = calculate_euclidean_distance(study_individual, reference_individual)
        if distance < closest_distance:
            closest_distance = distance
            closest_population = reference_individual.population
    return closest_population

# Function to extract the FREEMIX value (DNA contamination) from a selfSM file.
def extract_freemix(filename):
    with open(filename) as f:
        headers = f.readline().strip().split()  # Read the header line
        if "FREEMIX" in headers:
            freemix_index = headers.index("FREEMIX")
            for line in f:
                return line.strip().split()[freemix_index]  # Return the FREEMIX value
    return "NA"  # Return "NA" if FREEMIX value is not found

# Parse reference population data and PC values.
def parse_ancestry_file(filename):
    pcs = []  # List to hold PC values
    with open(filename) as f:
        next(f)  # Skip the header line
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:  # Expecting 3 columns: PC, ContaminatingSample, IntendedSample
                try:
                    pc_value = float(parts[2])  # Get the intended sample's PC value
                    pcs.append(pc_value)
                except ValueError:
                    pass  # Skip lines where conversion to float fails
    if len(pcs) == 4:
        return tuple(pcs)
    return None, None, None, None  # Return None if the expected number of PC values aren't found

# Function to calculate the Euclidean distance between two individuals based on their principal components.
def calculate_euclidean_distance(individual1, individual2):
    pc1_1, pc2_1, pc3_1, pc4_1 = (individual1.pc1 or 0.0, individual1.pc2 or 0.0, 
                                  individual1.pc3 or 0.0, individual1.pc4 or 0.0)
    pc1_2, pc2_2, pc3_2, pc4_2 = (individual2.pc1 or 0.0, individual2.pc2 or 0.0, 
                                  individual2.pc3 or 0.0, individual2.pc4 or 0.0)
    
# Calculate the Euclidean distance using the formula: sqrt(sum((pc1_1 - pc1_2)^2, ..., (pc4_1 - pc4_2)^2))
    return math.sqrt((pc1_1 - pc1_2) ** 2 + (pc2_1 - pc2_2) ** 2 + 
                     (pc3_1 - pc3_2) ** 2 + (pc4_1 - pc4_2) ** 2)

reference_individuals = parse_reference_populations(reference_populations_file)
parse_reference_pcs(reference_pcs_file, reference_individuals)

# Open output files for writing contamination and population data.
with open(contamination_file, "w") as f_cont, open(populations_file, "w") as f_pop:
    f_cont.write("SAMPLE\tFREEMIX\n")
    f_pop.write("SAMPLE\tPC1\tPC2\tPC3\tPC4\tPOPULATION\n")
    
    # Iterate through ancestry files in the output directory.
    for filename in os.listdir(ancestry_dir):
        if filename.endswith(".Ancestry"):
            base_filename = filename.replace(".Ancestry", "")
            pc1, pc2, pc3, pc4 = parse_ancestry_file(os.path.join(ancestry_dir, filename))

            # Extract FREEMIX value from the corresponding selfSM file.
            freemix_file = os.path.join(contamination_dir, f"{base_filename}.selfSM")
            freemix_value = extract_freemix(freemix_file)

            # Write contamination data to the output file.
            f_cont.write(f"{base_filename}\t{freemix_value}\n")

            # Create a study individual object with PCs and assign population.
            study_individual = Individual(base_filename, pc1, pc2, pc3, pc4)
            population = assign_population(study_individual, reference_individuals)

            # Write population data to the output file.
            f_pop.write(f"{base_filename}\t{pc1}\t{pc2}\t{pc3}\t{pc4}\t{population}\n")

# Print a message indicating that the output files have been generated.
print("Contamination.txt and Populations.txt files generated.")

