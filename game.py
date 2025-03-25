import pygame
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Physics constants
GRAVITY = 9.81
AIR_DENSITY = 1.225
WING_AREA = 20  # m²
LIFT_COEFFICIENT = 1.2
DRAG_COEFFICIENT = 0.05
MASS = 1500  # kg
THRUST_FORCE = 20000  # Newtons

class Plane:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.pitch = 0  # Degrees
        self.roll = 0
        self.speed = 100  # m/s
        self.altitude = 1000  # meters
        self.throttle = 0.2
        self.fuel = 1000  # kg

    def calculate_forces(self):
        # Calculate lift
        dynamic_pressure = 0.5 * AIR_DENSITY * self.speed**2
        lift = dynamic_pressure * WING_AREA * LIFT_COEFFICIENT * math.cos(math.radians(self.pitch))
        
        # Calculate drag
        drag = dynamic_pressure * WING_AREA * DRAG_COEFFICIENT * math.sin(math.radians(self.pitch))
        
        # Thrust force
        thrust = THRUST_FORCE * self.throttle
        
        # Net vertical force
        self.net_force = lift - (MASS * GRAVITY) - drag
        
        # Calculate acceleration
        self.acceleration = self.net_force / MASS

    def update(self, dt):
        self.calculate_forces()
        
        # Update speed
        self.speed += self.acceleration * dt
        if self.speed < 0:
            self.speed = 0
            
        # Update altitude
        self.altitude += self.speed * dt - 0.5 * GRAVITY * dt**2
        
        # Update position
        self.y += self.speed * math.sin(math.radians(self.pitch)) * dt
        self.x += self.speed * math.cos(math.radians(self.pitch)) * dt
        
        # Fuel consumption
        self.fuel -= THRUST_FORCE * self.throttle * dt * 0.1

# Initialize plane
plane = Plane()

# Main loop
running = True
dt = 0
while running:
    screen.fill((0, 0, 50))  # Dark blue background
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                plane.throttle = min(plane.throttle + 0.1, 1.0)
            if event.key == pygame.K_DOWN:
                plane.throttle = max(plane.throttle - 0.1, 0.0)
            if event.key == pygame.K_LEFT:
                plane.pitch = max(plane.pitch - 5, -90)
            if event.key == pygame.K_RIGHT:
                plane.pitch = min(plane.pitch + 5, 90)

    # Update physics
    plane.update(dt)
    dt = clock.tick(30) / 1000  # Time delta in seconds

    # Draw plane
    pygame.draw.polygon(screen, (255, 0, 0), [
        (plane.x, plane.y),
        (plane.x + 50, plane.y + 20),
        (plane.x + 50, plane.y - 20)
    ])
    
    # Draw horizon
    horizon_y = HEIGHT // 2 + plane.pitch * 2
    pygame.draw.line(screen, (0, 255, 0), (0, horizon_y), (WIDTH, horizon_y), 3)
    
    # Display information
    info = f"Altitude: {plane.altitude:.0f}m | Speed: {plane.speed:.0f}m/s | Throttle: {plane.throttle*100:.0f}% | Pitch: {plane.pitch}°"
    text = font.render(info, True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
