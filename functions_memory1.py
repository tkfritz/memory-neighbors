#import needed modules
import numpy as np
import time as time 
import itertools

#creates ordered numbers array
def ord_memory(n_pair):
    lis=[]
    for i in range(n_pair):
        lis.append(i)
        lis.append(i)
        arr=np.asarray(lis)
    return(arr)

#creates ransom 1d array of x apirs 
def random_1d(n_pair):
    #this shuffle function is used
    d = np.random.default_rng()
    #the previos function is used as inout
    arr=ord_memory(n_pair)
    #shuffle
    d.shuffle(arr)   
    return(arr)

#This function gets the most compact rectangle for a number of pairs
def fac(n_pair):
    #factors to output
    xar=np.zeros(2,dtype=int)
    #run until square root reached
    for i in range(int(np.sqrt(2*n_pair))):
        #execute if no rest in division, if yes pair  overwritten with more similar ones if possible
        if 2*n_pair/(i+1)%1==0:
            xar[0]=1+i
            xar[1]=2*n_pair/xar[0]
    return xar    

#convert tuple of tuple to list of list 
def tuple_to_list(t):
    return [list(x) for x in t]


#not ideal from memory usuage since first are created, also not fast 
#for 4 , 5 seconds 
#5 are 3628800 in total uniques are   takes hours at least 
#get unique permutations for a number of memory pairs
def uniqper(pairs):
    start_time=time.time()
    #create two vectors of length
    arra = np.arange(pairs)
    arrb = np.arange(pairs)
    #combine them
    arr=np.concatenate((arra,arrb))
    #convert to list
    lista=arr

    #get permutaations
    a=list(itertools.permutations(lista))
    #convert to list
    lista=tuple_to_list(a)
    #fill first element which is never a duplication
    listb=[lista[0]]
    c=1
    print(f"all permutations are {len(lista)}")
    for i in range(1,len(lista)):
        x=0
        j=0
        #check for equality in while loop should make it faster
        while x==0 and j<len(listb):
            if lista[i]==listb[j]:
                x=1
            j+=1    
        if x==0:
            listb.append(lista[i])
            c+=1
    print(f"unique permutations are {c}") 
    bar=np.array(listb) 
    stop_time=time.time()
    print(f"run time is {stop_time-start_time} s")
    return bar

#function which determine whether there is no
#neighboring pair in a tiling (identical numbers neighbors in a numpy array) 
#input is a 2D array
def check_nopairs_tiling(array):
    #bollean paramter for existance of no neighboring pairs
    c=False
    #dimnsion of array
    axis1=array.shape[0]
    axis2=array.shape[1]
    #number od pairs
    n_pair=int(axis1*axis2/2)
    #for more than 2 pairs
    #subtract by one shifted in both axis
    if n_pair>2:
        x1=np.min(abs(array[0:axis1-1,:]-array[1:axis1,:]))
        #create dummy only changed if second operation needed
        x2=0
        #only done if no macth in first part
        if x1>0:
            x2=np.min(abs(array[:,0:axis2-1]-array[:,1:axis2]))
        #enarge counter by one if no match 
            if x1>0 and x2>0:
                c=True
    if n_pair==2:
            #special case for two pairs
            if array[0,0]!=array[0,1] and array[0,0]!=array[1,0]:
                c=True
    #return whether there are no no neighboring pairs                                               
    return c


#function to determine fraction of no neighboring tilings among all tilings
def prob_all_perm(n_pair):
    print(str(n_pair)+" pairs")
    #time for knowing run_time
    start_time=time.time()
    list_pairs=ord_memory(n_pair)
    #permute list
    perm_object=list(itertools.permutations(list_pairs))
    #convert permutation object to list
    list_permutations=tuple_to_list(perm_object)
    #convert to array, each row is one to be tested case
    arr=np.array(list_permutations)
    #dimensions of reordering to tile
    dim=fac(n_pair)
    print(f"number of permutations {arr.shape[0]}")
    #number of cases with no neighbors
    no_neighbor=0
    for i in range(arr.shape[0]):
        #reorder to tile
        array=arr[i].reshape(dim[0], dim[1])
        #function to determing whether there are no neighboring pairs
        c=check_nopairs_tiling(array)
        no_neighbor+=c
    stop_time=time.time()
    print(f"run time is {round(stop_time-start_time,4)} sec")
    print(f"no neighboring pair in tiling to {round(no_neighbor/arr.shape[0]*100,2)} % ")  
    return no_neighbor/arr.shape[0]


#analytic probability
def ana_prob(n_pair):
    #dimeniosn of the tile
    xar=fac(n_pair)
    #number of corner
    corn_num=4
    #inner tile
    inner_num=(xar[0]-2)*(xar[1]-2)
    #rest is number of edge 
    edge_num=xar[0]*xar[1]-inner_num-corn_num
    #get number of neighbors, divide by two since it work both ways 
    n_neigh=(inner_num*4+edge_num*3+corn_num*2)/2
    #excluding the current one there 2_n-1 in the denominator, in the numertator it is 1 less more
    prob=((2*n_pair-2)/(2*n_pair-1))**(n_neigh)
    return xar[0],  xar[1], prob  



#parameters: number_of_pairs, number of random draws
#the neighbor counting is the same as above should be another function
def count_rand_pairb(pairs,draws):
    #convert to integer
    pairs=int(pairs)
    #function for getting dimensions of tiled area
    dim=fac(pairs)
    #counter for no_pair cases
    counter=0
    #do the number of random draws
    for i in range(draws):
        #shuffle the pairs
        shuf=random_1d(pairs)
        #reorder into tiling
        reord=shuf.reshape(dim[0], dim[1])
        #application of function which check whethers the assumption that there are no pairs is correct
        no_pair=check_nopairs_tiling(reord)  
        counter+=no_pair                  
    return counter/draws 
