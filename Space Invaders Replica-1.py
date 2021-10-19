
import tkinter
import turtle
import os
import math
import random


class Drawable:

    def __init__(self, color, shape, x, y):
        self.turtle = turtle.Turtle()
        self.turtle.color(color)
        self.turtle.shape(shape)
        self.x = x
        self.y = y
        self.turtle.penup()
        self.turtle.speed(0)

    def draw(self):
        self.turtle.setposition(self.x, self.y)

    def show(self):
        self.turtle.showturtle()

    def hide(self):
        self.turtle.hideturtle()


class Collidable(Drawable):

    def is_collision(self, other):
        distance = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
        if distance < 45:
            return True
        else:
            return False


class Enemy(Collidable):

    def __init__(self):
        super().__init__("red", "rsz-virus.gif", 0, 0)
        self.enemySpeed = 10
        self.reset()

    def update(self):
        # Move the enemy
        self.x += self.enemySpeed

        # Move the enemy back and down
        if self.x > 280:
            # Move all enemies down together
            self.y -= 40
            self.enemySpeed *= -1

        if self.x < -280:
            self.y -= 40
            self.enemySpeed *= -1
        self.draw()

    def reset(self):
        self.x = random.randint(-200, 200)
        self.y = random.randint(100, 250)


class Bullet(Collidable):

    def __init__(self):
        super().__init__('red', "circle", 0, 0)
        self.ready = True
        # Create the player's bullets
        self.turtle.setheading(90)
        self.turtle.shapesize(0.5, 0.5)
        self.turtle.hideturtle()
        self.speed = 30

    def hide(self):
        self.ready = True
        self.x, self.y = (0, -400)
        super().hide()

    def fire_bullet(self):
        if self.ready:
            # Declare BulletState as a global if it needs changed
            #os.system("aplay SoundEffect.wav&")
            self.ready = False
            # Move the bullet to the just above the player
            self.y += 10
            self.show()

    def is_collision(self, other):
        if self.ready:
            return False
        return super().is_collision(other)

    def update(self, player):
        if self.ready:
            self.x = player.x
            self.y = player.y
        if not self.ready:
            self.y += self.speed
        self.draw()


class Player(Collidable):

    def __init__(self):
        super().__init__("blue", "globerotate.gif", 0, -250)
        # Create the player Turtle
        self.speed = 45
        self.turtle.setheading(90)
        self.draw()

    # move the player right and left
    # also included: Boundary Checking
    def move_left(self):
        self.x -= self.speed
        if self.x < -280:
            self.x = -280
        self.draw()

    def move_right(self):
        self.x += self.speed
        if self.x > 280:
            self.x = 280
        self.draw()


# set up the screen
wn = turtle.Screen()
wn.bgcolor("Black")
wn.title("Corona Invaders")
wn.bgpic("spaceBackground.gif")

# Register the Shapes
turtle.register_shape("rsz-virus.gif")
turtle.register_shape("globerotate.gif")

# Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("White")
border_pen.penup()
border_pen.setposition(-300, -300)

border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the Score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("White")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

player = Player()
bullet = Bullet()
# Choose a number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the Enemy
    enemies.append(Enemy())

# Create keyboard bindings
turtle.listen()
turtle.onkey(player.move_left, "Left")
turtle.onkey(player.move_right, "Right")
turtle.onkey(bullet.fire_bullet, "space")

# Main Game Loop
while True:
    bullet.update(player)

    for enemy in enemies:
        enemy.update()
        # Check to see if the bullet has gone to the top
        if bullet.y > 275:
            bullet.hide()

        # Check for collision between bullet and enemy
        if bullet.is_collision(enemy):
            # Reset the Bullet
            bullet.hide()
            # Reset the Enemy
            enemy.reset()
            # Update the Score
            score += 10
            score_string = "Score: %s" % score
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        if player.is_collision(enemy):
            player.hide()
            enemy.hide()
            print("Game Over")
            break
