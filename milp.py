import sys, os
import cplex

from Dataset import Dataset

def ComputeMILP(datasetFile, scoreFile, treewidth):
 dataset = Dataset(datasetFile, scoreFile);
 c = cplex.Cplex();

# Preparing Variables
## N
 N = dataset.variablesQuantity;
## Uper bounds
### (6i)
 zUpperBound = [1] * N;
 vUpperBound = [1] * N;
### (6j)
 yUpperBound = [[1] * N] * N;
### (6k)
 piUpperBound = [[1] * len(parentSet) for parentSet in dataset.scoreSet.parentSets]

## Lower bounds
### (6i)
 zLowerBound = [0] * N;
 vLowerBound = [0] * N;
### (6j)
 yLowerBound = [[0] * N] * N;
### (6k)
 piLowerBound = [[0] * len(parentSet) for parentSet in dataset.scoreSet.parentSets]

## Names
 piNames = [['pi_' + str(i) + '_' + str(j) for j in range(len(dataset.scoreSet.parentSets[i]))] for i in range(len(dataset.scoreSet.parentSets))];
 yNames = [['y_' + str(i) + '_' + str(j) for j in range(N)] for i in range(N)];
 zNames = ['z_' + str(i) for i in range(N)];
 vNames = ['v_' + str(i) for i in range(N)];

## Types
 piTypes = [[c.variables.type.integer * len(piVariable)] for piVariable in piUpperBound];
 yTypes = [[c.variables.type.integer * N] * N];
 vTypes = [c.variables.type.continuous * N];
 zTypes = [c.variables.type.continuous * N];

## Indexes for faster reference later after linearization
 k = 0;

 piIndex = []
 for i in range(len(piUpperBound)):
  piIndex.append([]);
  for _ in range(len(piUpperBound[i])):
   piIndex[i].append(k);
   k += 1;

 yIndex = [];
 for i in range(N):
  yIndex.append([]);
  for _ in range(N):
   yIndex[i].append(k);
   k += 1;

 vIndex = [0] * N;
 for i in range(N):
  vIndex[i] = k;
  k += 1;

 zIndex = [0] * N;
 for i in range(N):
  zIndex[i] = k;
  k += 1;

## Linearization of matrixes
 scoresLinear = sum(dataset.scoreSet.parentScores, []);
 piUpperBoundLinear = sum(piUpperBound, []);
 piLowerBoundLinear = sum(piLowerBound, []);
 piTypesLinear = sum(piTypes, []);
 yUpperBoundLinear = sum(yUpperBound, []);
 yLowerBoundLinear = sum(yLowerBound, []);
 yTypesLinear = sum(yTypes, []);

# Setting up problem
 c.set_problem_type(cplex.Cplex.problem_type.MILP);
 c.objective.set_sense(c.objective.sense.maximize);

# Objective function (6a)
 c.variables.add(obj = scoresLinear, ub = piUpperBoundLinear, lb = piLowerBoundLinear, types = piTypesLinear);

# Auxiliary Variables
## y
 c.variables.add(ub = yUpperBoundLinear, lb = yLowerBoundLinear, types = yTypesLinear);
## v
 c.variables.add(ub = vUpperBound, lb = vLowerBound, types = vTypes);
## z
 c.variables.add(ub = zUpperBound, lb = zLowerBound, types = zTypes);

# Constraints
 linearExpressions = [];
 senses = [];
 rightHandSide = [];

