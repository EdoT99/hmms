import argparse
import os
from collections import defaultdict



def get_handle(file_handler:dict,
               output_dir:str,
               group_chain
               ):
    
    if file_handler[group_chain] is None:
        path = os.path.join(output_dir, f"{group_chain}.faa")
        file_handler[group_chain] = open(path, "a")  # Open file in append mode
    
    return file_handler[group_chain]


def extract_group(header,
                  separator = "|",
                  ):
    # Remove the ">" and split
    parts = header.lstrip(">").split(separator)

    if len(parts) == 3:
        id = parts[0]
        species_name = parts[1]
        subparts = parts[2].split('_')
        group_chain = subparts[2]
    else:
        print(f'Unknown header --> {header}')

    return id,species_name,group_chain



def de_multiplex(
        fasta_file:str,
        output_dir:str,
)->dict:
    
    os.makedirs(output_dir,exist_ok=True)

    file_handles = defaultdict(lambda: None)


    with open(fasta_file,'r')as reader:
        dict_counts = {}

        for line in reader:
            line = line.strip()

            if line.startswith('>'):
                header = line

                id,s_name,chain_group=extract_group(header,separator = "|")
                header_new = f'>{'#'.join([id,s_name,chain_group])}'

                handle = get_handle(
                    file_handler=file_handles,
                    output_dir=output_dir,
                    group_chain=chain_group
                                    )

                if chain_group not in dict_counts.keys():
                    dict_counts[chain_group] = 1
                else:
                    dict_counts[chain_group] += 1
            
            else:
                sequence = line
                if handle and header_new:
                    handle.write(f'{header_new}\n{sequence}\n')

                
                
    # close all handles
    for h in file_handles.values():
        h.close()
    #writing counts
    file_counts= os.path.join(output_dir,'chain_counts.txt')

    with open(file_counts,'w') as writer:
        for k,v in dict_counts.items():
            writer.write(f'{k}:{v}\n')
            print(f'{k}:{v}')

    return dict_counts



parser = argparse.ArgumentParser("preprocess_sequences")
parser.add_argument(
        "-f", "--fasta",
        help="Excel file containing the metadata for the sequences.",
        type=str
    )
parser.add_argument(
        "-o", "--output_dir",
        help="Directory containing the sequences to submit.",
        type=str
    )
args = parser.parse_args()

dictionary = de_multiplex(
    fasta_file=args.fasta,
    output_dir=args.output_dir
)
