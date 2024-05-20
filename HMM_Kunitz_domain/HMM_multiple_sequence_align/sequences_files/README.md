### Here's a description for each of the files contained in this section: 

- clean_msa_kunitz.aln-clustalw: This file is obtained by downloading the output from MUSCLE, with the multiple sequence alignment

- cut_msa_kunitz: This file is used as input to make the model, generated from the previous one by excluding gaps to obtain better results.
  
- cut_msa_kunitz_3d.hmm: this is the constructed HMM for the Kunitz-type protease inhibitor domain.

- bpti_pos_selected.fasta: This file contains the positive set of the benchmark set.

- negatives_r1.ids: This file contains the identifiers for the negative set of the benchmark set, which consists of proteins without the domain of interest.

- msa_com_set_*.txt: These files represent combined sets containing both positive and negative data, labeled accordingly (1 if part of the positive set, 0 if negative). They include the e-value and the ID and are used for training the model.

- msa_set_*.txt: These files represent single sets with both positive and negative data used for testing. They also contain the e-value, ID, and label.
