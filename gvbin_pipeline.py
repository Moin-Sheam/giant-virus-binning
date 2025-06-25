import os
import subprocess
import argparse
import shutil

def run_command(command, cwd=None):
    print(f"\nRunning: {command}")
    process = subprocess.run(command, shell=True, executable="/bin/bash", cwd=cwd,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process.stdout)
    if process.returncode != 0:
        print(process.stderr)
        raise RuntimeError(f"Command failed: {command}")

def main():
    parser = argparse.ArgumentParser(description="GVMAG identification pipeline using MetaBAT2 and ViralRecall2.")
    parser.add_argument("-i", "--input", required=True, help="Input contigs FASTA file")
    parser.add_argument("-o", "--output", required=True, help="Output directory for results")
    parser.add_argument("--bam_dir", required=True, help="Directory containing sorted BAM files")
    parser.add_argument("--viralrecall_dir", required=True, help="Directory containing viralrecall.py")
    parser.add_argument("--viralrecall_env", default="viralrecall", help="Name of the conda environment for ViralRecall")

    args = parser.parse_args()

    input_fasta = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)
    bam_dir = os.path.abspath(args.bam_dir)
    viralrecall_dir = os.path.abspath(args.viralrecall_dir)

    os.makedirs(output_dir, exist_ok=True)

    depth_file = os.path.join(output_dir, "depth.txt")
    bins_prefix = os.path.join(output_dir, "bins")
    viralrecall_output_prefix = os.path.join(output_dir, "viralrecall_results")

    print("Step 1: Calculating depth file...")
    run_command(f"jgi_summarize_bam_contig_depths --outputDepth {depth_file} {bam_dir}/*.bam")

    print("Step 2: Running MetaBAT2 binning...")
    run_command(f"metabat2 -i {input_fasta} -a {depth_file} -s 100000 -m 2500 -o {bins_prefix}")

    print("Step 2b: Preparing clean bins directory for ViralRecall...")
    bins_only_dir = os.path.join(output_dir, "bins_only")
    os.makedirs(bins_only_dir, exist_ok=True)

    # Move only bin fasta files (e.g. bins.1.fa) into bins_only_dir
    for file in os.listdir(output_dir):
        if file.startswith("bins.") and file.endswith(".fa"):
            shutil.move(os.path.join(output_dir, file), os.path.join(bins_only_dir, file))
    print(f"Moved bins to {bins_only_dir} for ViralRecall input.")

    print("Step 3: Running ViralRecall2...")
    run_command(
        f"conda run -n {args.viralrecall_env} python viralrecall.py -i {bins_only_dir} "
        f"-p {viralrecall_output_prefix} -b --contiglevel -e 1e-5",
        cwd=viralrecall_dir
    )

    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main()
