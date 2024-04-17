<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>README - Genomic Data Analysis Workflow (Analyzing Genetic Ancestry)</h1>
    <h2>Introduction</h2>
    <p>This document outlines the execution of a genomic data analysis workflow. The workflow aims to estimate DNA contamination, analyze genetic ancestry, and assign population labels to a cohort of ten individuals using CRAM sequencing data.</p>
    <h2>Pre-requisites</h2>
    <p>Prior to initiating the workflow, please ensure the following requirements are satisfied:</p>
    <ul>
        <li><strong>Software Dependencies:</strong></li>
        <li>VerifyBamID: A specific version compatible with the data analysis process. The installation guide is available on the <a href="https://github.com/Griffan/VerifyBamID">official VerifyBamID repository</a>.</li>
        <li>Python 3.6 or higher, with pandas and matplotlib libraries installed.</li>
        <li><strong>Data Files and Directories:</strong></li>
        <li>Place the CRAM files and their indices in the <a href="https://github.com/CERC-Genomic-Medicine/skills_test_3/tree/main/input">input/ directory</a>.</li>
        <li>Download the GRCh38 reference panel and its index file from the NCBI FTP server and store them in the resource/ folder. Due to their large size, these files need to be downloaded directly to your system. Links: <a href="ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa">GRCh38.fa</a>, <a href="ftp://ftp-trace.ncbi.nih.gov/1000genomes/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa.fai">GRCh38.fai</a></li>
    </ul>
    <h2>Workflow Execution Steps</h2>
    <ol>
        <li>VerifyBamID Installation: Install VerifyBamID as per the instructions on its official repository.</li>
        <li>Reference Data Download: Obtain the GRCh38 reference genome files, both the .fa and .fa.fai files, and ensure they are available in the resource/ folder.</li>
        <li>Configure Python Environment: Create and activate a Python virtual environment, then install the pandas and matplotlib libraries using pip.</li>
        <li>Running the Scripts: Process CRAM files to estimate DNA contamination levels, analyze ancestry information to assign population labels, and generate PCA plots to visualize ancestry results.</li>
    </ol>
    <h2>Outputs</h2>
    <p>Generated files include DNA contamination estimates (Contamination.txt), PCA scatter plots in PNG format, and PCA coordinates with assigned population labels (Populations.txt).</p>
    <h2>Code Documentation</h2>
    <p>The source code for the analysis is comprehensively commented to provide clarity on each segment's purpose and facilitate a smooth workflow experience.</p>
    <h2>Directory Structure</h2>
    <p>Ensure that the file paths in the scripts correctly reflect the local directory structure as follows:</p>
    <ul>
        <li>CRAM files and reference population data in input/</li>
        <li>GRCh38 reference genome files in resource/</li>
        <li>Outputs to be saved in output/</li>
    </ul>
    <h2>Contact</h2>
    <p>Prepared by Ashif Rahman, March 24, 2024. 
    For additional support or questions regarding the workflow, please contact <a href="mailto:ashif.rahman@uleth.ca">Ashif Rahman</a></p>
</body>
</html>
