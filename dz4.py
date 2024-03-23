import threading,time,multiprocessing,asyncio

from random import randint

sumflow=0

mass=[]
for i in range(1000):
    mass.append(randint(1,101))
ma=[]

st=0
end=0
step=int(len(mass)/5)
for i in range(5):
    if i==4:
        end=len(mass)
    else:
        end=st+step
    ma.append(mass[st:end])
    st=end

syncsum=0
def sinc():
    start_time = time.time()
    for i in mass:
        syncsum+=i
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения в синхронном режиме: {execution_time} секунд")


def flow(mass):
    global sumflow
    summ=0
    for m in mass:
        # sumflow+=m
        summ+=m
    sumflow+=summ



def flows():
    start_time = time.time()
    threads=[]
    for i in ma:
        t=threading.Thread(target=flow(i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения всех потоков: {execution_time} секунд\nСумма={sumflow}")


syncsum=0
def sinc():
    global syncsum
    start_time = time.time()
    for i in mass:
        syncsum+=i
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения в синхронном режиме: {execution_time} секунд\nСумма={syncsum}")

sumprocess=multiprocessing.Value('i',0)

def proces (cnt,mass):
    summ=0
    for i in mass:
        summ+=i
    with cnt.get_lock():
        cnt.value+=summ

def process():
    start_time = time.time()
    processes=[]
    for i in ma:
        p=multiprocessing.Process(target=proces,args=(sumprocess,i,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения в многопроцессорном режиме: {execution_time} секунд\nСумма={sumprocess.value:_}")
sumasync=0
async def asyncc(mass):
    global sumasync
    summ=0
    for i in mass:
        summ+=i
    sumasync+=summ

async def asyncs():
    
    tasks=[asyncio.create_task(asyncc(mass)) for mass in ma]
    await asyncio.gather(*tasks)

def runasync ():
    start_time = time.time()
    asyncio.run(asyncs())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения в асинхронном режиме: {execution_time} секунд\nСумма={sumprocess.value:_}")



if __name__ == "__main__":
    process()
    runasync()
    flows()
    sinc()