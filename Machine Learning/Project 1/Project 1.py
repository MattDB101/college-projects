import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn import metrics
from sklearn import model_selection
from sklearn import neighbors


csv = "movie_reviews.xlsx"



def split():
    
    df = pd.read_excel("movie_reviews.xlsx") 
    
    dfTrain = df.loc[df["Split"] == "train"]
    dfTest = df.loc[df["Split"] == "test"]
    
    trainingData = dfTrain["Review"]
    trainingLabels = dfTrain["Sentiment"]
    testingData = dfTest["Review"]
    testingLabels = dfTest["Sentiment"]

    #print(f"Positive reviews in the training set: {trainingLabels.value_counts()["positive"]}")
    #print(f"Negative reviews in the training set: {trainingLabels.value_counts()["negative"]}")
    #print(f"Positive reviews in the evaluation set: {testingLabels.value_counts()["positive"]}")
    #print(f"Negative reviews in the evaluation set: {testingLabels.value_counts()["negative"]}")
    
    return trainingData, trainingLabels, testingData, testingLabels



def extract(trainingData, minLen, minCount):
    trainingData = trainingData.replace("[^a-zA-Z0-9 ]", "", regex=True) # Remove non-alphanumeric characters.
    trainingData = trainingData.str.lower()
    trainingData = trainingData.str.split(" ")
    
    #print (pd.value_counts(np.hstack(trainingData))) # numpy solution
    #print (pd.Series([y for x in trainingData for y in x]).value_counts()) # pandas only solution
    
    occList = pd.value_counts(np.hstack(trainingData)).rename_axis("Word").reset_index(name="Occurrences") # horizontaly stack then count the unique values, create a new df with labels Word & Occurrences
    occList = occList[occList.Occurrences >= minCount] # drop rows where the count is less than specified
    occList = occList[occList["Word"].str.len() >= minLen] # drop rows where the word length is less than specified
    
    print(occList)
    
    return occList["Word"]



def countReviews(reviews, extractedWords):
    
    wordDict = {}
    
    for word in extractedWords:
        wordDict[word] = 0
       
        for review in reviews["Review"]:
            if " " + word + " " in review:
                #print(f"{word}: {review}")
                wordDict[word]+=1
                
    #print(wordDict)

    return wordDict



def calculateLikelihoods(positiveReviewWords, positiveReviewsCount, negativeReviewsWords, negativeReviewsCount):
    priorPos = positiveReviewsCount / (positiveReviewsCount + negativeReviewsCount) # calculate priors
    priorNeg = negativeReviewsCount / (positiveReviewsCount + negativeReviewsCount) # calculate priors
    
    wordsPosLikelihood = {}
    wordsNegLikelihood = {}
    

    for word in positiveReviewWords: # how many SENTIMENT reviews the word appears in, divided by the total count of SENTIMENT reviews.
        wordsPosLikelihood[word] = (positiveReviewWords[word] + 1) / (positiveReviewsCount + (1 * 2))

    for word in negativeReviewsWords:
        wordsNegLikelihood[word] = (negativeReviewsWords[word] + 1) / (negativeReviewsCount + (1 * 2))

    return wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg
    
    
     
def predict(review, wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg):

    logLikelihoodPos = 0
    logLikelihoodNeg = 0

    for word in review.lower().split():
        if word in wordsPosLikelihood.keys():
            logLikelihoodPos = logLikelihoodPos + math.log((wordsPosLikelihood[word]))
            
        if word in wordsNegLikelihood.keys():
            logLikelihoodNeg = logLikelihoodNeg + math.log((wordsNegLikelihood[word]))
        
    if logLikelihoodPos - logLikelihoodNeg > math.log(priorNeg) - math.log(priorPos):
        return "positive"
    else:
        return "negative"



