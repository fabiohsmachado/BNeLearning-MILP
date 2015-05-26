import sys, os
import cplex

from ScoreSet import ScoreSet

def ComputeMILP(scoreFile, treewidth):
 print "Learning new structure for socre file " + scoreFile + " and treewidth " + str(treewidth);
 scoreSet = ScoreSet(scoreFile);
 c = cplex.Cplex();
 start = c.get_time();

# Preparing Variables
## N
 N = scoreSet.variablesQuantity;
## Uper bounds
### (6i)
 zUpperBound = [N] * N;
 vUpperBound = [N] * N;
### (6j)
 yUpperBound = [[1] * N] * N;
### (6k)
 piUpperBound = [[1] * len(parentSet) for parentSet in scoreSet.parentSets]

## Lower bounds
### (i6)
 zLowerBound = [0] * N;
 vLowerBound = [0] * N;
### (6j)
 yLowerBound = [[0] * N] * N;
### (6k)
 piLowerBound = [[0] * len(parentSet) for parentSet in scoreSet.parentSets]

## Types
 piTypes = [[c.variables.type.integer * len(piVariable)] for piVariable in piUpperBound];
 yTypes = [[c.variables.type.integer * N] * N];
 vTypes = [c.variables.type.continuous * N];
 zTypes = [c.variables.type.continuous * N];

##Names
 piNames = [['pi_' + str(i) + '_' + str(j) for j in range(len(scoreSet.parentSets[i]))] for i in range(len(scoreSet.parentSets))];
 yNames = [['y_' + str(i) + '_' + str(j) for j in range(N)] for i in range(N)];
 zNames = ['z_' + str(i) for i in range(N)];
 vNames = ['v_' + str(i) for i in range(N)];

## Indexes for reference
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
 scoresLinear = sum(scoreSet.parentScores, []);
 piNamesLinear = sum(piNames, []);
 piUpperBoundLinear = sum(piUpperBound, []);
 piLowerBoundLinear = sum(piLowerBound, []);
 piTypesLinear = sum(piTypes, []);
 yNamesLinear = sum(yNames, []);
 yUpperBoundLinear = sum(yUpperBound, []);
 yLowerBoundLinear = sum(yLowerBound, []);
 yTypesLinear = sum(yTypes, []);

# Setting up problem
 c.set_problem_type(cplex.Cplex.problem_type.MILP);
 c.objective.set_sense(c.objective.sense.maximize);

# (6a) - Objective Function
 c.variables.add(obj = scoresLinear, ub = piUpperBoundLinear, lb = piLowerBoundLinear, types = piTypesLinear, names = piNamesLinear);

# Auxiliary Variables
## y
 c.variables.add(ub = yUpperBoundLinear, lb = yLowerBoundLinear, types = yTypesLinear, names = yNamesLinear);
## v
 c.variables.add(ub = vUpperBound, lb = vLowerBound, types = vTypes, names = vNames);
## z
 c.variables.add(ub = zUpperBound, lb = zLowerBound, types = zTypes, names = zNames);

# Constraints
 linearExpressions = [];
 senses = [];
 rightHandSide = [];

## (6b)
 for i in range(N):
  linearExpressions.append([[yIndex[i][j] for j in range(N)], [1.0 for j in range(N)]]);
  senses.append('L');
  rightHandSide.append(float(treewidth));

