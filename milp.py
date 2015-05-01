import sys, os
import cplex

from Dataset import Dataset

def ComputeMILP(datasetFile, scoreFile, treewidth):
 dataset = Dataset(datasetFile, scoreFile);
 N = dataset.variablesQuantity;

 c = cplex.Cplex();

#Preparing Variables
##Uper bounds
###(6i)
 zUb = [1] * N;
 vUb = [1] * N;
###(6j)
 yUb = [[1] * N] * N;
###(6k)
 piUb = [[1] * len(parentSet) for parentSet in dataset.scoreSet.parentSets]

#All lower bounds are zero (cplex default), and don't need to be specified.
##Names
 piNames = [['pi_' + str(i) + '_' + str(j) for j in range(len(dataset.scoreSet.parentSets[i]))] for i in range(len(dataset.scoreSet.parentSets))];
 yNames = [['y_' + str(i) + '_' + str(j) for j in range(N)] for i in range(N)];
 zNames = ['z_' + str(i) for i in range(N)];
 vNames = ['v_' + str(i) for i in range(N)];

##Types
 piTypes = [[c.variables.type.integer * len(piVariable)] for piVariable in piUb];
 yTypes = [[c.variables.type.integer * N] * N];
 vTypes = [c.variables.type.continuous * N];

##Indexes for faster reference later after linearization
 k = 0;

 piIndex = []
 for i in range(len(piUb)):
  piIndex.append([]);
  for _ in range(len(piUb[i])):
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

##Linearization of matrixes
 scoresLinear = sum(dataset.scoreSet.parentScores, []);
 piUbLinear = sum(piUb, []);
 piTypesLinear = sum(piTypes, []);
 yUbLinear = sum(yUb, []);
 yTypesLinear = sum(yTypes, []);

#Setting up problem
 c.set_problem_type(cplex.Cplex.problem_type.MILP);
 c.objective.set_sense(c.objective.sense.maximize);

#Objective function (6a)
 c.variables.add(obj = scoresLinear, ub = piUbLinear, types = piTypesLinear);

#Auxiliary Variables
##y
 c.variables.add(ub = yUbLinear, types = yTypesLinear);
##v
 c.variables.add(ub = vUb, types = vTypes);

#Constraints
 linearExpressions = [];
 senses = [];
 rightHandSide = [];
 rangeValues = [];

##(6e)
 for piVariablesIndex in piIndex:
  linearExpressions.append([piVariablesIndex, [1.0 for i in xrange(len(piVariablesIndex))]]);
  senses.append('E');
  rightHandSide.append(1);

##(6f)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    linearExpressions.append([[piIndex[i][t], vIndex[variableParentSet[t][j]], vIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

##(6g)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    linearExpressions.append([[piIndex[i][t], yIndex[i][variableParentSet[t][j]], yIndex[variableParentSet[t][j]][i]], [1.0, -1.0, -1.0]]);
    senses.append('L');
    rightHandSide.append(0);

##(6h)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    for k in range(len(variableParentSet[t])):
     if(j != k):
      linearExpressions.append([[piIndex[i][t] , yIndex[variableParentSet[t][j]][variableParentSet[t][k]], yIndex[variableParentSet[t][k]][variableParentSet[t][j]]], [1.0, -1.0, -1.0]]);
      senses.append('L');
      rightHandSide.append(0);

  c.linear_constraints.add(lin_expr = linearExpressions, senses = senses, rhs = rightHandSide);
  c.solve();

##(6e)
 for i in range(N):
  linearExpressions.append([piVariablesIndex, [1.0 for i in xrange(len(piVariablesIndex))]]);
  senses.append('E');
  rightHandSide.append(1);

##(6g)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    linearExpressions.append([[piIndex[i][t], yIndex[i][variableParentSet[t][j]], yIndex[variableParentSet[t][j]][i]], [1.0, -1.0, -1.0]])

##(6f)
 for i in range(N):
  variableParentSet = dataset.scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in range(len(variableParentSet[t])):
    linearExpressions.append([[piIndex[i][t], vIndex[variableParentSet[t][j]], vIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

 result = c.solution.get_values();
 resultMatrixPi = [[result[piVariablesIndex[i]] for i in range(len(piVariablesIndex))] for piVariablesIndex in piIndex]
 resultMatrixY = [[result[yVariablesIndex[i]] for i in range(len(yVariablesIndex))] for yVariablesIndex in yIndex]
 resultV = [result[vIndex[i]] for i in range(len(vIndex))]
 print(result);
 print(resultMatrixPi);
 print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in resultMatrixY]));
 print(resultV);

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
