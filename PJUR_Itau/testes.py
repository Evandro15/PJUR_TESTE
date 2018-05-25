import tools
import os
import csv
cont_tot = tools.conta_arquivo(r"PjurDocs", r"erros.txt")
print(cont_tot)

with open(r"ListalinksDocumentos.csv") as listaLinksDocumentos:
    leitorCSV = csv.reader(listaLinksDocumentos)
    cont = 0
    for linha in leitorCSV:
        if cont == cont_tot:
            break
        cont = cont + 1
        print("{0} / {1}".format(cont, cont_tot))
        in_files = 0
        txt = open(r"erros.txt")
               
        if linha[2] not in txt.read():
            for r, d, files in os.walk(r"PjurDocs"):
                for i in files:
                    if linha[2] in i:
                        in_files = 1
                        break
                   
            if in_files == 0:
                txtA = open(r"erros.txt", "a")
                txtA.write(str(linha))
                txtA.write("\n")
                txtA.close()
        
        txt.close()            
                
cont_tot = tools.conta_arquivo(r"PjurDocs", r"erros.txt")
print(cont_tot)              



