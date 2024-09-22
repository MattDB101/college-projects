import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import model_selection



def split():
    csv = "energy_performance.csv"
    df = pd.read_csv(csv) 
    
    features = df.drop(['Heating load', 'Cooling load'], axis=1).to_numpy()
    targets = df[['Heating load', 'Cooling load']].to_numpy()
    
    heatTarget = targets[:, 0]
    coolTarget = targets[:, 1]

    minHeat = heatTarget.min()
    maxHeat = heatTarget.max()
    minCool = coolTarget.min()
    maxCool = coolTarget.max()

    print(f"Min. Heating: {minHeat}")
    print(f"Max. heating: {maxHeat}")
    print(f"Min. cooling: {minCool}")
    print(f"Max. cooling: {maxCool}")

    return features, targets, df



def calculate_model_function(deg, features, p):
    result = np.zeros(features.shape[0])
    t = 0
    for n in range(deg + 1):
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    for l in range(n + 1):
                        for m in range(n + 1):
                            for o in range(n + 1):
                                for q in range(n + 1):
                                    for r in range(n + 1):
                                        if i + j + k + l + m + o + q + r == n:
                                            result += p[t] * (features[:, 0] ** i) * (features[:, 1] ** j) * (features[:, 2] ** k) * (features[:, 3] ** l) * (features[:, 4] ** m) * (features[:, 5] ** o) * (features[:, 6] ** q) * (features[:, 7] ** r) 
                                            t += 1
    return result



def num_coefficients_8(d):
    t = 0
    for n in range(d + 1):
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    for l in range(n + 1):
                        for m in range(n + 1):
                            for o in range(n + 1):
                                for p in range(n + 1):
                                    for q in range(n + 1):
                                        if i + j + k + l + m + o + p + q == n:
                                            t += 1
    return t



def linearize(deg, features, p0):
    f0 = calculate_model_function(deg, features, p0) # Task 3.1 Start by calculcating the model function for the first time with the starting parameters
    J = np.zeros((len(f0), len(p0))) # define the jacobian ladder to be a matrix of 0's that is the of the dimmensions required
    epsilon = 1e-6  # define the starting epsilon
    for i in range(len(p0)): # loop for the width of the ladder (aka the length of p0)
        p0[i] += epsilon # add the epsilon's value to the element in index i of list p0
        fi = calculate_model_function(deg, features, p0) # Task 3.1 Re-calculate the model function again, this time passing the updated p0 list as a parameter
        p0[i] -= epsilon # subtract the epsilon that was previously added in p0's index i
        di = (fi - f0) / epsilon # Task 3.2 calculate the partial derivative using the new model function, original model function and the epsilon
        J[:, i] = di # add the partial derivative to the Jacobian ladder
    return f0, J



def calculate_update(y, f0, J):
    l = 1e-2 # regularisation factor
    N = np.matmul(J.T, J) + l * np.eye(J.shape[1]) # Task 4.1 calculate the normal equation matrix with np.matmul(J.T, J), it's regularised and adding the regularisation factor multiplied by np.eye(J.shape[1])
    r = y - f0 # Task 4.2 Calculate the residuals, the residual is the target vector and the model function output.It contains every training sample's difference from the model function
    n = np.matmul(J.T, r)  # We create the right hand side of the normal equation
    dp = np.linalg.solve(N, n) # solve to find the optimal paramter update
    return dp



def regression(deg, features, target):
    max_iter = 10
    p0 = np.zeros(num_coefficients_8(deg)) # Task 5.1 initialize the parameter vector to 0's
    for i in range(max_iter):
        f0, J = linearize(deg, features, p0) # get the model function and the jacobian ladder
        dp = calculate_update(target, f0, J) # get the figure required to preform the parameter vector update
        p0 += dp # Task 5.1 Update the parameter vector
    return p0 # Task 5.2 This will decrease the greatest on its first update, with each subsequent update being smaller and smaller the closer it gets to the local minimum
    # Task 5.3 Count the iterations required until the parameter vector and the parameter update are at a local minimum


