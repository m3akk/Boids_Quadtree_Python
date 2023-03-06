
import pygame
from random import randint
from random import uniform
from pygame.math import Vector2
from math import pow
from math import sqrt
import math
from math import pi, cos, sin, atan2, degrees, sqrt


# =============================================================
#                       CONSTRAINTS
# =============================================================

Width, Height = 800, 800
Resolution = (Width, Height)

NODE_CAPACITY = 8
RADIUS = 2

SIZE = 200

Black, White = (0, 0, 0), (255, 255, 255)
Color1 = (210, 210, 210)



# =============================================================
#                       PARTICLE
# =============================================================


class Particle:
    def __init__(self, position = Vector2(0, 0), radius=6, color=(255, 255, 255)):
        self.position = position
        self.color = color
        self.radius = radius
        self.highlighted = False
        self.HighlightColor = None

    def move(self):
        self.position.x += uniform(-2, 2)
        self.position.y += uniform(-2, 2)

    def collide(self, other):
        dist = GetDistance(self.position.x, self.position.y, other.position.x, other.position.y)
        if dist < self.radius + other.radius:
            return True
        else:
            return False

    def Highlight(self, color=(0, 255, 255)):
        self.highlighted = True
        self.highlightColor = color

    def draw(self, screen, radius=None):
        _radius = self.radius
        if radius != None:
            _radius = radius

        surface = pygame.Surface((_radius*2, _radius*2), pygame.SRCALPHA, 32)
        r,g, b = self.color
        if self.highlighted == True:
            r, g, b = self.highlightColor
        pygame.draw.circle(surface, (r, g, b, 100), (int(_radius), int(_radius)), _radius)
        pygame.draw.circle(surface, (r, g, b, 255), (int(_radius), int(_radius)), _radius, 1)

        screen.blit(surface, ( int(self.position.x) - _radius, int(self.position.y) - _radius))
        self.highlighted = False


def GetDistance(x1, y1, x2, y2):
    return sqrt( (x2 - x1) * (x2-x1) + (y2 - y1) * (y2 - y1) )



