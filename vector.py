import math
def add(vector1,vector2):
    ret=(vector1[0]+vector2[0],vector1[1]+vector2[1])
    return ret

def add_scalar(vector1,scalar):
    ret=(vector1[0]+scalar,vector1[1]+scalar)
    return ret

def subtract(vector1,vector2):
    ret=(vector1[0]-vector2[0],vector1[1]-vector2[1])
    return ret

def subtract_scalar(vector1,scalar):
    ret=(vector1[0]-scalar,vector1[1]-scalar)
    return ret

def multiply_scalar(vector,scalar):
    ret=(vector[0]*scalar,vector[1]*scalar)
    return ret

def multiply(vector1,vector2):
    ret=(vector1[0]*vector2[0],vector1[1]*vector2[1])
    return ret

def divide_scalar(vector,scalar):
    ret=(vector[0]/scalar,vector[1]/scalar)
    return ret

def divide(vector1,vector2):
    ret=(vector1[0]/vector2[0],vector1[1]/vector2[1])
    return ret

def square(vector):
    ret=(math.pow(vector[0],2),math.pow(vector[1],2))
    return ret

def sqrt(vector):
    ret=(math.sqrt(vector[0]),math.sqrt(vector[1]))
    return ret

def module(vector):
    return math.sqrt(math.pow(vector[0],2)+math.pow(vector[1],2))

def invert(vector):
    ret=(-vector[0],-vector[1])
    return ret

def to_int(vector):
    ret=(int(vector[0]),int(vector[1]))
    return ret