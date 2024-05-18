#!/bin/bash

# all the output files are generated in the current directory 


# POSITIVE 
# Step 1: Randomize and split the IDs
sort -R selected.ids > r1.selected.ids
split -d -a 1 -n 5 r1.selected.ids pos_subset_

# Step 2: Create the 5 positive fasta files
for i in {0..4}; do
    python3 select_fasta.py  pos_subset_$i  bpti_pos_selected.fasta  > msa_pos_subset_$i.fasta
done

# Step 3: Create 5 subsets that are iteratively excluding one set
for i in {0..4}; do
    # Initialize prefix variable
    pref=""

    # Loop to construct prefix without i
    for j in {0..4}; do
        if [ $j -ne $i ]; then
            pref="${pref}${j}"
        fi
    done

    # Loop to concatenate subset files
    for j in {0..4}; do 
        cat msa_pos_subset_$j.fasta >> msa_pos_subset_${pref}.fasta
    done

    hmmsearch -Z 1 --domZ 1 --max --noali --tblout msa_combined_pos_hmm_${pref}.out cut_msa_kunitz.hmm msa_pos_subset_${pref}.fasta 
    grep -v "#" msa_combined_pos_hmm_${pref}.out |awk '{print $1"\t"$8"\t1"}' > msa_com_set_${pref}.txt



    # Apply hmmsearch to each file
    hmmsearch -Z 1 --domZ 1 --max --noali --tblout msa_hmmsearch_pos_$i.out cut_msa_kunitz.hmm msa_pos_subset_$i.fasta
    grep -v "#" msa_hmmsearch_pos_$i.out |awk '{print $1"\t"$8"\t1"}' > msa_set_$i.txt

done


# NEGATIVE
# Step 1: Randomize and split the IDs
zcat -f all_nobpti.fasta | grep "^>" | cut -d  "|" -f 2 > negative.ids
sort -R negative.ids > negatives_r1.ids
split -d -a 1 -n 5 negatives_r1.ids neg_subset_

# Step 2: Create the 5 negative fasta files
for i in {0..4}; do
    python3 select_fasta.py  neg_subset_$i  <(zcat -f all_nobpti.fasta) 2   > msa_neg_subset_$i.fasta
done

# Step 3: Create 5 subsets that are iteratively excluding one set
for i in {0..4}; do
    # Initialize prefix variable
    pref=""

    # Loop to construct prefix without i
    for j in {0..4}; do
        if [ $j -ne $i ]; then
            pref="${pref}${j}"
        fi
    done

    # Loop to concatenate subset files
    for j in {0..4}; do 
        cat msa_neg_subset_$j >> msa_neg_subset_${pref}.ids 
        cat msa_neg_subset_$j.fasta >> msa_neg_subset_${pref}.fasta
        
    done

    # Apply hmmsearch to each combined file
    hmmsearch -Z 1 --domZ 1 --max --noali --tblout msa_combined_neg_hmm_${pref}.out cut_msa_kunitz.hmm msa_neg_subset_${pref}.fasta 

    grep -v "#" msa_combined_neg_hmm_${pref}.out |awk '{print $1"\t"$8"\t0"}' > msa_tmp_neg_${pref}.txt
    comm -23 <(sort msa_neg_subset_${pref}.ids ) <(cut -f 1 msa_tmp_neg_${pref}.txt | sort)| awk '{print $1"\t10\t0"}' >> msa_tmp_neg_${pref}.txt
    cat msa_tmp_neg_${pref}.txt >> msa_com_set_${pref}.txt


    # Apply hmmsearch to each file
    hmmsearch -Z 1 --domZ 1 --max --noali --tblout msa_hmmsearch_neg_$i.out cut_msa_kunitz.hmm msa_neg_subset_$i.fasta
    grep -v "#" msa_hmmsearch_neg_$i.out |awk '{print $1"\t"$8"\t0"}' > msa_tmp_neg_$i.txt
    comm -23 <(sort neg_subset_$i) <(cut -f 1 msa_tmp_neg_$i.txt | sort)| awk '{print $1"\t10\t0"}' >> msa_tmp_neg_$i.txt
    cat msa_tmp_neg_$i.txt >> msa_set_$i.txt


done


# Step 4: Analysis of the performance
for file in msa_com_set_*.txt; do
    out="${file%.txt}.res"  # Substitute .txt with .res

    # Run Performance.py on the current file for different threshold values
    # for i in $(seq 1 15); do
    #     python3 Performance.py "$file" 1e-$i >> "$out"
    # done
    for i in $(seq 1 15); do python3 Performance.py "$file" 1e-$i; done > "$out"

    image="${file%.txt}.png"  # Corrected assignment

    th=$(python3 best_mcc.py "$out" "$image")

    # Run Performance.py on corresponding files with the best threshold value
    for i in {0..4}; do
        if ! grep -q $i <<< $file; then
            python3 Performance.py "msa_set_$i.txt" "$th" >> msa_out_best.txt
        fi
    done
done

# Step 5: Final performance
grep -v ">" msa_out_best.txt |grep -v ":" | awk -F ',' '{split($6, mcc, "="); sum += mcc[2]; count++} END {print "Average MCC:", sum/count}'
grep "F1 score" msa_out_best.txt | awk -F ': ' '{sum += $2; count++} END {print "Average F1:", sum/count}'
