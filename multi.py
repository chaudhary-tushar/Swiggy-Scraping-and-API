import multiprocessing
import time

#it is probabbly better for the function testing to go through fibo finction tha through increment func
def my_function(n):
    print(f"Processing input {n}")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    # Use a loop to compute the nth Fibonacci number
    prev_prev = 0
    prev = 1
    for i in range(2, n+1):
        curr = prev_prev + prev
        prev_prev = prev
        prev = curr
    
    return curr

'''q=[1]
times=time.time()
for i in range(49):
    #print(my_function(q[0]))
    my_function(q[0])
timee=time.time()
runtime = timee - times
print("Runtime: {:.2f} seconds.".format(runtime))

'''
if __name__ == '__main__':
    inputs = []
    for i in range(49):
        inputs.append(400000)
    times=time.time()
    print("Start time: {:.2f} seconds.".format(times))
    processes = []

    for input_arg in inputs:
        p = multiprocessing.Process(target=my_function, args=(input_arg,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        
    timee=time.time()
    print("End time: {:.2f} seconds.".format(timee))
    runtime = timee - times
    print("Runtime: {:.2f} seconds.".format(runtime))