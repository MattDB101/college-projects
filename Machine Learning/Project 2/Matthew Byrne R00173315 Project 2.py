import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn import neighbors, svm, tree, metrics, linear_model, model_selection
import time
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

csv = "product_images.csv"
df = pd.read_csv(csv) 


def split():
    
    labels = df["label"]
    featureVectors = df.drop("label", axis=1)

    sneakers = df.loc[df["label"] == 0].drop("label", axis=1) # seperate into sneakers only and drop label column
    boots = df.loc[df["label"] == 1].drop("label", axis=1) # seperate into boots only and drop label column
    countSneakers = len(sneakers)
    countBoots = len(boots)
    
    print(f"Count sneakers: {countSneakers}")
    print(f"Count boots: {countBoots}")
    
    plt.figure()
    plt.imshow(sneakers.iloc[0].to_numpy().reshape(28, 28))
    
    plt.figure()
    plt.imshow(boots.iloc[0].to_numpy().reshape(28, 28))
    
    #plt.show()

    return labels, featureVectors
    

def evaluate(data, target):
    
    def run():    
        prediction = 0
        trainingTimeList = []
        testingTimeList = []
        fold = 1
        
        kf = model_selection.KFold(n_splits=numSplits, shuffle=True) # create kfold selection
        trainingData, testingData, trainingTarget, testingTarget = model_selection.train_test_split(data, target, test_size=0.33)

        
        trainingData = pd.DataFrame(trainingData) # convert to df
        trainingTarget = pd.DataFrame(trainingTarget) # convert to df
        trainingData = trainingData.sample(n=n) # sample of size n
        indexes = trainingData.index # get indexes
        trainingTarget = trainingTarget.take(indexes) # use found indexes to get matching target
        
        trainingData = trainingData.to_numpy() # convert to numpy array
        trainingTarget = trainingTarget.to_numpy() # convert to numpy array
        
        for train_index, test_index in kf.split(trainingData, trainingTarget):
            if not sampling:
                if i == 0 or i == 3:
                    print(f"\n===== {classifiers[i]} fold: {fold} =====")
                if i == 2:
                    print(f"\n===== {classifiers[i]} k: {k} fold: {fold} =====")
                if i == 1:
                    print(f"\n===== {classifiers[i]} with Gamma value: {gamma} fold: {fold} =====")
                    
            if sampling:
                if i == 0 or i == 3:
                    print(f"\n===== {classifiers[i]} Sample Size: {n} fold: {fold} =====")
                if i == 2:
                    print(f"\n===== {classifiers[i]} Sample Size: {n} k: {k} fold: {fold} =====")
                if i == 1:
                    print(f"\n===== {classifiers[i]} Sample Size: {n} with Gamma value: {gamma} fold: {fold} =====")
          
            
            
            startTraining = time.time()
            clf.fit(trainingData[train_index], trainingTarget[train_index])
            endTraining = time.time()
            trainingRuntime = (endTraining - startTraining)
            trainingTimeList.append(trainingRuntime)
            
            startTesting = time.time()
            prediction = clf.predict(testingData)
            endTesting = time.time()
            testingRuntime = (endTesting - startTesting)
            testingTimeList.append(testingRuntime)
            
            print(f"Training Runtime: {trainingRuntime}")
            print(f"Testing Runtime: {testingRuntime}")
            print(f"Accuracy: {round(metrics.accuracy_score(testingTarget, prediction), 5)}")
            accuracyList.append(metrics.accuracy_score(testingTarget, prediction))
            fold+=1
                    
        confusion = metrics.confusion_matrix(testingTarget, prediction)
        print(confusion)
        tp = (confusion[0,0] / np.sum(confusion)) * 100
        fp = (confusion[0,1] / np.sum(confusion)) * 100
        fn = (confusion[1,0] / np.sum(confusion)) * 100
        tn = (confusion[1,1] / np.sum(confusion)) * 100
        
        print(f"true positive {round(tp, 2)}%")
        print(f"false positive {round(fp, 2)}%")
        print(f"true negative {round(tn, 2)}%")
        print(f"false negative {round(fn, 2)}%")
        print()
        print(f"-{classifiers[i]} Accuracies-")
        print(f"Min. Accuracy: {round(min(accuracyList), 5)}")
        print(f"Max. Accuracy: {round(max(accuracyList), 5)}")
        print(f"Mean Accuracy: {round(sum(accuracyList)/len(accuracyList), 5)}")
        print()
        if i == 1 and sampling == False:
            gammaResultsList.append(sum(accuracyList)/len(accuracyList))
       
        meanAccuracyList.append(sum(accuracyList)/len(accuracyList))
        print(f"-{classifiers[i]} Training Times (Per sample, n:{n})-")      
        print(f"Min. Training Time: {min(trainingTimeList)/n}s")
        print(f"Max. Training Time: {max(trainingTimeList)/n}s")
        print(f"Mean Training Time: {(sum(trainingTimeList)/n)/len(trainingTimeList)}s")
        print()
        print(f"-{classifiers[i]} Testing Times (Per sample, n:{n})-") 
        print(f"Min. Testing Time: {min(testingTimeList)/n}s")
        print(f"Max. Testing Time: {max(testingTimeList)/n}s")
        print(f"Mean Testing Time: {(sum(testingTimeList)/n)/len(testingTimeList)}s")
        

    
        return sum(trainingTimeList)/len(trainingTimeList), sum(testingTimeList)/len(testingTimeList)

    numSplits = 3
    classifiers = ["Perceptron", "SVM", "KNN", "Decision Tree"]
    samples = [1000, 2500, 5000, 7000]
    n=7000

    for i in range(4):
        bestGammas=[]
        list1 = []
        list2 = []
        sampling = False
        meanAccuracyList = []
        accuracyList = []
        
        if i == 0:
            clf = linear_model.Perceptron()
            run()
            print()
            print(f"Greatest accuracy of {classifiers[i]} occured on fold = {accuracyList.index(max(accuracyList)) + 1}") # Highest mean accuracy - finding best K
            print(f"Mean prediction accuracy for classifier {classifiers[i]}: {round(meanAccuracyList[0], 5)}") # Mean of all runs' means.
            sampling = True
            for sample in samples:
                n = sample
                sampleTrainingTime, sampleTestingTime = run()
                list1.append(sampleTrainingTime)
                list2.append(sampleTestingTime)
            plt.figure()
            plt.title("Perceptron classifier overall runtime when changing sample size")
            br1= np.arange(len(samples))
            br2= [x + 0.3 for x in br1]
            plt.bar(br1, list1, width= 0.3, label="Training Times")
            plt.bar(br2, list2, width= 0.3, label="Testing Times")
            plt.xticks([r + 0.15 for r in range(len(samples))], samples)
            plt.show()
            
        if i == 1:
            gammas = [1e-1, 1e-2, 1e-3]
            gammaResultsList = []
            for gamma in gammas:
                clf = svm.SVC(kernel="rbf", gamma=gamma)
                run()
            j=0
            while j < len(gammaResultsList):
                print(f"Mean Prediction Accuracy with Gamma of {gammas[j]}: {gammaResultsList[j]}")
    
                meanAccuracyList.append(sum(gammaResultsList)/len(gammaResultsList))
                j+=1
            print(f"Best gamma was: {gammas[gammaResultsList.index(max(gammaResultsList))]} with a value of: {max(gammaResultsList)}") # Need to take this result and use it in the sampling for SVM
            sampling = True
            clf = svm.SVC(kernel="rbf", gamma=gammas[gammaResultsList.index(max(gammaResultsList))])
            for sample in samples:
                n = sample
                sampleTrainingTime, sampleTestingTime = run()
                list1.append(sampleTrainingTime)
                list2.append(sampleTestingTime)
            plt.figure()
            plt.title(f"SVM classifier with Gamma of {gammas[gammaResultsList.index(max(gammaResultsList))]} overall runtime when changing sample size")
            br1= np.arange(len(samples))
            br2= [x + 0.3 for x in br1]
            plt.bar(br1, list1, width= 0.3, label="Training Times")
            plt.bar(br2, list2, width= 0.3, label="Testing Times")
            plt.xticks([r + 0.15 for r in range(len(samples))], samples)
            plt.show()

        if i == 2:
            kResultsList = []
            for k in range(1, 5):
                clf = neighbors.KNeighborsClassifier(n_neighbors=k)
                run()
            print(meanAccuracyList)
            print(f"Greatest accuracy of {classifiers[i]} occured on k = {meanAccuracyList.index(max(meanAccuracyList)) + 1} with a value of: {max(meanAccuracyList)}") # Highest mean accuracy - finding best K
            print(f"Mean of all k's prediction accuracy for classifier {classifiers[i]}: {round(sum(meanAccuracyList)/len(meanAccuracyList), 5)}") # Mean of all runs' means.
            sampling = True
            clf = neighbors.KNeighborsClassifier(n_neighbors=meanAccuracyList.index(max(meanAccuracyList))+1)
            for sample in samples:
                n = sample
                sampleTrainingTime, sampleTestingTime = run()
                list1.append(sampleTrainingTime)
                list2.append(sampleTestingTime)
            plt.figure()
            plt.title(f"KNN classifier with K of {meanAccuracyList.index(max(meanAccuracyList)) + 1} overall runtime when changing sample size")
            br1= np.arange(len(samples))
            br2= [x + 0.3 for x in br1]
            plt.bar(br1, list1, width= 0.3, label="Training Times")
            plt.bar(br2, list2, width= 0.3, label="Testing Times")
            plt.legend()
            plt.xticks([r + 0.15 for r in range(len(samples))], samples)
            plt.show()
           
        if i == 3:
            clf = tree.DecisionTreeClassifier()
            run()
            print()
            print(f"Greatest accuracy of {classifiers[i]} occured on fold = {accuracyList.index(max(accuracyList)) + 1}") # Highest mean accuracy - finding best K
            print(f"Mean prediction accuracy for classifier {classifiers[i]}: {round(meanAccuracyList[0], 5)}") # Mean of all runs' means.
            sampling = True
            for sample in samples:
                n = sample
                sampleTrainingTime, sampleTestingTime = run()
                list1.append(sampleTrainingTime)
                list2.append(sampleTestingTime)
            plt.figure()
            plt.title("Decision Tree classifier overall runtime when changing sample size")
            br1= np.arange(len(samples))
            br2= [x + 0.3 for x in br1]
            plt.bar(br1, list1, width= 0.3, label="Training Times")
            plt.bar(br2, list2, width= 0.3, label="Testing Times")
            plt.xticks([r + 0.15 for r in range(len(samples))], samples)
            plt.show()



        
labels, featureVectors = split()

featureVectors = featureVectors.to_numpy() # convert to numpy array
labels = labels.to_numpy() # convert to numpy array

evaluate(featureVectors, labels)