import queue

from django.contrib.gis.geos import LineString
from .models import LineModel, PointModel


# A star search algorithm (A*).
# Finds shortest path in graph provided certain priority func.
# Works only in all-linked graph
def a_star(start_point, goal_point, priority_func, initial_priority=0):
    class QueueItem:
        def __init__(self, priority, current_point, previous_point):
            self.priority = priority
            self.current_point = current_point
            self.previous_point = previous_point

        def __lt__(self, other):
            return self.priority < other.priority

        def __eq__(self, other):
            return self.priority == other.priority

    visited_points = []
    priority_queue = queue.PriorityQueue()
    # (priority, current_point, previous_point)
    priority_queue.put(QueueItem(initial_priority, start_point, None))
    while not priority_queue.empty():
        item = priority_queue.get()
        current_priority, current, previous = item.priority, item.current_point, item.previous_point
        if current in [v[0] for v in visited_points]:
            continue
        visited_points.append((current, previous))
        if current == goal_point:
            break
        # get all neighbours
        neighbours = [line.to_point for line in current.from_point.all()] + \
                     [line.from_point for line in current.to_point.all()]
        for vertex in neighbours:
            if vertex in [v[0] for v in visited_points]:
                continue
            pr = priority_func(current=current,
                               inserted=vertex,
                               goal=goal_point,
                               current_priority=current_priority)
            priority_queue.put(QueueItem(pr, vertex, current))
    path = []
    p = current
    while p is not None:
        path.append(p)
        for it in visited_points:
            if it[0] == p:
                p = it[1]
    path.reverse()
    return path


# Returns dictionary containing LineString that connects points p1 and p2 in graph.
# Has least distance cost (total length of included edges).
# Return value:
# {
#     'line': <LineString>,
#     'length': <float>
# }
def get_line_min_distance(p1, p2):
    def priority_func(current, inserted, goal, current_priority):
        return current_priority + current.geom.distance(inserted.geom) + \
               inserted.geom.distance(goal.geom) - current.geom.distance(goal.geom)

    points = a_star(p1, p2, priority_func, initial_priority=p1.geom.distance(p2.geom))
    line = LineString([p.geom for p in points])
    return {'line': line, 'length': line.length}


# Returns dictionary containing LineString that connects points p1 and p2 in graph.
# Has least score cost (total score of included points).
# Return value:
# {
#     'line': <LineString>,
#     'score': <int>
# }
def get_line_min_score(p1, p2):
    def priority_func(current, inserted, goal, current_priority):
        if inserted == goal:
            return current_priority
        return current_priority + inserted.score

    points = a_star(p1, p2, priority_func, initial_priority=p1.score)
    line = LineString([p.geom for p in points])
    return {'line': line, 'score': sum([p.score for p in points])}
