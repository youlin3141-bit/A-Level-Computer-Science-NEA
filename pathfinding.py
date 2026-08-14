import random
INFINITY=float("inf")
def astar(start,finish,map):
    pathfinding_list=[start]#list of considerable tilels
    previous_tile={}#dictionary of previous tiles
    actual_cost={start:0}#dictionary of "cost" from each ttile
    total_cost={start:heuristic(start,finish)}#dictiionary of heuristic length+width
    while pathfinding_list:
        current=min(pathfinding_list,key=lambda tile:total_cost.get(tile,INFINITY))#smallest based on key value .get(none existent)=inf
        if current==finish:#best path found
            return create_path(previous_tile,current)
        pathfinding_list.remove(current)  #remove unsuccessful path
        for neighbour in get_neighbours(current,map):
            new_actual_cost=actual_cost[current]+1#calculate new cost
            if new_actual_cost<actual_cost.get(neighbour,INFINITY):#if new cost is faster,
                previous_tile[neighbour]=current#backtrack for current tile to be the new prior step
                actual_cost[neighbour]=new_actual_cost#updates the cost to the new cost
                total_cost[neighbour]=heuristic(finish,neighbour)+new_actual_cost#A*: f(n)=g(n)+h(n)
                if neighbour not in pathfinding_list:
                    pathfinding_list.append(neighbour)#no repeat neighbours
    return None
def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])#manhatten distance
def get_neighbours(tile,map):
    x,y=tile
    possible_neighbours=[
        (x+1,y),
        (x+1,y+1),
        (x+1,y-1),
        (x-1,y),
        (x-1,y-1),
        (x-1,y+1),
        (x,y+1),
        (x,y-1),
    ]
    neighbours=[]
    for nx,ny in possible_neighbours:
        if nx<0 or nx>=len(map[0]):
            continue
        if ny<0 or ny>=len(map):
            continue
        if map[ny][nx]!=0:
            neighbours.append((nx,ny))
        random.shuffle(neighbours)
    return neighbours
def create_path(previous_tile,current):
    path=[current]
    while current in previous_tile:
        current=previous_tile[current]#working backwards to find the goal
        path.append(current)
    path.reverse()
    return path
