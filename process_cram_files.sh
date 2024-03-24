#!/bin/bash

# Define directories and files for the analysis.
CRAM_DIR="/Users/ar/Documents/bioin/input"  # Directory containing the CRAM files
OUTPUT_DIR="/Users/ar/Documents/bioin/output"  # Directory to store the output files
REFERENCE="/Users/ar/Documents/bioin/resource/GRCh38_full_analysis_set_plus_decoy_hla.fa"  # Reference genome file
SVDPREFIX="/Users/ar/Documents/bioin/VerifyBamID/resource/1000g.phase3.100k.b38.vcf.gz.dat"  # 1000 Genomes reference panel data
VERIFYBAMID="/Users/ar/Documents/bioin/VerifyBamID/bin/VerifyBamID"  # Path to the VerifyBamID executable
CONTAMINATION_FILE="$OUTPUT_DIR/Contamination.txt"  # Output file for contamination values

# Create the output directory if it doesn't exist.
mkdir -p "$OUTPUT_DIR"

# Add a header to the Contamination.txt file to label the columns.
echo -e "SAMPLE\tFREEMIX" > "$CONTAMINATION_FILE"

# Process each CRAM file in the input directory.
for CRAM in "$CRAM_DIR"/*.cram; do
  SAMPLE_NAME=$(basename "$CRAM" .cram)  # Extract the sample name from the filename
  echo "Starting processing of $SAMPLE_NAME at $(date)"  # Print a message to track progress

  # Run VerifyBamID to estimate DNA contamination and ancestry, calculating 4 principal components.
  $VERIFYBAMID --SVDPrefix $SVDPREFIX \
               --Reference $REFERENCE \
               --BamFile $CRAM \
               --NumPC 4 \
               --Output "$OUTPUT_DIR/$SAMPLE_NAME" > "$OUTPUT_DIR/$SAMPLE_NAME.output.txt"

  echo "Finished processing of $SAMPLE_NAME at $(date)"  # Print a message to track progress

  # Extract the FREEMIX value (DNA contamination) from the VerifyBamID output.
  FREEMIX=$(grep "FREEMIX(Alpha)" "$OUTPUT_DIR/$SAMPLE_NAME.output.txt" | awk '{print $2}')

  # Append the sample name and FREEMIX value to the Contamination.txt file.
  echo -e "$SAMPLE_NAME\t$FREEMIX" >> "$CONTAMINATION_FILE"

done