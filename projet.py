
import math
import matplotlib.pyplot as plt
import random
import time

#1 Echauffement

def decomposition(x):
    """ 
    int->liste[bool] 
    retourne  une liste de bit correspondant à la decomposition en base 2 de x
    """
    res=[]
    if(x==0):
        return [False]
    while (x>0):
        quotient =x//2
        rest = x%2
        if (rest==0):
            res.append(False)
        else:
            res.append(True)
        x=quotient
    return res

#a=decomposition(38)
#print(a)

def completion(l,n):
    """ 
    list[bool]*int->list[bool]
    retourne la liste tronquée de l ne contenant que ses n premiers éléments
    """
    if len(l)>=n:
        return l[0:n]
    else :
        res=l
        t=n-len(l)
        for i in range (t):
            res.append(False)
        return res

#print(completion([False, True, True, False, False, True], 8))

def table(x,n):
    """
    int*int->list[bool]
    retourne la decomposition binaire de x completee afin qu'elle soit de taille n
    """
    bin=decomposition(x)
    return completion(bin,n)

#print(table(38,8))

#2 Arbre de décision et compression

#2.5
class ArbreBinDec():
    def __init__(self, val, fg, fd,luka):
        self.val = val
        self.fg = fg
        self.fd = fd
        self.luka = luka
    def __str__(self):
        if(self.val) is not None and self.fg is not None and self.fd is not None:
            return "x" + str(self.val) + " (" + str(self.fg) +", "+ str(self.fd) +")"
        elif self.fg is None and self.fd is None:
            return str(self.val)

