import subprocess
import glob
import os
import argparse


def select_fasta(
        input_dir:str,
        lenght_th:int
    )->list:

    all_fasta = glob.glob(os.path.join(input_dir,'*.faa'))
    selected_fasta = []
    for fasta in all_fasta:
        with open(fasta,'r') as reader:
            count = 0
            for line in reader:
                if line.startswith('>'):
                    count += 1
            else:
                continue

        if count >= lenght_th:
            selected_fasta.append(fasta)

    return selected_fasta

def count_max_seq_length(fasta_path: str) -> int:
    max_len = 0
    count_seqs = 0
    with open(fasta_path, 'r') as reader:
        for line in reader:
            if not line.startswith('>'):
                max_len = max(max_len, len(line.strip()))
            if line.startswith('>'):
                count_seqs += 1

    return max_len, count_seqs



def run_mafft(input_fasta: str, output_fasta_aln: str, mafft_path: str = "mafft", extra_args=None):
    """
    Run MAFFT alignment from a Python script.

    Args:
        input_fasta (str): Path to input FASTA file.
        output_fasta (str): Path to write the aligned output FASTA.
        mafft_path (str): Path to MAFFT binary (default assumes it's in your PATH).
        extra_args (list): Optional list of extra MAFFT arguments.
    """
    # if extra_args is None:
    #     extra_args = []

    max_length,n_seqs = count_max_seq_length(input_fasta)

    if n_seqs < 200 and max_length < 2000:
        args = [mafft_path, '--maxiterate', '1000', '--localpair', input_fasta]
    else:
        args = [mafft_path, '--maxiterate', '1000', '--genafpair', input_fasta]


    with open(output_fasta_aln, "w") as out_f:
            subprocess.run(args, stdout=out_f, stderr=subprocess.PIPE, check=True)




def main(input_dir:str,
         output_dir:str
         ):
        

        fasta_files = select_fasta(
                input_dir=input_dir,
                lenght_th=args.lenght_th
                )
        
        for file in fasta_files:
                
                file_name = os.path.basename(file)
                output_path = os.path.join(output_dir, file_name.replace('.faa', '.aln.faa'))
                run_mafft(input_fasta=file,output_fasta_aln=output_path)




parser = argparse.ArgumentParser("preprocess_sequences")
parser.add_argument(
        "-f", "--fasta",
        help="Excel file containing the metadata for the sequences.",
        type=str
    )
parser.add_argument(
        "-o", "--output_dir",
        help="Directory containing the aligned",
        type=str
    )
parser.add_argument(
        "-t", "--lenght_th"
        help="Select chains based on Minimu number of sequences per file "
        type =int
    )

args = parser.parse_args()

main(
    input_dir=input_dir,
    output_dir=args.output_dir
         )

dictionary = de_multiplex(
    fasta_file=args.fasta,
    output_dir=args.output_dir
)