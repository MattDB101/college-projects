import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import model_selection
from sklearn import neighbors

def cross_validation():
    titanic = pd.read_csv("titanic.csv")

    titanic["Sex"] = titanic["Sex"].map({"male":0,"female":1})    

    data = titanic[["Sex","Pclass"]].to_numpy() #train data
    target = titanic["Survived"].to_numpy() # train labels
    
    survivors = len(data[target==1])
    casulties = len(data[target==0])
                
    kf = model_selection.StratifiedKFold(n_splits=5, shuffle=True)
    for k in range(1,11):
        true_casulties = []
        true_survivors= []
        false_casulties = []
        false_survivors= []
        for train_index, test_index in kf.split(data, target): # splits dataset
            clf = neighbors.KNeighborsClassifier(n_neighbors=k)
            clf.fit(data[train_index,:], target[train_index])
            predicted_labels = clf.predict(data[test_index,:])
            
            C = metrics.confusion_matrix(target[test_index], predicted_labels)
            
            true_casulties.append(C[0,0])
            false_survivors.append(C[0,1])
            false_casulties.append(C[1,0])
            true_survivors.append(C[1,1])            
            
            
        
        print("k =",k)
        print("True casulties:", np.sum(true_casulties))
        print("True survivors:", np.sum(true_survivors))
        print("False casulties:", np.sum(false_casulties))
        print("False survivors:", np.sum(false_survivors))
        print()
                    
    


    
    
def main():
    cross_validation()
    
main()
