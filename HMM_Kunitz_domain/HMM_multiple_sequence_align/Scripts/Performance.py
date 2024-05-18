#!/usr/bin/env python3
import sys
import numpy as np

# def get_data(predfile): 
#     """Reading the info has to identify to each seq the e-value and the label"""
#     preds = [] #output = list of lists
#     with open(predfile, "r") as f:
#         for line in f:
#             v = line.rstrip().split() #v = [seqID, e-value, label]
#             v[1] = float(v[1]) #e-value
#             v[2] = int(v[2]) #label -> we use int instead of bool because is useful after for the confision matrix (we use them as indexes to access the matrix)
#             preds.append(v)
#     return preds

def get_data(predfile): 
    """Reading the info has to identify to each seq the e-value and the label"""
    preds = [] #output = list of lists
    with open(predfile, "r") as f:
        c = 0
        for line in f:
            c += 1
            v = line.rstrip().split() #v = [seqID, e-value, label]
            if len(v) >= 3:  # Ensure the line has at least three elements
                v[0] = str(v[0])
                v[1] = float(v[1]) #e-value
                v[2] = int(v[2]) #label -> we use int instead of bool because is useful after for the confision matrix (we use them as indexes to access the matrix)
                preds.append(v)
            else:
                print("yes")
                print(line, c)
    return preds  
    
#CONFUSION MATRIX (CM)
def compute_cm(preds,th=0.5): 
    cm = np.zeros((2,2)) #matrix 2x2
    fp_ids = []
    fn_ids = []
    #we have to go line by line and assign the correct values
    for pred in preds: #we mantein 0 and 1 because these are also the indexes of the line and the col of the matrix
        p=0  #prediction is 0 by default
        if pred[1]<=th: p=1 #if e-value lower than the threshold the prediction is positive
        #the sign depends on what is the variable that we use to do the classification, in our case the best case is the e-value as lower as possible, so we use <=
        cm[p][pred[2]]+=1 #we identify the cell [prediction][label=reality] and we add one case
        if p == 0 and pred[2] == 1: # false pos
            fp_ids.append(pred[0]) # append IDs
        elif p ==1 and pred[2] == 0: # false neg
            fn_ids.append(pred[0])

    return cm, fn_ids, fp_ids #return the confusion matrix TN, FN, FP, TP
        
        
#OVERALL ACCURACY        
def get_accuracy(cm): #(TN+TP)/(TN+TP+FN+FP) = (TN+TP)/tot
    q2 = float((cm[0][0]+cm[1][1])/np.sum(cm))
    #print('Q2=', q2, 'N=', np.sum(cm))
    return q2


#MATTHEW CORRELATION COEFFICIENT -> if the dataset is not balanced 
def get_mcc(cm): #(TP*TN-FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    tp = cm[1][1]
    tn = cm[0][0]
    fp = cm[0][1]
    fn = cm[1][0]
    mcc = (tp*tn-fp*fn)/np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    #at the denominator all the possible combinations between true and false
    return mcc

#F1 SCORE
def get_f1(cm): # 2 * (precision * recall) / (precision + recall)
    tp = cm[1][1]
    tn = cm[0][0]
    fp = cm[0][1]
    fn = cm[1][0]
    

    if tp + fp == 0 or tp + fn == 0:
        return 0.0  # Avoid division by zero

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    if precision + recall == 0:
        return 0.0  # Avoid division by zero

    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score



if __name__=="__main__":
    predfile = sys.argv[1]
    #to do the optimization we have to compare the performance with different thresholds
    preds = get_data(predfile)
    #print(preds)
    if len(sys.argv)<2: 
        cm_complete = compute_cm(preds)
        
    else:
        th = float(sys.argv[2]) #float because it is an e-value
        cm_complete = compute_cm(preds,th)
        
    cm = cm_complete[0]
    fp = cm_complete[2]
    fn = cm_complete[1]
    q2 = get_accuracy(cm)
    mcc = get_mcc(cm)
    f1 = get_f1(cm)

    if "com" in sys.argv[1]:
        print(">" + " " + str(th))
        print('TP=' + str(cm[1][1]) + "," + 'TN=' + str(cm[0][0]) + "," + 'FN=' + str(cm[1][0]) + "," + 'FP=' + str(cm[0][1]) + "," + 'Q2=' + str(q2) + "," + 'MCC=' + str(mcc))
    else:
        print(">" + sys.argv[1] + " " + str(th))
        print('TP=' + str(cm[1][1]) + "," + 'TN=' + str(cm[0][0]) + "," + 'FN=' + str(cm[1][0]) + "," + 'FP=' + str(cm[0][1]) + "," + 'Q2=' + str(q2) + "," + 'MCC=' + str(mcc))
        print("false negative:", fn)
        print("false positive:", fp)
        print("F1 score:", f1)


