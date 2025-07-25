# GVMAG Pipeline

A Python script for identifying Giant Virus Metagenome-Assembled Genomes (GVMAGs) from metagenomic data.  
This pipeline performs contig binning using **MetaBAT2** and detects giant virus marker genes using **ViralRecall2**.

---

## Features

- Calculates contig depth from sorted BAM files  
- Performs binning with MetaBAT2  
- Detects giant virus marker genes using ViralRecall2  

---

## Requirements

The following tools **must be installed separately** using conda before running the pipeline:

- [MetaBAT2](https://bitbucket.org/berkeleylab/metabat/src/master/)  
- [ViralRecall2](https://github.com/faylward/viralrecall)  

Make sure your BAM files are sorted and indexed.

---

## Usage

Run the pipeline script with the following command:

```bash
python gvbin_pipeline.py \
  -i /path/to/contigs.fa \
  -o /path/to/output_directory \
  --bam_dir /path/to/sorted_bam_files \
  --viralrecall_dir /path/to/viralrecall_directory \
  --viralrecall_env viralrecall
Arguments
-i, --input: Path to input contigs FASTA file
-o, --output: Directory where outputs will be saved
--bam_dir: Directory containing sorted BAM files for depth calculation
--viralrecall_dir: Directory containing viralrecall.py script
--viralrecall_env: Name of the conda environment where ViralRecall is installed (default: viralrecall)