def modelSelection():
    features, targets, df = split()
    heatTarget = targets[:, 0]
    coolTarget = targets[:, 1]
    
    kf1 = model_selection.KFold(n_splits=5, shuffle=True) # Setup two cross-validation procedures, one for the heat loads and one for cooling loads [1 point].
    kf2 = model_selection.KFold(n_splits=5, shuffle=True)
    
    heatDiffPerDegree = []
    coolDiffPerDegree = []

    for polynomialDeg in range(0, 3):
        
        heatDiffAllSplits = []
        coolDiffAllSplits = []

        for train_index, test_index in kf1.split(df): 
            
            trainingFeatures = features[train_index]
            testingfeatures = features[test_index]
            heatTrainingTarget = heatTarget[train_index]
            heatTestingTarget = heatTarget[test_index]

            p0 = regression(polynomialDeg, trainingFeatures, heatTrainingTarget)
            heatingTestPrediction = calculate_model_function(polynomialDeg, testingfeatures, p0)    
            heatingDifference = np.absolute(heatingTestPrediction - heatTestingTarget) # Calculate the difference between the predicted target and the 
            heatDiffAllSplits = np.concatenate((heatDiffAllSplits, heatingDifference), axis=0) # actual target for the test set in each cross-validation fold [1 point]
        
        heatDiffPerDegree.append(np.mean(heatDiffAllSplits)) # output the mean of absolute differences across all folds for 
        print(f"Mean heating load absolute differences across all splits where degree = {polynomialDeg}: {np.mean(heatDiffAllSplits)}")
         
         
        for train_index, test_index in kf2.split(df): 
            
            trainingFeatures = features[train_index]
            testingfeatures = features[test_index]
            coolTrainingTarget = coolTarget[train_index]
            coolTestingTarget = coolTarget[test_index]
            
            p1 = regression(polynomialDeg, trainingFeatures, coolTrainingTarget)
            coolingTestPrediction = calculate_model_function(polynomialDeg, testingfeatures, p1)
            coolingDifference = np.absolute(coolingTestPrediction - coolTestingTarget)
            coolDiffAllSplits = np.concatenate((coolDiffAllSplits, coolingDifference), axis=0)
            
        coolDiffPerDegree.append(np.mean(coolDiffAllSplits)) # both the heating load estimation as well as the cooling load estimation [2 points].
        print(f"Mean cooling load absolute differences across all splits where degree = {polynomialDeg}: {np.mean(coolDiffAllSplits)}")
        
    heatingBestDegree = heatDiffPerDegree.index(min(heatDiffPerDegree))
    coolingBestDegree = coolDiffPerDegree.index(min(coolDiffPerDegree))

    print(f"Optimal degree for heating loads: {heatingBestDegree}") # evaluate polynomial degrees ranging between 0 and 2 to determine the optimal 
    print(f"Optimal degree for cooling loads: {coolingBestDegree}") # degree for the model function for both the heating as well as the cooling loads [2 points].
    
    evaluate(features, heatTarget, coolTarget, heatingBestDegree, coolingBestDegree, heatDiffPerDegree, coolDiffPerDegree)



def evaluate(features, heatTarget, coolTarget, heatingBestDegree, coolingBestDegree, heatDiffPerDegree, coolDiffPerDegree):
    p0 = regression(heatingBestDegree, features, heatTarget) # estimate the model parameters for both the heating loads as well as the cooling loads
    p1 = regression(coolingBestDegree, features, coolTarget) # using the selected optimal model function as determined in task 6 [1 point].
    
    heatingBestDegreePrediction = calculate_model_function(heatingBestDegree, features, p0) # Calculate the predicted heating and cooling loads using the estimated 
    coolingBestDegreePrediction = calculate_model_function(coolingBestDegree, features, p1) # model parameters for the entire dataset [1 point].

    plt.figure()
    plt.scatter(heatingBestDegreePrediction, heatTarget, label='Prediction')
    plt.plot([min(heatTarget), max(heatTarget)], [min(heatTarget), max(heatTarget)],  label='Actual')
    plt.xlabel("Heating Predicted")
    plt.ylabel("Heating Actual")
    plt.legend()
    plt.figure()
    
    plt.scatter(coolingBestDegreePrediction, coolTarget, label='Prediction')
    plt.plot([min(coolTarget), max(coolTarget)], [min(coolTarget), max(coolTarget)],  label='Actual')
    plt.xlabel("Cooling Predicted")
    plt.ylabel("Cooling Actual")
    plt.legend()
    plt.show() # Plot the estimated loads against the true loads for both the heating and the cooling case [2 points].
    
    heatingDifference = np.mean(np.absolute(heatingBestDegreePrediction - heatTarget)) 
    coolingDifference = np.mean(np.absolute(coolingBestDegreePrediction - coolTarget))

    print(f"Heating load absolute differences estimated vs actual: {heatingDifference}") # Calculate and output the mean absolute difference between estimated 
    print(f"Cooling load absolute differences estimated vs actual: {coolingDifference}") # heating/cooling loads and actual heating/cooling loads [2 points].
    
    
    
modelSelection()