## (6c)
 for i in range(N):
  for j in range(N):
   if(i != j):
    linearExpressions.append([[yIndex[i][j], zIndex[j], zIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

 for i in range(N):
   linearExpressions.append([[yIndex[i][i]], [(N + 1)]]);
   senses.append('L');
   rightHandSide.append(N);

# ##(6d)
 for i in range(N):
  for j in range(N):
   for k in range(N):
    if (i != j and i != k and j != k):
     linearExpressions.append([[yIndex[i][j], yIndex[i][k], yIndex[j][k], yIndex[k][j]], [1.0, 1.0, -1.0, 1.0]]);
     senses.append('L');
     rightHandSide.append(N);

 for i in range(N):
  for k in range(N):
   if (i != k):
    linearExpressions.append([[yIndex[i][i], yIndex[k][i]], [1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(1);

 for i in range(N):
  for j in range(N):
   if (i != j):
    linearExpressions.append([[yIndex[i][j], yIndex[i][i], yIndex[j][i]], [2.0, 1.0, -1.0]]);
    senses.append('L');
    rightHandSide.append(1);

 for i in range(N):
  for j in range(N):
    linearExpressions.append([[yIndex[i][j]], [2.0]]);
    senses.append('L');
    rightHandSide.append(N);

## (6e)
 for piVariablesIndex in piIndex:
  linearExpressions.append([piVariablesIndex, [1.0 for i in range(len(piVariablesIndex))]]);
  senses.append('E');
  rightHandSide.append(1);

# ## (6f)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    linearExpressions.append([[piIndex[i][t], vIndex[variableParentSet[t][j]], vIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

## (6g)
 for i in range(N):
  variableParentSets = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSets)):
   for j in range(len(variableParentSets[t])):
    print(i, t, j, variableParentSets[t]);
   #  linearExpressions.append([[piIndex[i][t], yIndex[i][variableParentSet[t][j]], yIndex[variableParentSet[t][j]][i]], [1.0, -1.0, -1.0]]);
   #  senses.append('L');
   #  rightHandSide.append(0);

# ## (6h)
#  for i in range(N):
#   variableParentSet = dataset.scoreSet.parentSets[i];
#   for t in range(len(variableParentSet)):
#    for j in range(len(variableParentSet[t])):
#     for k in range(len(variableParentSet[t])):
#      if(j != k):
#       linearExpressions.append([[piIndex[i][t] , yIndex[variableParentSet[t][j]][variableParentSet[t][k]], yIndex[variableParentSet[t][k]][variableParentSet[t][j]]], [1.0, -1.0, -1.0]]);
#       senses.append('L');
#       rightHandSide.append(0);

#  for i in range(N):
#   variableParentSet = dataset.scoreSet.parentSets[i];
#   for t in range(len(variableParentSet)):
#    for j in range(len(variableParentSet[t])):
#     linearExpressions.append([[piIndex[i][t] , yIndex[variableParentSet[t][j]][variableParentSet[t][j]]], [1.0, -2.0]]);
#     senses.append('L');
#     rightHandSide.append(0);

 # c.linear_constraints.add(lin_expr = linearExpressions, senses = senses, rhs = rightHandSide);
 # c.solve();

 # dataset.boundedAdjacencyMatrix = GetAdjacencyMatrix(c, piVariablesIndex, dataset.scoreSet.parentSets);
 # dataset.WriteBoundedAdjacencyMatrixToFile();
 # # print('\n'.join([','.join(['{:4}'.format(int(item)) for item in row]) for row in dataset.boundedAdjacencyMatrix]));
 # print("\n".join(" ".join(map(str, dataLine)) for dataLine in dataset.boundedAdjacencyMatrix));


# # New Constraints
#  linearExpressions = [];
#  senses = [];
#  rightHandSide = [];

# ## (6b)
#  for i in range(N):
#   linearExpressions.append([[yIndex[i][j] for j in range(N)], [1.0 for i in range(N)]]);
#   senses.append('L');
#   rightHandSide.append(float(treewidth));

#  c.linear_constraints.add(lin_expr = linearExpressions, senses = senses, rhs = rightHandSide);
#  c.solve();

#  dataset.unboundedAdjacencyMatrix = GetAdjacencyMatrix(c, piVariablesIndex, dataset.scoreSet.parentSets);
#  dataset.WriteUnboundedAdjacencyMatrixToFile();
#  print('\n'.join([','.join(['{:4}'.format(int(item)) for item in row]) for row in dataset.boundedAdjacencyMatrix]));

def GetAdjacencyMatrix(problem, piVariablesIndex, parentSets):
 result = problem.solution.get_values();
 resultMatrixPi = [[result[piVariablesIndex[i]] for i in range(len(parentSet))] for parentSet in parentSets];
 # resultMatrixY = [[result[yVariablesIndex[i]] for i in range(len(yVariablesIndex))] for yVariablesIndex in yIndex]
 # resultV = [result[vIndex[i]] for i in range(len(vIndex))]
 # resultZ = [result[vIndex[i]] for i in range(len(vIndex))]

 print("\n".join(" ".join(map(str, map(int, dataLine))) for dataLine in resultMatrixPi));
 # print('\n'.join([''.join(['{:4}'.format(int(item)) for item in row]) for row in resultMatrixY]));
 # print(resultV);
 # print(resultZ);

 matrix = [[0] * len(parentSets)] * len(parentSets);
 for i in range(len(resultMatrixPi)):
  for t in resultMatrixPi[i]:
   if resultMatrixPi[i][int(t)] == 1:
    for j in parentSets[i][int(t)]:
     matrix[j][i] = 1;

 return matrix; 

def Error():
 print("Usage:", sys.argv[0], "treewidth", "dataset_file" "score_file");
 exit(0);

if __name__ == "__main__":
 # try:
  if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
   ComputeMILP(sys.argv[1], sys.argv[2], sys.argv[3])
  else:
   Error();
 # except:
 #  Error();