def GetDistanceSQ(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    return  (x2 - x1) * (x2-x1) + (y2 - y1) * (y2 - y1)


# =============================================================
#                       quadtree
# =============================================================


class QuadTree:
    def __init__(self, capacity, boundary, color = (140, 255, 160), thickness=1):
        self.capacity = capacity
        self.boundary = boundary
        self.particles = []
        self.color = color
        self.lineThickness = thickness
        self.northWest = None
        self.northEast = None
        self.southWest = None
        self.southEast = None

    def subdivide(self):
        parent = self.boundary

        boundary_nw = Rectangle(
                Vector2(
                parent.position.x ,
                parent.position.y
                ),
            parent.scale/2
            )
        
        boundary_ne = Rectangle(
                Vector2(
                parent.position.x + parent.scale.x/2,
                parent.position.y
                ),
                parent.scale/2
            )
        
        boundary_sw = Rectangle(
                Vector2(
                parent.position.x,
                parent.position.y + parent.scale.y/2
                ),
                parent.scale/2
            )
        
        boundary_se = Rectangle(
                Vector2(
                parent.position.x + parent.scale.x/2,
                parent.position.y + parent.scale.y/2
                ),
                parent.scale/2
            )

        self.northWest = QuadTree(self.capacity, boundary_nw, self.color, self.lineThickness)
        self.northEast = QuadTree(self.capacity, boundary_ne, self.color, self.lineThickness)
        self.southWest = QuadTree(self.capacity, boundary_sw, self.color, self.lineThickness)
        self.southEast = QuadTree(self.capacity, boundary_se, self.color, self.lineThickness)

        for i in range(len(self.particles)):
            self.northWest.insert(self.particles[i])
            self.northEast.insert(self.particles[i])
            self.southWest.insert(self.particles[i])
            self.southEast.insert(self.particles[i])

    def insert(self, particle):
        if self.boundary.containsParticle(particle) == False:
            return False

        if len(self.particles) < self.capacity and self.northWest == None:
            self.particles.append(particle)
            return True
        else:
            if self.northWest == None:
                self.subdivide()

            if self.northWest.insert(particle):
                return True
            if self.northEast.insert(particle):
                return True
            if self.southWest.insert(particle):
                return True
            if self.southEast.insert(particle):
                return True
            return False

    def queryRange(self, _range):
        particlesInRange = []

        if _range.name == "circle":
            if _range.intersects(self.boundary)==False:
                return particlesInRange
        else:
            if _range.intersects(self.boundary)==True:
                return particlesInRange

        for particle in self.particles:
            if _range.containsParticle(particle):
                particlesInRange.append(particle)
        if self.northWest != None:
            particlesInRange += self.northWest.queryRange(_range)
            particlesInRange += self.northEast.queryRange(_range)
            particlesInRange += self.southWest.queryRange(_range)
            particlesInRange += self.southEast.queryRange(_range)
        return particlesInRange
        

    def Show(self, screen):
        self.boundary.color = self.color
        self.boundary.lineThickness = self.lineThickness
        self.boundary.Draw(screen)
        if self.northWest != None:
            self.northWest.Show(screen)
            self.northEast.Show(screen)
            self.southWest.Show(screen)
            self.southEast.Show(screen)






# =============================================================
#                       RANGE
# =============================================================


class Rectangle:
    def __init__(self, position, scale):
        self.position = position
        self.scale = scale
        self.color = (255, 255, 255)
        self.lineThickness = 1
        self.name = "rectangle"

    def containsParticle(self, particle):
        x, y = particle.position
        bx, by = self.position
        w, h = self.scale
        if x > bx and x < bx+w and y > by and y < by+h:
            return True
        else:
            return False

    def intersects(self,_range):
        x, y = self.position
        w, h = self.scale
        xr, yr = _range.position
        wr, hr = _range.scale
        if xr > x + w or xr+wr < x-w or yr > y + h or yr+hr < y-h:
            return True
        else:
            return False

    def Draw(self, screen):
        x, y = self.position
        w, h = self.scale
        pygame.draw.rect(screen, self.color, [x, y, w, h], self.lineThickness)


# =============================================================
#                       boid
# =============================================================

def Limit(vec, max_mag):
    magsq = Vector2.magnitude_squared(vec)
    temp = vec
    if magsq > (max_mag * max_mag):
        temp = Vector2.normalize(temp)
        temp *= max_mag

    return temp


def Heading(vec):
    angle = atan2(vec.y, vec.x)
    return angle

class Boid:
    def __init__(self, position, flock=None):
        self.position = position
        self.radius = RADIUS
        self.angle = uniform(0, pi*2)
        self.acceleration = Vector2(0, 0)
        self.velocity = Vector2(cos(self.angle), sin(self.angle))
        self.maxSpeed = 4
        self.maxForce = 0.03
        self.flock = flock
        self.stroke = 1
        self.hue = 0

        self.trailStroke = 2
        self.trailLimit = 20
        self.trail = []
        self.counter = 0

    def Simulate(self, boids):
        self.Flock(boids)
        self.Update()
        self.Boundary()

    def ApplyForce(self, f):
        self.acceleration += f

    def Flock(self, boids):
        separation  = self.Separate(boids)
        alignment   = self.Align(boids)
        cohesion    = self.Cohesion(boids)

        separation *= self.flock.separation
        alignment  *= self.flock.alignment
        cohesion   *= self.flock.cohesion

        self.ApplyForce(separation)
        self.ApplyForce(alignment)
        self.ApplyForce(cohesion)



    # def Update(self):
    #     self.velocity += self.acceleration
    #     self.velocity = Limit(self.velocity, self.maxSpeed)
    #     self.position += self.velocity
    #     self.acceleration *= 0
    #     self.angle = Heading(self.velocity) + round(pi/2,2)


    def Update(self):
        self.velocity += self.acceleration
        self.velocity = Limit(self.velocity, self.maxSpeed)
        self.position += self.velocity
        self.acceleration *= 0
        self.angle = Heading(self.velocity) + round(pi/2,2)


        if self.position[0] > Width:
            self.position[0] = Width
            self.velocity[0] *= -1
        elif self.position[0] < 0:
            self.position[0] = 0
            self.velocity[0] *= -1

        if self.position[1] > Height:
            self.position[1] = Height
            self.velocity[1] *= -1
        elif self.position[1] < 0:
            self.position[1] = 0
            self.velocity[1] *= -1





    def Separate(self, boids):
        steering = Vector2(0, 0)
        total = 0
        desired_separation = self.flock.separation_value

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < desired_separation:
                difference = self.position - boid.position
                difference = Vector2.normalize(difference)
                difference /= dist
                steering += difference
                total += 1
                boid.hue = self.flock.HUE

        if total > 0:
            steering /= total

        magnitude = Vector2.magnitude(steering)
        if magnitude > 0:
            steering = Vector2.normalize(steering)
            steering *= self.maxSpeed
            steering -= self.velocity
            steering = Limit(steering, self.maxForce)

        return steering
    


    def Align(self, boids):
        total = 0
        steering = Vector2(0, 0)
        neighbourDistance = self.flock.alignment_value

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < neighbourDistance:
                steering += boid.velocity
                total += 1
                boid.hue = self.flock.HUE * 2


        if total > 0:
            steering /= total
            steering = Vector2.normalize(steering)
            steering *= self.maxSpeed
            steering -= self.velocity
            steering = Limit(steering, self.maxForce)
            return steering
        else:
            return Vector2(0, 0)

    def Cohesion(self, boids):
        neighbourDistance = self.flock.cohesion_value
        total = 0
        steering = Vector2(0, 0)

        for boid in boids:
            dist = Vector2.distance_to(self.position, boid.position)
            if dist > 0 and dist < neighbourDistance:
                steering += boid.position
                total += 1
                boid.hue = self.flock.HUE * 3

        if total > 0:
            steering /= total
            return self.Steer(steering)
        else:
            return Vector2(0, 0)
        
    def Steer(self, target):
        t = target - self.position
        t = Vector2.normalize(t)
        t *= self.maxSpeed
        steer = t - self.velocity
        steer = Limit(steer, self.maxForce)
        return steer


    def Boundary(self):
        if self.position.x < -self.radius:
            self.position.x = Width+self.radius
        if self.position.y < - self.radius:
            self.position.y = Height+self.radius

        if self.position.x > Width + self.radius:
            self.position.x = -self.radius
        if self.position.y > Height+self.radius:
            self.position.y = -self.radius

    def Render(self):
 
        c = pygame.Color(0, 0, 0)
        c.hsva = (self.hue%360, 100, 100, 100)
        color = c

        distance = 5
        scale = 30
        ps = []
        points = [None for _ in range(4)]

        points[0] = [[0],[-self.radius],[0]]
        points[1] = [[self.radius//2],[self.radius//2],[0]]
        points[2] = [[-self.radius//2],[self.radius//2],[0]]
        points[3] = [[0],[0],[0]]

        for point in points:
        	rotated = matrix_multiplication(rotationZ(self.angle) , point)
        	z = 1/(distance - rotated[2][0])
        	projection_matrix = [[z, 0, 0], [0, z, 0]]
        	projected_2d = matrix_multiplication(projection_matrix, rotated)
        	x = int(projected_2d[0][0] * scale) + self.position.x
        	y = int(projected_2d[1][0] * scale) + self.position.y
        	ps.append((x, y))

        if len(self.trail) > self.trailLimit:
            self.trail.pop(0)

        window = self.flock.window
        if self.flock.showTrail:
            if len(self.trail) > 0:
                dist = GetDistanceSQ(self.trail[-1], ps[3])
                if dist > 10:
                    self.trail = []
            self.trail.append(ps[3])
            for i in range(len(self.trail)-1):
                pygame.draw.line(window, color, self.trail[i], self.trail[i+1], self.trailStroke)
        pygame.draw.polygon(window, color, ps[:3])
        pygame.draw.polygon(window, color, ps[:3], self.stroke)


# =============================================================
#                       FLOCK
# =============================================================

class Flock:
    def __init__(self, screen, boids=[]):
        self.boids = boids
        self.separation = 1.2
        self.alignment = 3
        self.cohesion = 1
        self.separation_value = 15
        self.alignment_value = 50
        self.cohesion_value = 55
        self.window = screen
        self.quadTree = None
        self.ActivateQuadtree = True
        self.showRange = False
        self.showTrail = False
        self.HUE = 70
        
    def Simulate(self):
        if self.ActivateQuadtree:
            for boid in self.boids:
                if self.quadTree:
                    self.quadTree.insert(boid)
                boid.Render()

                xx, yy = boid.position
                r = 100


                rangeRect = Rectangle(Vector2(xx - r/2, yy - r/2), Vector2(r, r))
                rangeRect.color = (190, 210, 55)
                rangeRect.lineThickness = 1

                if self.showRange:
                    rangeRect.Draw(self.window)
                others = self.quadTree.queryRange(rangeRect)


                boid.Simulate(others)
        else:
            for boid in self.boids:
                boid.Simulate(self.boids)
                boid.Render()


    def Append(self, boid):
        self.boids.append(boid)



# ============================================================
#                           matrix
# =============================================================




def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix

    else:
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None

def rotationX(angle):
    return [[1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]]
def rotationY(angle):
    return [[math.cos(angle), 0, -math.sin(angle)],
            [0, 1, 0],
            [math.sin(angle), 0, math.cos(angle)]]

def rotationZ(angle):
    return [[math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0 ,1]]



# ============================================================
#                           main
# =============================================================


def main():
    screen = pygame.display.set_mode(Resolution)

    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()
    fps = 1000

    flock = Flock(screen)

    for i in range(SIZE):
        offset = 200
        pos = Vector2(randint(offset, Width-offset), randint(offset, Height-offset))


        flock.Append(Boid(pos, flock))

    showQuadTree = True
    SwitchRange = 1
    run = True
    while run:
        screen.fill(Color1)
        pygame.display.set_caption("Boids")
        clock.tick(fps)

        # create QuadTree
        boundary = Rectangle(Vector2(0, 0), Vector2(Width, Height))

        quadtree = QuadTree(NODE_CAPACITY, boundary)
        quadtree.lineThickness = 1
        quadtree.color = (230,150,10)
        flock.quadTree = quadtree

        # ----- HANDLE EVENTS ------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE:
                    flock.ActivateQuadtree = not flock.ActivateQuadtree
                    notification = " -Space partitioning is Activated- " if flock.ActivateQuadtree else " -Space partitioning is Deactivated- "
                    print(notification)
                if event.key == pygame.K_RETURN or event.key == pygame.K_q:
                    showQuadTree = not showQuadTree
                if event.key == pygame.K_r:
                    flock.showRange = not flock.showRange
                if event.key == pygame.K_t:
                    flock.showTrail = not flock.showTrail
        # -----------------------------

        flock.Simulate()

        if showQuadTree:
            quadtree.Show(screen)

        pygame.display.flip()

    pygame.quit()






if __name__ == "__main__":
    main()
