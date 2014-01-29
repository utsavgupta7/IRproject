#import os module to read directory structure
import os

#matrix is a dictionary used to store inverted index
matrix={}

#the list terms store the terms present in the entire corpus
terms=[]

#the dictionary matrix_siii is used to store schema independent inverted index
matrix_siii={}

#phrase matching algorithm
def next(term,position):
    for pos in matrix_siii[term]:
        if pos>=position:
            return pos
    return None

#phrase matching algorithm
def phrase_match(phrase_terms,position):
    u=next(phrase_terms[0],position)
    v=u
    for i in range(1,len(phrase_terms)):
        if v<>None:
            v=next(phrase_terms[i],v)
    if v==None or u==None:
        return 'Not Found'
    elif v-u==(len(phrase_terms))-1:
        return u
    else:
        return phrase_match(phrase_terms,v-len(phrase_terms))

#creates schema independent inverted index
def create_siiindex(path):
    words=""
    doclist=os.listdir(path)
    for filename in doclist:
        full_filename=path+'/'+filename
        file=open(full_filename,'r')
        words=words+file.read().lower()+" "
    terms=words.split()
    i=1
    for term in terms:
        if term in matrix_siii:
            matrix_siii[term].append(i)
        else:
            matrix_siii[term]=[i]
        i=i+1
    print "\nThe schema independent inverted index is :"
    for term in matrix_siii:
        print term,":",matrix_siii[term]   

#used for calculating edit distance between query term and terms in the corpus
def edit_distance(query_term,term):
    m=[[0 for x in xrange(len(query_term)+1)]for x in xrange(len(term)+1)]
    for j in xrange(len(query_term)+1):
        m[0][j]=j
    for j in xrange(len(term)+1):
        m[j][0]=j
    for i in range(1,len(term)+1):
        for j in range(1,len(query_term)+1):
            if term[i-1]==query_term[j-1]:
                p=m[i-1][j-1]
            else:
                p=m[i-1][j-1]+1
            m[i][j]=min(p,m[i-1][j]+1,m[i][j-1]+1)
    return m[len(term)][len(query_term)]

#used for checking and correcting spellings             
def spell_check(query_term):
    editdist=[0 for x in xrange(len(terms)+1)]
    i=1
    for term in terms:
        editdist[i]=edit_distance(query_term,term)
        i=i+1
    index=0
    #set the value of min as per the precision required
    min=len(query_term)-1
    for x in xrange(1,len(editdist)):
        if editdist[x]<min:
            index=x
            min=editdist[x]
    if index==0:
        return ''
    else:
        return terms[index-1]

#if the query comprise of just one term we use this function        
def singleton_query(term):
    if term not in matrix:
        term=spell_check(term)
    if term=='':
        return "term not found"
    print "did u mean ",term
    return matrix[term]

#creates inverted index    
def create_matrix(words,filename):
    filename=int(filename[3:4])
    for word in words:
        if word in matrix:
            if filename not in matrix[word]:
                matrix[word].append(filename)
        else:
            matrix[word]=[filename]

#used for reading the corpus and creates inverted index
def get_terms(path):
    doclist=os.listdir(path)
    for filename in doclist:
        full_filename=path+'/'+filename
        file=open(full_filename,'r')
        words=file.read().lower().split()
        for word in words:
            if word not in terms:
                terms.append(word)
        create_matrix(words,filename)
    print "\n\nthe index is as follows:"
    for entries in matrix:
        print entries,matrix[entries]

#used for processing the query(union and intersection)
def query_processing(entry):
    answer=['query term not found']
    if (entry.find(' and '))<>-1:
        pivot=entry.find(' and ')
        term1=entry[:pivot].strip()
        term2=entry[pivot+5:].strip()
        if term1 not in matrix:
            term1=spell_check(term1)
        if term2 not in matrix:
            term2=spell_check(term2)
        print '\nDid u mean: ',term1,' AND ',term2
        if term1<>'' and term2<>'':
            answer=intersection(matrix[term1],matrix[term2])
    elif (entry.find(' or '))<>-1:
        pivot=entry.find(' or ')
        term1=entry[:pivot].strip()
        term2=entry[pivot+4:].strip()
        if term1 not in matrix:
            term1=spell_check(term1)
        if term2 not in matrix:
            term2=spell_check(term2)
        print '\nDid u mean: ',term1,' OR ',term2
        if term1<>'' and term2<>'':
            answer=union(matrix[term1],matrix[term2])
        
    return answer

#used for procesing intersection logic(AND clause)
def intersection(list1,list2):
    i=0
    j=0
    answer=[]
    while i<len(list1) and j<len(list2):
        if list1[i]==list2[j]:
            answer=answer+[list1[i]]
            i=i+1
            j=j+1
        elif list1[i]<list2[j]:
            i=i+1
        else:
            j=j+1
    return answer

#used for processing union logic(OR clause)
def union(list1,list2):
    i=0
    j=0
    answer=[]
    while i<len(list1) and j<len(list2):
        if list1[i]==list2[j]:
            answer=answer+[list1[i]]
            i=i+1
            j=j+1
        elif list1[i]<list2[j]:
            answer=answer+[list1[i]]
            i=i+1
        else:
            answer=answer+[list2[j]]
            j=j+1
    while i<len(list1):
        answer=answer+[list1[i]]
        i=i+1
    while j<len(list2):
        answer=answer+[list2[j]]
        j=j+1
    return answer
    

#prompt the user to enter the directory path
path=raw_input("enter the directory path ::>")

#function cal to read the directory structure and create inverted index implicitly
get_terms(path)

#create schema independent inverted index
create_siiindex(path)

entry=''
while entry<>'exit':
    entry=(raw_input("\n\n1.type 'query' to process a query\n2.type 'phrase' to search phrase\n3.type 'exit' to exit\n")).lower()
    if entry=='exit':
        continue
    elif entry=='phrase':
        phrase=(raw_input("enter the phrase u r lookin for !!!\n")).lower()
        phrase_terms=[]
        if len(phrase.split())<2:
            print "This isn't a phrase,this is a query :"
            print singleton_query(phrase)
            continue
        for phrase_term in phrase.split():
            if phrase_term not in matrix:
                phrase_term=spell_check(phrase_term)
                if phrase_term=='':
                    print 'Not Found'
                    continue
            phrase_terms.append(phrase_term)
        print "Did U mean :",phrase_terms                
        u=0
        
        while u<>'Not Found':
            u=phrase_match(phrase_terms,u+1)
            if u<>'Not Found':
                print "phrase is present at following indexes:\n"
                print u
                                
    elif entry=='query':
        query=(raw_input("enter the query")).lower()
        if query.find(' and ')==-1 and query.find(' or ')==-1:
            print singleton_query(query)
            continue
        print query_processing(query)
    else:
        print "enter a proper choice"



 
    
        


    
    







