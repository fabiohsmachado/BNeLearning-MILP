import sys, os
from subprocess import call

def CompactFolder(folder_name, delete = False):
 compactCommand = ["tar", "-C", os.path.dirname(folder_name), "-zcf", folder_name + ".tar.gz", os.path.basename(folder_name)];
 call(compactCommand, stdout = None, shell = False);

 if(delete):
  deleteCommand = ["rm", "-rf", folder_name]
  call(deleteCommand, stdout = None, shell = False);

def Error():
 print("Usage:", sys.argv[0], "folder_name", "delete_option");
 exit(0);
 
if __name__ == "__main__":
 # try:
  CompactFolder(sys.argv[1], sys.argv[2]);
 # except:
 #  Error();
