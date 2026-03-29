#!/usr/bin/env python3
"""tsp_solver - TSP solvers: brute force (small), nearest neighbor, 2-opt."""
import sys, math, itertools

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def brute_force(cities):
    n = len(cities)
    if n > 10: raise ValueError("Too many cities for brute force")
    best = float('inf')
    best_tour = None
    for perm in itertools.permutations(range(n)):
        d = sum(distance(cities[perm[i]], cities[perm[i+1]]) for i in range(n-1))
        d += distance(cities[perm[-1]], cities[perm[0]])
        if d < best:
            best = d
            best_tour = list(perm)
    return best, best_tour

def nearest_neighbor(cities, start=0):
    n = len(cities)
    visited = {start}
    tour = [start]
    current = start
    total = 0
    for _ in range(n - 1):
        nearest = min((i for i in range(n) if i not in visited),
                      key=lambda i: distance(cities[current], cities[i]))
        total += distance(cities[current], cities[nearest])
        visited.add(nearest)
        tour.append(nearest)
        current = nearest
    total += distance(cities[current], cities[start])
    return total, tour

def two_opt(cities, tour):
    n = len(tour)
    improved = True
    def tour_dist(t):
        return sum(distance(cities[t[i]], cities[t[(i+1)%n]]) for i in range(n))
    best = tour_dist(tour)
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                d = tour_dist(new_tour)
                if d < best - 1e-9:
                    tour = new_tour
                    best = d
                    improved = True
    return best, tour

def test():
    cities = [(0,0), (1,0), (1,1), (0,1)]  # square
    d, tour = brute_force(cities)
    assert abs(d - 4.0) < 1e-6
    d2, tour2 = nearest_neighbor(cities)
    assert d2 <= 5.0  # reasonable
    d3, tour3 = two_opt(cities, tour2)
    assert abs(d3 - 4.0) < 1e-6  # 2-opt should find optimal for square
    print("tsp_solver: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: tsp_solver.py --test")
