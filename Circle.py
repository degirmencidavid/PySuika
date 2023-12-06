# Circle
import pygame as pg

class Circle(pg.sprite.Sprite):
    
    # Constructor
    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.diameter = 2 * radius
        self.image = pg.Surface((self.diameter, self.diameter), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pg.math.Vector2(0, 0)
        self.acceleration = pg.math.Vector2(0, 3)

    def update(self, WIDTH, HEIGHT, bucket_rect, circles, score_counter):
        # Update position based on velocity and acceleration
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

       # Collision with bucket edges
        if self.rect.left <= bucket_rect.left or self.rect.right >= bucket_rect.right:
            self.velocity.x *= -1  # Reverse direction when hitting bucket edges

        if self.rect.bottom + self.radius >= bucket_rect.bottom + self.radius:
            # Calculate the contact point between circumference and bucket's base
            delta_y = self.rect.bottom + self.radius - bucket_rect.bottom - self.radius
            self.rect.y -= delta_y

            # Only stop the circle if it's moving downward and the velocity is below a threshold
            if self.velocity.y > 0 and abs(self.velocity.y) < 1:
                self.velocity.y = 0  # Stop the circle

        # Ensure the circle stays within the bucket's walls horizontally
        if self.rect.left < bucket_rect.left:
            self.rect.left = bucket_rect.left
        elif self.rect.right > bucket_rect.right:
            self.rect.right = bucket_rect.right

        # Collision between circles to combine
        for other_circle in circles:
            if other_circle != self and self.check_collision(other_circle):
                if self.radius == other_circle.radius:
                    new_circle, removed_circle_radius = self.combine(other_circle)
                    if new_circle:
                        circles.remove(self)
                        circles.remove(other_circle)
                        score_counter.increase_score(removed_circle_radius)
                        circles.append(new_circle)
                        break

        # Physics collision between circles
        for other_circle in circles:
            if other_circle != self and self.check_collision(other_circle):
                self.handle_collision(other_circle)

        # Apply friction to velocities
        friction_coefficient = 0.1  # Adjust the friction coefficient as needed
        self.velocity *= (1 - friction_coefficient)
        


    def check_collision(self, other_circle):
        distance = ((self.rect.centerx - other_circle.rect.centerx) ** 2 +
                    (self.rect.centery - other_circle.rect.centery) ** 2) ** 0.5
        combined_radii = self.radius + other_circle.radius
        return distance <= combined_radii


    def combine(self, other_circle):
        if self.radius == other_circle.radius:
            distance = ((self.rect.centerx - other_circle.rect.centerx) ** 2 +
                        (self.rect.centery - other_circle.rect.centery) ** 2) ** 0.5
            if distance <= self.radius + other_circle.radius:
                combined_radius = int(1.5 * self.radius)
                new_x = (self.rect.centerx + other_circle.rect.centerx) // 2
                new_y = (self.rect.centery + other_circle.rect.centery) // 2
                new_circle = Circle(new_x, new_y, combined_radius)
                return new_circle, self.radius  # Return the new circle and removed circle radius
        return None, None


    
    def calculate_collision_velocities(self, other_circle):
        # Calculate velocities after collision (simple elastic collision)
        v1 = self.velocity
        v2 = other_circle.velocity
        m1 = self.radius ** 2  # Consider the radius as mass for simplicity
        m2 = other_circle.radius ** 2

        v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        v2f = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

        return v1f, v2f
    
    def handle_collision(self, other_circle):
        # Calculate the normal and tangent vectors
        normal = pg.Vector2(other_circle.rect.center) - pg.Vector2(self.rect.center)
        distance = normal.length()
        normal /= distance  # Normalize
        tangent = pg.Vector2(-normal.y, normal.x)

        # Calculate the overlap distance
        overlap = (self.radius + other_circle.radius) - distance

        # Resolve the overlap
        self.rect.x -= overlap * normal.x / 2
        self.rect.y -= overlap * normal.y / 2
        other_circle.rect.x += overlap * normal.x / 2
        other_circle.rect.y += overlap * normal.y / 2

        # Calculate velocities in terms of normal and tangent components
        self_velocity = self.velocity.dot(normal)
        other_velocity = other_circle.velocity.dot(normal)

        # Calculate new velocities after collision in terms of normal and tangent components
        self_final_velocity = ((self_velocity * (self.radius - other_circle.radius)) + (2 * other_circle.radius * other_velocity)) / (self.radius + other_circle.radius)
        other_final_velocity = ((other_velocity * (other_circle.radius - self.radius)) + (2 * self.radius * self_velocity)) / (self.radius + other_circle.radius)

        # Convert normal and tangent components back to vectors
        self_velocity_vector = self_final_velocity * normal
        other_velocity_vector = other_final_velocity * normal

        # Update velocities for both circles
        self.velocity -= self.velocity.dot(normal) * normal
        other_circle.velocity -= other_circle.velocity.dot(normal) * normal
        self.velocity += self_velocity_vector
        other_circle.velocity += other_velocity_vector

        # Move circles to avoid overlapping (optional but recommended)
        overlap = (self.radius + other_circle.radius) - distance
        self.rect.x -= overlap * normal.x / 2
        self.rect.y -= overlap * normal.y / 2
        other_circle.rect.x += overlap * normal.x / 2
        other_circle.rect.y += overlap * normal.y / 2

        def apply_friction(self, friction_coefficient):
            # Reduce velocity components by a certain amount (friction)
            self.velocity *= (1 - friction_coefficient)