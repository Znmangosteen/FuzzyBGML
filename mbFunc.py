# contains all the membership functions used by fuzzy rules
def func(K:int, k:int,x):
    #don't care
    if(K == 1):
        return 1
    # triangle membership functions
    a = (k-1)/(K-1)
    b = 1/(K-1)
    return max(1-abs(a-x)/b,0)
def u(n,x):
    i = 1
    t = n
    while ((t-i) > 0):
        t -= i
        i += 1
    return (func(i,t,x))
        