import math
import random
import time
from typing import List, Tuple

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, v: 'Vector'):
        self.x += v.x
        self.y += v.y

    def sub(self, v: 'Vector'):
        self.x -= v.x
        self.y -= v.y

    def div(self, scalar: float):
        if scalar != 0:
            self.x /= scalar
            self.y /= scalar

    def mag(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        m = self.mag()
        if m > 0:
            self.div(m)

    def limit(self, max_force: float):
        if self.mag() > max_force:
            self.normalize()
            self.x *= max_force
            self.y *= max_force
            
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

class Boid:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.position = Vector(x, y)
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector(0, 0)
        self.max_speed = 2.0
        self.max_force = 0.03

    def update(self):
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.max_speed)
        self.position.add(self.velocity)
        self.acceleration = Vector(0, 0) # Reset

    def apply_force(self, force: Vector):
        self.acceleration.add(force)

    def flock(self, boids: List['Boid']):
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohesion(boids)

        # Weights
        sep.x *= 1.5; sep.y *= 1.5
        ali.x *= 1.0; ali.y *= 1.0
        coh.x *= 1.0; coh.y *= 1.0

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def separate(self, boids: List['Boid']) -> Vector:
        desired_separation = 2.0
        steer = Vector(0, 0)
        count = 0
        
        for other in boids:
            d = self.dist(other.position)
            if 0 < d < desired_separation:
                diff = Vector(self.position.x, self.position.y)
                diff.sub(other.position)
                diff.normalize()
                diff.div(d) # Weight by distance
                steer.add(diff)
                count += 1
                
        if count > 0:
            steer.div(count)
            steer.normalize()
            steer.x *= self.max_speed; steer.y *= self.max_speed
            steer.sub(self.velocity)
            steer.limit(self.max_force)
            
        return steer

    def align(self, boids: List['Boid']) -> Vector:
        neighbor_dist = 5.0
        sum_v = Vector(0, 0)
        count = 0
        
        for other in boids:
            d = self.dist(other.position)
            if 0 < d < neighbor_dist:
                sum_v.add(other.velocity)
                count += 1
                
        if count > 0:
            sum_v.div(count)
            sum_v.normalize()
            sum_v.x *= self.max_speed; sum_v.y *= self.max_speed
            steering = Vector(sum_v.x, sum_v.y)
            steering.sub(self.velocity)
            steering.limit(self.max_force)
            return steering
            
        return Vector(0, 0)

    def cohesion(self, boids: List['Boid']) -> Vector:
        neighbor_dist = 5.0
        sum_p = Vector(0, 0)
        count = 0
        
        for other in boids:
             d = self.dist(other.position)
             if 0 < d < neighbor_dist:
                sum_p.add(other.position)
                count += 1
                
        if count > 0:
            sum_p.div(count)
            return self.seek(sum_p)
            
        return Vector(0, 0)

    def seek(self, target: Vector) -> Vector:
        desired = Vector(target.x, target.y)
        desired.sub(self.position)
        desired.normalize()
        desired.x *= self.max_speed; desired.y *= self.max_speed
        steer = Vector(desired.x, desired.y)
        steer.sub(self.velocity)
        steer.limit(self.max_force)
        return steer

    def dist(self, v: Vector) -> float:
        return math.sqrt((self.position.x - v.x)**2 + (self.position.y - v.y)**2)

# --- Example Usage ---

if __name__ == "__main__":
    boids = [Boid(i, random.uniform(0, 10), random.uniform(0, 10)) for i in range(5)]
    
    print("--- Simulation Start ---")
    for t in range(3):
        print(f"\nStep {t}:")
        for b in boids:
            b.flock(boids)
            b.update()
            print(f"   🐦 Boid {b.id}: {b.position}")
