from pyccel.decorators import types, pure

@pure
@types('int','int')
def add2(x, y):
    return x+y

@types('int')
@pure
def sum_to_n(n):
    result=0
    for i in range(1,n+1):
        result = add2(result,i)
    return result

print(sum_to_n(4))