#2.6
def consArbre(tab):
    """
    liste[bool]->ArbreBinDec
    """

    namevar=math.log2(len(tab))
    if(namevar==0):
        return ArbreBinDec(tab[0],None,None,None)

    if len(tab) == 0:
        return None
    else:
        return ArbreBinDec(int(namevar), consArbre(tab[:len(tab) // 2]), consArbre(tab[(len(tab) // 2):]),None)




def luka(abr):
    """
    ArbreBinDec->string
    """
    if abr.luka is not None:
        return str(abr.luka)
    else:
        if abr.fg is not None and abr.fd is not None:
            abr.luka = "x" + str(abr.val) + "(" + str(luka(abr.fg)) +") ("+ str(luka(abr.fd)) +")"
        else:
            abr.luka = str(abr.val)
        return abr.luka

#2.8


def parcours(self,d={},):
    if self.fg:
        parcours(self.fg,d)
    if(self.val in d):
        d[len(d)]=self.luka
    else:
        d[self.val]=self.luka
    if self.fd:
        parcours(self.fd,d)
    return d


#2.8
def compression(arbre):
    """
    ArbreBinDec->ArbreBinDec
    """
    def dag(arbreLuka, listeNoeud, listeLuka):
        if arbreLuka.luka not in listeLuka:
            listeLuka.append(arbreLuka.luka)
            listeNoeud.append(arbreLuka)
            #print(listeLuka)
            if arbreLuka.fg is not None and arbreLuka.fd is not None:
                noeudGauche = dag(arbreLuka.fg,listeNoeud,listeLuka)
                noeudDroit = dag(arbreLuka.fd,listeNoeud,listeLuka)
                return ArbreBinDec(arbreLuka.val, noeudGauche, noeudDroit, arbreLuka.luka)
            else:
                return ArbreBinDec(arbreLuka.val, None, None, arbreLuka.luka)
        else:
            i=listeLuka.index(arbreLuka.luka)
            return listeNoeud[i]
    luka(arbre)
    l=[]
    return dag(arbre, l, [])
    #for i in range (len(l)):
    #    print(l[i].luka)


#2.9 Fonctionne que pour les arbres non compressés
def dot1(abr):
    f=open("arbre1.dot","w")
    f.write("digraph {\n")
    def ecriture(noeud,f,val,l=[]):
        if noeud.fg is not None:
            if noeud.fg not in l:
                l.append(noeud.fg)
                s=len(l)-1
            else:
                s=l.index(noeud.fg)
            name="x"+str(noeud.fg.val)+"_"+str(s)
            f.write(val+"->"+name+"\n")
            ecriture(noeud.fg,f,name,l)
        if noeud.fd is not None:
            if noeud.fd not in l:
                l.append(noeud.fd)
                s=len(l)-1
            else:
                s=l.index(noeud.fd)
            name="x"+str(noeud.fd.val)+"_"+str(s)
            f.write(val+"->"+name+"\n")
            ecriture(noeud.fd,f,name,l)

    val="x"+str(abr.val)
    l=[]
    l.append(abr)
    ecriture(abr,f,val,l)
    f.write("}")


#2.9 Fonctionne que pour les arbres compressés
def dot2(abr):
    f=open("arbre2.dot","w")
    f.write("digraph {\n")
    def ecriture(noeud,f,val,l=[]):
        if noeud.fg is not None:
            if noeud.fg.luka not in l:
                l.append(noeud.fg.luka)
                s=len(l)-1
                name="x"+str(noeud.fg.val)+"_"+str(s)
                f.write(val+"->"+name+"\n")
                ecriture(noeud.fg,f,name,l)
            else:
                s=l.index(noeud.fg.luka)
                name="x"+str(noeud.fg.val)+"_"+str(s)
                f.write(val+"->"+name+"\n")
            
        if noeud.fd is not None:
            if noeud.fd.luka not in l:
                l.append(noeud.fd.luka)
                s=len(l)-1
                name="x"+str(noeud.fd.val)+"_"+str(s)
                f.write(val+"->"+name+"\n")
                ecriture(noeud.fd,f,name,l)
            else:
                s=l.index(noeud.fd.luka)
                name="x"+str(noeud.fd.val)+"_"+str(s)
                f.write(val+"->"+name+"\n")


    val="x"+str(abr.val)
    l=[]
    l.append(abr.luka)
    ecriture(abr,f,val,l)
    f.write("}")


#3.10
def compression_bdd(arbre):
    """
    Terminal rule: 
        The only possible leaf nodes are T and F,
        so these nodes can be represented by two singleton objects, 
        allowing pointers to them to be shared.
    Deletion rule: 
        If any node X is such that its positive and negative arrows both 
        point to the same node Y , then X is said to be symmetric. Such a node can be 
        deleted and arrows previously pointing to it may be promoted to point to Y 
        directly.
    """
    newdag=compression(arbre)

    a1=ArbreBinDec(False,None,None,str(False))
    a2=ArbreBinDec(True,None,None,str(True))

    def bdd(arbredag, pere=None):

        if pere is None:
            return ArbreBinDec(arbredag.val,bdd(arbredag.fg,arbredag),bdd(arbredag.fd,arbredag),None)

        else:
            if arbredag.fg is not None and arbredag.fd is not None:
                if (arbredag.fg.luka == arbredag.fd.luka):
                    temp=arbredag
                    while(temp.fg.fg is not None and temp.fg.fg.luka == temp.fg.fd.luka):
                        temp=temp.fg

                    if temp.fg.fg is not None and temp.fg.fd is not None: 
                        return ArbreBinDec(temp.fg.val,bdd(temp.fg.fg,pere),bdd(temp.fg.fd,pere),None)
                    else:
                        return temp.fg
                else:
                    return ArbreBinDec(arbredag.val,bdd(arbredag.fg,arbredag),bdd(arbredag.fd,arbredag),None)
            else: 
                if arbredag.val==True:
                    return a2
                else:
                    return a1
    res=bdd(newdag)
    luka(res)
    return res

tab1=table(38,8)
ab1=consArbre(tab1)
#dot1(ab1)
#dot2(compression(ab1))
#res=compression_bdd(ab1)
#dot2(res)
tab2=table(432,8)
ab2=consArbre(tab2)
dot1(ab2)
dot2(compression_bdd(ab1))

#4 Experimentation

def nbnoeud(arbre):
    """
    retourne le nombre de noeud d'un arbre
    """
    if (arbre.fg.luka == arbre.fd.luka and arbre.fg.fg is None and arbre.fg.fd is None):
        return 1
    def aux(abr,listeLuka):
        if abr.luka not in listeLuka:
            listeLuka.append(abr.luka)
            if abr.fg is not None and abr.fd is not None:
                aux(abr.fg,listeLuka)
                aux(abr.fd,listeLuka)
    
    l=[]
    aux(arbre,l)
    return len(l)

#print(nbnoeud(compression_bdd(ab1)))


#M'a permis de voir que compression_bdd ne fonctionne pas bien lorsque
#la racine a les mêmes fg et fd
def test2variables():
    for i in range(0,2**(2**2)):
        arbre=consArbre(table(i,2**2))
        print(table(i,2**2))
        print(arbre)
        bdd=compression_bdd(arbre)
        print(bdd)
        print(nbnoeud(bdd))


def qu15():

    for i in range(1,5):
        nb=[0]* (2 ** i + 2)
        #Avec index = nombre de noeuds et val = nombre d'arbre qui ont ne nb de noeuds
        for j in range(0,2**(2**i)):
            arbre=consArbre(table(j, (2**i) ))
            bdd=compression_bdd(arbre)
            nb[nbnoeud(bdd)]+=1

        lx = []
        y = []
        for x in range(len(nb)):
            if nb[x] != 0:
                lx.append(x)
                y.append(nb[x])
        plt.scatter(lx,y)
        plt.plot(lx, y)
        plt.xlabel("ROBDD node count for " + str(i) + " variables")
        plt.ylabel("Number of Boolean functions")
        plt.show()

#qu15()

def qu16():

    xaxe = [20, 40, 50, 80, 150, 260]
    #Si je faisais comme la question 15 les tableaux allaient être beaucoup trop grands
    #Donc j'ai pris les mêmes axes que la figure 10
    nbsamples = [500003, 400003, 486892, 56343, 94999, 17975]
    for i in range(5, 11):
        nb = [0] * xaxe[i-5]
        start = time.time()
        abr=[]
        for j in range(nbsamples[i-5]):
            r=random.randrange(2 ** (2 ** i))
            while( r in abr):
                r=random.randrange(2 ** (2 ** i))
            abr.append(r)
            arbre = consArbre(table(r, 2 ** i))
            bdd= compression_bdd(arbre)
            if len(nb) >= nbnoeud(bdd):
                nb[nbnoeud(bdd) - 1] += 1
        end = time.time()
        t=end-start
        print("Temps d'execution pour "+str(i)+" variables : "+str(t))
        print("Seconds ROBDD: "+str(t/nbsamples[i-5]))

        lx = []
        y = []
        nbunique = 0
        tmp = []
        for x in range(len(nb)):
            lx.append(x + 1)
            y.append(nb[x])
            if nb[x] not in tmp:
                tmp.append(nb[x])
                nbunique += 1
        print("No unique size for  "+str(i)+" variables : "+str(nbunique))

        plt.scatter(lx, y)
        plt.plot(lx, y)
        plt.ylabel('Number of Boolean functions')
        plt.xlabel('ROBDD node count for ' + str(i) + ' variables')
        plt.show()

qu16()