from dataclasses import dataclass, field

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, any]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: any, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> any:
        return heapq.heappop(self.elements)[1]

class MapFilters:
    def __init__(self, water_depth) -> None:
        self.water_depth = water_depth



class Position:
    def __init__(self, x, y, filters) -> None:
        self.x = x
        self.y = y
        self.filters = filters
    
    def __lt__(self, other):
        return (self.x + self.y) < (other.x + other.y)
    
    def __repr__(self) -> str:
        return f"Position(x={self.x}, y={self.y})"
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

class Agent:
    def __init__(self, is_amphibious: bool, isFourByFour: int) -> None:
        self.is_amphibious = is_amphibious
        self.is_four_by_four = isFourByFour


def cost(agent, filter):
    return 1

# loss travelled + loss remaining to dist (manhattan)
class Pathfinder:
    def __init__(self, graph: list[list[Position]]) -> None:
        self.graph = graph

    def reconstruct_path(
            self,
            came_from: dict[Position, Position],
            start: Position, 
            goal: Position
        ) -> list[Position]:

        current: Position = goal
        path: list[Position] = []
        if goal not in came_from: # no path was found
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start) # optional
        path.reverse() # optional
        return path

    def find_ponnection(self, start: Position, end: Position, agent: Agent):
        queue = PriorityQueue()
        queue.put(start, 0)
        came_from: dict[Position, Position] = {}
        cost_so_far: dict[Position, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0
        
        while not queue.empty():
            current: Position = queue.get()
            
            if current.x == end.x and current.y == end.y:
                break
            
            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + cost(agent, next.filters)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.remaining_manhattan_loss(next, end)
                    queue.put(next, priority)
                    came_from[next] = current
        return self.reconstruct_path(came_from, start, end), cost_so_far[end]

    def get_neighbors(self, position: Position):
        deltas = [-1, 0, 1]
        x, y = position.x, position.y
        height, width = len(self.graph), len(self.graph[0])

        neighbors = []
        for dx in deltas:
            for dy in deltas:
                new_x, new_y = x + dx, y + dy
                if dx == 0 and dy == 0: continue
                if new_x < 0 or new_x >= width: continue
                if new_y < 0 or new_y >= height: continue

                neighbors.append(self.graph[new_y][new_x])
            
        return neighbors
    
    def remaining_manhattan_loss(self, start: Position, end: Position):
        dx = abs(end.x - start.x)
        dy = abs(end.y - start.y)
        
        bad_but_accept = 1
        return (dx + dy) * bad_but_accept


    def add_used_path(self):
        pass


graph = []
for y in range(10):
    row = []
    for x in range(10):
        row.append(Position(x, y, None))
    graph.append(row)

agent = Agent(False, 0)

pathfinder = Pathfinder(graph)

start = Position(1, 1, None)
end = Position(4, 5, None)

path, curr_cost = pathfinder.find_ponnection(start, end, agent)
for p in path:
    print(p.x, "  ", p.y)
print(curr_cost)