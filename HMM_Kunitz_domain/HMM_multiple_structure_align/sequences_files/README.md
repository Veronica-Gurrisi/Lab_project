### Here's a description for each of the files contained in this section: 

- PDB_report.csv: This file is a custom report generated from an advanced search in the Protein Data Bank (PDB). It contains information on the 21 selected proteins that were used in the study. The columns included in this file are:

    PDB ID: The unique identifier for each protein structure in the PDB,
    Amino Acid Sequence: The sequence of amino acids for the protein,
    Chain Identifier (Auth Asym ID): The identifier for the specific chain of the protein,
    Polymer Entity Entry ID: The identifier for the polymer entity within the PDB entry.
  
- list_pdb.txt: This file is generated from the PDB_report.csv file using a series of command-line operations. It contains identifiers for the protein sequences used in the study. It is uploaded in PDBeFold to carry out the 3D structural alignment.

- clean_kunitz_3d.ali: This file is obtained by downloading the output for PDBeFold, manipulated for better visualization. It represents the multiple sequence alignment derived from the multiple structure alignment.

- cut_kunitz_3d.ali: This file is used as input to make the model, generated from the previous one by excluding gaps to obtain better results.
  
- cut_kunitz_3d.hmm: output of the HMM 

- bpti_pos_selected.fasta: This file contains the positive set of the benchmark set. It likely includes sequences that are known to belong to a certain protein family or class.

- negatives_r1.ids: This file contains the identifiers for the negative set of the benchmark set, which consists of proteins without the domain of interest.

- com_set_*.txt: These files represent combined sets containing both positive and negative data, labeled accordingly (1 if part of the positive set, 0 if negative). They include the e-value and the ID and are used for training the model.

- set_*.txt: These files represent single sets with both positive and negative data used for validation. They also contain the e-value, ID, and label.

