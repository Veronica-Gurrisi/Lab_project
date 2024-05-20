### Scripts

This folder includes all necessary scripts to preprocess data, perform 3D structural alignments, build the HMM model, and validate the results. Key scripts include:

- cross_val.sh: bash script to run the 5-fold CV. This script represents the pipeline for analyzing biological sequence data and for evaluating the performance of the HMM and follows these steps:

### 1. Positive Dataset Processing:
Randomize and split the IDs of positive sequences. Create subsets of positive sequences. Run a sequence search algorithm (hmmsearch) on each subset. Store the results in separate files.

### 2. Negative Dataset Processing:
Extract negative sequences from a larger dataset. Randomize and split the IDs of negative sequences. Create subsets of negative sequences. Run hmmsearch on each subset. Adjust the results and merge them into combined files.

### 3. Performance Analysis:
Loop through each combined result file. Run a Python script (Performance.py) with different threshold values to evaluate the performance. Generate a graphical representation of the performance. Determine the best threshold value using another Python script (best_mcc.py). Run Performance.py again on corresponding files with the best threshold value. Output the final performance metrics, including Average MCC (Matthews Correlation Coefficient) and Average F1 score. Overall, this script automates the process of evaluating the performance of a protein sequence classification algorithm using a combination of positive and negative datasets, employing a sequence search algorithm (hmmsearch), and assessing its effectiveness using metrics like MCC and F1 score. It's a comprehensive workflow for bioinformatics analysis.

- select_fasta.py: the script reads a sequence file in FASTA format and extracts sequences based on a list of identifiers provided in another file.
- Performance.py: this script reads predictions from a file, computes performance metrics such as the confusion matrix, overall accuracy (Q2), Matthews Correlation Coefficient (MCC), and F1 score, and then outputs these metrics. Steps:
### 1. Reading Data (get_data):
Reads prediction data from a file. Each line contains information about a sequence, including its ID, predicted e-value, and label. Converts the e-value to a float and the label to an integer.

### 2. Confusion Matrix Calculation (compute_cm):
Computes the confusion matrix based on predicted values and labels. Determines true positives (TP), true negatives (TN), false positives (FP), and false negatives (FN). Stores false positive and false negative IDs separately.

### 3. Accuracy Calculation (get_accuracy):
Calculates the overall accuracy of the model based on the confusion matrix.

### 4. Matthews Correlation Coefficient Calculation (get_mcc):
Calculates the Matthews Correlation Coefficient, a measure of the quality of binary classifications. Takes into account TP, TN, FP, and FN.

### 5. F1 Score Calculation (get_f1):
Calculates the F1 score, which is the harmonic mean of precision and recall. Takes into account TP, TN, FP, and FN.

### 6. Main Function:
Reads the prediction file from the command-line arguments. Optionally, accepts a threshold value for prediction. Computes confusion matrix and other metrics. Prints the results including TP, TN, FP, FN, accuracy, MCC, and F1 score. Additionally, if the prediction file name contains "com", it only prints essential metrics without false positives and false negatives.

- best_mcc.py: it reads a performance evaluation file, extracts Matthews Correlation Coefficient (MCC) values and their corresponding thresholds, identifies the best threshold that maximizes the MCC, and plots the MCC values against the thresholds.

- script.sh: bash script needed to modify the output file of MSA from MUSCLE in order to clean it, removing any white lines and gaps, so to use the final modified file for building the model.
