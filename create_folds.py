#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import sys, os
from Dataset import Dataset

def CreateDatasetDirectory(datasetParentDirectory, dataset):
 if not os.path.exists(datasetParentDirectory):
  os.makedirs(datasetParentDirectory);
 pathToDataset = datasetParentDirectory + "/" + dataset.name;
 if not os.path.exists(pathToDataset):
  os.makedirs(pathToDataset)
 dataset.pathToFiles = datasetParentDirectory;
 return pathToDataset;

def Parse(dataset, folds, parents, ess, root_directory = None):
 print "Parsing dataset:", dataset.name, "into", folds, "folds.";
 datasetDirectory = "datasetFolds_" + str(parents) + "_" + str(ess);
 if not root_directory:
  datasetDirectory = root + datasetDirectory

 datasetPath = CreateDatasetDirectory(datasetDirectory, dataset);
 trainingFiles = [];
 validationFiles = [];
 for training, validation in dataset.KFoldGenerator(folds):
  trainingFiles.append(training.WriteToFile(datasetPath));
  validationFiles.append(validation.WriteToFile(datasetPath));
 print "Finished parsing.";
 return datasetPath, dataset.variablesQuantity, trainingFiles;

def CreateFolds(datasetFile, folds, parents, ess):
 if os.path.isfile(datasetFile):
  return Parse(Dataset(datasetFile), folds, parents, ess);
 else:
  return "Ivalid dataset file: " + datasetFile;

def CreateFoldsForMultipleDatasets(fileList, folds, parents, ess):
 return [CreateFolds(datasetFile, folds, parents, ess) for datasetFile in fileList]

def Error():
 print("Usage:", sys.argv[0], "data_filename", "number_of_folds");
 exit(0);

if __name__ == "__main__":
 # try:
  print(CreateFoldsForMultipleDatasets(sys.argv[1:-1], int(sys.argv[-1])));
 # except:
 #  Error();
