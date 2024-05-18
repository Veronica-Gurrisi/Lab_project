#!/bin/bash

input_file="clean_msa_kunitz.aln-clustalw"  # Replace with your actual input file name
output_file="final_msa_kunitz.aln-clustalw"  # Replace with your desired output file name

# Split the input file into two parts
split -l 23 $input_file temp_part_

# Use awk to format and combine the sequences
awk '
NR==FNR {
    seq_id[FNR] = $1
    seq[FNR] = $2
    next
}
{
    seq[FNR] = seq[FNR] $2
}
END {
    for (i = 1; i <= FNR; i++) {
        print ">" seq_id[i]
        print seq[i]
    }
}' temp_part_aa temp_part_ab > $output_file

# Clean up temporary files
rm temp_part_aa temp_part_ab