## (6c)
 for i in range(N):
  for j in range(N):
   if(i != j):
    linearExpressions.append([[yIndex[i][j], zIndex[j], zIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

## (6d)
 for i in range(N):
  for j in range(N):
   for k in range(N):
    if (i != j and i != k and j != k): # and j < k):
     linearExpressions.append([[yIndex[i][j], yIndex[i][k], yIndex[j][k], yIndex[k][j]], [1.0, 1.0, -1.0, -1.0]]);
     senses.append('L');
     rightHandSide.append(1);

## (6e)
 for piVariablesIndex in piIndex:
  linearExpressions.append([piVariablesIndex, [1.0 for _ in range(len(piVariablesIndex))]]);
  senses.append('E');
  rightHandSide.append(1);

## (6f)
 for i in range(N):
  variableParentSet = scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in variableParentSet[t]:
    linearExpressions.append([[piIndex[i][t], vIndex[j], vIndex[i]], [(N + 1), -1.0, 1.0]]);
    senses.append('L');
    rightHandSide.append(N);

## (6g)
 for i in range(N):
  variableParentSets = scoreSet.parentSets[i];
  for t in range(len(variableParentSets)):
   for j in variableParentSets[t]:
    linearExpressions.append([[piIndex[i][t], yIndex[i][j], yIndex[j][i]], [1.0, -1.0, -1.0]]);
    senses.append('L');
    rightHandSide.append(0);
    
## (6h)
 for i in range(N):
  variableParentSet = scoreSet.parentSets[i];
  for t in range(len(variableParentSet)):
   for j in variableParentSet[t]:
    for k in variableParentSet[t]:
     if(j != k): # and j < k):
      linearExpressions.append([[piIndex[i][t] , yIndex[j][k], yIndex[k][j]], [1.0, -1.0, -1.0]]);
      senses.append('L');
      rightHandSide.append(0);

 outputFileName = os.path.splitext(scoreFile)[0] + ".tw" + str(treewidth);
 c.set_log_stream(outputFileName + ".cplex.log");
 c.set_error_stream(outputFileName + ".cplex.error");
 c.set_warning_stream(outputFileName + ".cplex.warning");
 c.set_results_stream(outputFileName + ".cplex.resuts");

# Add constrainsts, save the problem and solve
 c.linear_constraints.add(lin_expr = linearExpressions, senses = senses, rhs = rightHandSide);
 c.write(outputFileName + "cplex.lp");
 c.solve();

# Get results
 result = c.solution.get_values();
 resultMatrixPi = [[result[varIndex] for varIndex in piVariable] for piVariable in piIndex];
 resultMatrixY = [[result[varIndex] for varIndex in yVariable] for yVariable in yIndex];
 resultListZ = [result[varIndex] for varIndex in zIndex];
 resultListV = [result[varIndex] for varIndex in vIndex];
 
# Create the adjacency matrix
 matrix = [];
 for _ in range(N):
  matrix.append([0] * N);

 for i in range(N):
  for j in range(len(resultMatrixPi[i])):
   if(resultMatrixPi[i][j] == 1):
    for k in scoreSet.parentSets[i][j]:
     matrix[k][i] = 1;

# Create result file
 eliminationOrder = [i[0] for i in sorted(enumerate(resultListZ), key=lambda x:x[1])]
 finalScore = c.solution.get_objective_value();
 gap = 0; ####
 end = c.get_time();

# Save results 
 with open(outputFileName + ".time", "w") as timeFile:
  timeFile.write("Elapsed time:\n");
  timeFile.write(str(end - start));
  timeFile.write("\nElimination order: \n");
  timeFile.write(str(eliminationOrder));
  timeFile.write("\nScore of the found network: \n");
  timeFile.write(str(finalScore) + "\n");
  timeFile.write("\nError gap to the best solution: \n");
  timeFile.write(str(gap) + "\n"); 

 with open(outputFileName + ".matrix", "w") as matrixFile:
  matrixFile.write("\n".join(" ".join(map(str, map(int, dataLine))) for dataLine in matrix));
  matrixFile.write("\n");

# End
 print "Finished learning new structure for socre file " + scoreFile + " and treewidth " + str(treewidth) + " with time " + str(end - start) + ".";
 return outputFileName + ".matrix";
 
def Error():
 print("Usage:", sys.argv[0], "score_file", "treewidth");
 exit(0);

if __name__ == "__main__":
 try:
  if os.path.isfile(sys.argv[1]):
   ComputeMILP(sys.argv[1], sys.argv[2])
  else:
   Error();
 except:
  Error();
