from dataclasses import dataclass, field

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: any, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> any:
        return heapq.heappop(self.elements)[1]

class Agent:
    def __init__(self, is_amphibious: bool, isFourByFour: int) -> None:
        self.is_amphibious = is_amphibious
        self.is_four_by_four = isFourByFour


def cost(agent, filters):
    return filters[0] + filters[1]

# loss travelled + loss remaining to dist (manhattan)
class Pathfinder:
    def __init__(self, graph) -> None:
        self.graph = graph

    def reconstruct_path(
            self,
            came_from,
            start, 
            goal
        ):

        current = goal
        path = []
        if goal not in came_from: # no path was found
            print("goal not found")
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path

    def find_ponnection(self, start, end, agent: Agent):
        queue = PriorityQueue()
        queue.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        cost_so_far[end] = float("inf")
        
        while not queue.empty():
            current = queue.get()
            
            if cost_so_far.get(current, 0) > cost_so_far[end]:
                continue
            
            for next in self.get_neighbors(current):
                x, y = next
                filters = self.graph[y][x]
                new_cost = cost_so_far[current] + cost(agent, filters) + 0.01
                if new_cost < cost_so_far.get(next, float("inf")) and new_cost < cost_so_far[end]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.remaining_manhattan_loss(next, end)
                    queue.put(next, priority)
                    came_from[next] = current
        return self.reconstruct_path(came_from, start, end)

    def get_neighbors(self, position):
        deltas = [-1, 0, 1]
        x, y = position
        height, width = len(self.graph), len(self.graph[0])

        neighbors = []
        for dx in deltas:
            for dy in deltas:
                new_x, new_y = x + dx, y + dy
                if dx == 0 and dy == 0: continue
                if new_x < 0 or new_x >= width: continue
                if new_y < 0 or new_y >= height: continue

                neighbors.append((new_x, new_y))
            
        return neighbors
    
    def remaining_manhattan_loss(self, start, end):
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])
        
        bad_but_accept = 1
        return (dx + dy) * bad_but_accept


    def add_used_path(self):
        pass