def evaluate(trainingData, trainingLabels, testingData, testingLabels):
    numSplits = 5
    meanAccuracyList = []
    
    kf = model_selection.StratifiedKFold(n_splits=numSplits, shuffle=True)
    
    for k in range(1,11):
        accuracy = 0
        for train_index, test_index in kf.split(trainingData, trainingLabels): 
            extractedWords = extract(trainingData.iloc[train_index], k, minCount)
            trainingReviews = trainingData.iloc[train_index].to_frame().join(trainingLabels.iloc[train_index]) #create a df from the two training series reviews and sentiment to link a review to it's sentiment
            positiveTrainingReviews = trainingReviews[trainingReviews["Sentiment"] == "positive"] # take positive rows
            negativeTrainingReviews = trainingReviews[trainingReviews["Sentiment"] == "negative"] # take negative rows
            countPos = countReviews(positiveTrainingReviews, extractedWords) # task 3
            countNeg = countReviews(negativeTrainingReviews, extractedWords) # task 3

            wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg = calculateLikelihoods(countPos, trainingLabels.value_counts()["positive"], countNeg, trainingLabels.value_counts()["negative"])
            prediction = []
            for review in trainingData.iloc[test_index]:
                prediction.append(predict(review, wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg))
            
            accuracy += metrics.accuracy_score(trainingLabels.iloc[test_index], prediction)
            print(f"MinLen: {k}, Accuracy: {metrics.accuracy_score(trainingLabels.iloc[test_index], prediction)} \n")
    
        meanAccuracy = accuracy / numSplits
        meanAccuracyList.append(meanAccuracy)
        print(f"Mean Accuracy: {meanAccuracy}")
        
    print(meanAccuracyList)
    print(f"Best: {max(meanAccuracyList)} MinLen: {meanAccuracyList.index(max(meanAccuracyList))+1}" )

    extractedWords = extract(trainingData, meanAccuracyList.index(max(meanAccuracyList))+1, minCount) # task 2
    trainingReviews = trainingData.to_frame().join(trainingLabels) #create a df from the two training series reviews and sentiment to link a review to it's sentiment
    positiveTrainingReviews = trainingReviews.loc[trainingReviews["Sentiment"] == "positive"] # take positive rows
    negativeTrainingReviews = trainingReviews.loc[trainingReviews["Sentiment"] == "negative"] # take negative rows
    countPos = countReviews(positiveTrainingReviews, extractedWords) # task 3
    countNeg = countReviews(negativeTrainingReviews, extractedWords)

    wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg = calculateLikelihoods(countPos, trainingLabels.value_counts()["positive"], countNeg, trainingLabels.value_counts()["negative"])

    prediction = []
    for review in testingData:
        prediction.append(predict(review, wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg)) 
        

    confusion = metrics.confusion_matrix(testingLabels, prediction)
    
    print(confusion)
    tp = (confusion[0,0] / np.sum(confusion)) * 100
    fp = (confusion[0,1] / np.sum(confusion)) * 100
    fn = (confusion[1,0] / np.sum(confusion)) * 100
    tn = (confusion[1,1] / np.sum(confusion)) * 100
    
    print(f"true positive {round(tp, 2)}%")
    print(f"false positive {round(fp, 2)}%")
    print(f"true negative {round(tn, 2)}%")
    print(f"false negative {round(fn, 2)}%")
    
    accuracy = metrics.accuracy_score(testingLabels, prediction)
    print(f"accuracy: {accuracy}")

    
minLen = 4
minCount = 1000

trainingData, trainingLabels, testingData, testingLabels = split() # task 1

extractedWords = extract(trainingData, minLen, minCount) # task 2

trainingReviews = trainingData.to_frame().join(trainingLabels) #create a df from the two training series reviews and sentiment to link a review to it's sentiment
testingReviews = testingData.to_frame().join(testingLabels) #create a df from the two training series reviews and sentiment to link a review to it's sentiment
frames = [trainingReviews, testingReviews]
allReviews = pd.concat(frames)
positiveTrainingReviews = trainingReviews.loc[trainingReviews["Sentiment"] == "positive"] # take positive rows
negativeTrainingReviews = trainingReviews.loc[trainingReviews["Sentiment"] == "negative"] # take negative rows
#print(allReviews)
#print(positiveTrainingReviews)
#print(negativeTrainingReviews)

countPos = countReviews(positiveTrainingReviews, extractedWords) # task 3
countNeg = countReviews(negativeTrainingReviews, extractedWords)
#print(f"Positive: {countPos}")
#print(f"Negative: {countNeg}")

wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg = calculateLikelihoods(countPos, trainingLabels.value_counts()["positive"], countNeg, trainingLabels.value_counts()["negative"])
#print(wordsPosLikelihood)
#print(wordsNegLikelihood)

userReview = "This film was awful, the story was confusing and the actors were terrible"

prediction = predict(userReview, wordsPosLikelihood, wordsNegLikelihood, priorPos, priorNeg)

evaluate(trainingData, trainingLabels, testingData, testingLabels)







