from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    def ssp_helper(visited,frontier):
        if len(frontier)==0:
            return visited
        else:
            # pick next node with minimum distance from heap
            distance, node_edges = heappop(frontier)
            node = node_edges[0]
            edges = node_edges[1]
            if node in visited:
                # Already visited, if it is same as min distance first and has fewer edges
                # update visited with this node 
                if visited[node][0]==distance and visited[node][1]>edges:
                    visited[node]=(distance,edges)
                return ssp_helper(visited,frontier)
            else:
                # Not visited, then update the node to visited
                visited[node]=(distance,edges) 
                for neighbor, weight in graph[node]:
                    # update the frontier
                    heappush(frontier,(distance+weight,(neighbor,edges+1)))
                return ssp_helper(visited,frontier)

    frontier=[]
    heappush(frontier,(0,(source,0))) # initialize the frontier, first 0 is distance, second 0 is num of edges
    visited=dict() # store final result
    return ssp_helper(visited,frontier)
    pass
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    ###TODO
    def bfs_path_helper(visited, frontier,path):
        if len(frontier)==0:
            return path
        else:
            visited=visited|frontier # update the visited set
            frontier_new=set()
            for node in frontier:
                for neighbor in graph[node]:
                # find the neighbors of frontier
                    if neighbor not in visited:
                        # make update if the neighbor is not visited 
                        path[neighbor]=node
                        frontier_new.add(neighbor)   
            return bfs_path_helper(visited, frontier_new, path)
        
    visited=set()
    frontier=set([source])
    path=dict()
    return bfs_path_helper(visited,frontier,path)
    pass

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    ###TODO
    def get_path_helper(res,destination):
        if destination==None:
            return res
        else:
            checker=0 # use to check if the destination can be traced back
            for parent in parents:
                if parent==parents[destination]:
                    # trace back the path
                    destination=parent
                    res=parents[destination]+res
                    checker+=1
            if checker!=1:
                destination=None
            return get_path_helper(res,destination)
         
    res=parents[destination]
    return get_path_helper(res,destination)
    pass

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
