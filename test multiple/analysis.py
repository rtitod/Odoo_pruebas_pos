import os
import re
from tabulate import tabulate
i = 2
# #1 : lines of code or comments
# #2 : wrong lines of code or comments
comments = [0,0]
codelines = [0,0]
classes = 0
avg_class = []
variables_names = set()
ntests = 0

comments_buffer = open('comments.txt','w')
codelines_buffer = open("codelines.txt",'w')
classes_buffer = open('classes.txt','w')
tests_buffer = open('tests.txt','w')

def walk_directory(path):
    global classes,ntests
    for root, dirs, files in os.walk(path):        
        for f in files:
            if f.endswith('.py'):
                print(os.path.join(root,f))
                pathFile = os.path.join(root,f)
                nclass = 0
                with open(pathFile,'r') as file:
                    for line in file.readlines():
                        line = line.strip()
                        names = re.findall(r'\b([a-zA-Z_]\w*)\b', line)
                        if names:
                            for name in names:
                                variables_names.add(name)
                        if line.startswith('def '):
                            functions_name = re.findall(r'\bdef\s+([a-zA-Z_]\w*)\s*\(', line)
                            if functions_name:
                                for fname in functions_name:
                                    if fname.startswith('test'):
                                        print(fname,file=tests_buffer)
                                        ntests+=1
                        if line.startswith('#') or line.startswith('"""'):
                            if len(line) > 72:
                                comments[1] += 1
                                print(line,file = comments_buffer)
                            else:
                                comments[0] += 1
                        elif line.startswith('class'):
                            nclass += 1
                            print(line,file =classes_buffer)
                        elif line != '':
                            if len(line) > 79:
                                print(line,file=codelines_buffer)
                                codelines[1] +=1
                            else:
                                codelines[0] +=1
                classes += nclass
                avg_class.append(nclass)

# Provide the path of the directory you want to walk
directory_path = os.path.join(os.getcwd(), 'point_of_sale')

# Call the function to walk through the directory
walk_directory(directory_path)

comments_buffer.close()
codelines_buffer.close()
classes_buffer.close()
tests_buffer.close()

table = []
index = 0
tmp = []
for var in variables_names:
    if index == 4:
        tmp = []
        index = 0
        table.append(tmp)
    tmp.append(var)
    index += 1


info = f'''
Total número de UnitTests: {ntests} unit tests

Total de número de variables: {len(variables_names)} nombres 

Total número clases: {classes}
Promedio de clases por archivo .py: {sum(avg_class)/len(avg_class):.2}

Total Lineas de Código: {codelines[0]+codelines[1]}
Total Lineas de comentarios: {comments[0]+ comments[1]}
Lineas de código > 79(PEP8): {codelines[1]}
Lineas de comentarios > 72(PEP8): {comments[1]}
%Lineas de código > 79: {(codelines[1]*100/sum(codelines))}%
%Linea de comentarios > 72: {comments[1]*100/sum(comments)}%
'''
print(info)
fn = open("variables.txt",'w')
print(tabulate(table),file=fn)
fn.close()