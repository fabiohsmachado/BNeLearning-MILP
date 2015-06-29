#!/bin/python
# Read a dataset file, a gobnilp adjacency matrix file and print the likelihood of the dataset.
import sys

import numpy
import networkx

from subprocess import call
from Dataset import Dataset
from data_likelihood import compute_likelihood

def GetGraphFromFile(matrixFile):
 matrix = "";
 with open(matrixFile, "r") as matrixFileFile:
  for line in matrixFileFile:
   matrix += line.strip('\n') + "; ";
 matrix = matrix[:-2];
 return networkx.from_numpy_matrix(numpy.matrix(matrix), create_using=networkx.DiGraph());

def GetListOfParents(matrixFile):
 gobnilpGraph = GetGraphFromFile(matrixFile);
 return [gobnilpGraph.predecessors(node) for node in gobnilpGraph.nodes()];

def MeasureLikelihood(datasetFile, matrixFile, ess):
 dataset = Dataset();
 dataset.ParseFile(datasetFile);
 return compute_likelihood(dataset.data, dataset.variablesCardinality, GetListOfParents(matrixFile), ess);

def Error():
 print "Usage:", sys.argv[0], "data_filename", "matrix_file", "ess";
 exit(0);

if __name__ == "__main__":
 if len(sys.argv) < 4:
  Error();
 print "Likelihood:", MeasureLikelihood(sys.argv[1], sys.argv[2], float(sys.argv[3]));
