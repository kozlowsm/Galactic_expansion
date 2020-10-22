import tkinter as tk
import time
from random import randint, uniform, random
import math

# Main Input

# location of galactic empire homeworld on map
HOME_WORLD_LOC = (200, 225)

# maximum number of years to simulate
MAX_YEARS = 1000000

# average exapsnion velocity as fraction of speed of light:
SPEED = .00012
MILES_PER_SECOND = 186000 * SPEED

# scale units
UNIT = 100

# setup the display canvas
root = tk.Tk()  # Root is the top level that will hold everything else
root.title('Milky Way Galaxy')
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

# Actual Milky way dimensions (light-years)
DISC_RADIUS = 50000
disc_radius_scaled = round(DISC_RADIUS/UNIT)


def polar_coordinates():
    """Generate uniform random (x,y) point within a disc for 2D display"""
    r = random()
    theta = uniform(0, 2*math.pi)
    x = round(math.sqrt(r) * math.cos(theta) * disc_radius_scaled)
    y = round(math.sqrt(r) * math.sin(theta) * disc_radius_scaled)
    return x, y


def spirals(b, r, rot_fac, fuz_fac, arm):
    """Build spiral arms for tkinter display using logaritmic spiral formula

    b = arbitrary constant in logarithmic spiral equation
    r = scaled galactic disc radius
    rot_fac = rotation factor
    fuz_fac = random shift in star position in arm, applied to 'fuzz' variable
    arm = spiral arm (0 = main arm, 1 = trailing stars)
    """

    spiral_stars = []
    fuzz = int(0.030 * abs(r))  # randomly shift star locations
    theta_max_degrees = 520
    for i in range(0, theta_max_degrees):  # range(0,600,2) for no blackhole
        theta = math.radians(i)
        x = r*math.exp(b*theta)*math.cos(theta+math.pi*rot_fac) + \
            randint(-fuzz, fuzz) * fuz_fac
        y = r*math.exp(b*theta)*math.sin(theta+math.pi*rot_fac) + \
            randint(-fuzz, fuzz) * fuz_fac
        spiral_stars.append((x, y))
    for x, y in spiral_stars:
        if arm == 0 and int(x % 2) == 0:
            c.create_oval(x-2, y-2, x+2, y+2, fill='white', outline='')
        elif arm == 0 and int(x % 2) != 0:
            c.create_oval(x-1, y-1, x+1, y+1, fill='white', outline='')
        elif arm == 1:
            c.create_oval(x, y, x, y, fill='white', outline='')


def star_haze(scalar):
    """Randomly distribute faint tkinter stars in galatic disc

      disc_radius_scaled = galactic disc radius scaled to radio bubble diameter
      density = multiplier to vary number of stars posted
    """

    for i in range(0, disc_radius_scaled*scalar):
        x, y = polar_coordinates()
        c.create_text(x, y, fill='white', font=('Helvetica', '7'), text='.')


def model_expansion():
    """Model empire expansion from homeworld with concentric rings."""
    r = 0  # radius from homeworld
    text_y_loc = -270
    x, y = HOME_WORLD_LOC
    c.create_oval(x-5, y-5, x+5, y+5, fill='red')
    increment = round(MAX_YEARS / 10)  # Year interval to post circles
    c.create_text(-475, -350, anchor='w', fill='red',
                  text='Increment = {:,}'.format(increment))
    c.create_text(-475, -325, anchor='w', fill='red',
                  text='Velocity as fraction of light = {:,}'.format(SPEED))
    c.create_text(-475, -300, anchor='w', fill='red',
                  text='Traveling at {:,} Miles/Sec'.format(MILES_PER_SECOND))
    c.create_text(HOME_WORLD_LOC[0], HOME_WORLD_LOC[1], fill='red', anchor='w',
                  text="------------------------------- HOME WORLD")

    for years in range(increment, MAX_YEARS+1, increment):
        time.sleep(0.5)  # delay before posting new expansion circle
        traveled = SPEED * increment / UNIT
        r = r + traveled
        c.create_oval(x-r, y-r, x+r, y+r, fill='', outline='red', width='1')
        c.create_text(-475, text_y_loc, anchor='w', fill='red',
                      text='Years = {:,}'.format(years))
        text_y_loc += 20
        # update canvas for new Circle; no longer need mainloop
        c.update_idletasks()
        c.update()


def main():
    """Calculate detection probabilty and post galaxy dispaly and statistics """

    # Build 4 main spiral arms and 4 trailing arms
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=-2, fuz_fac=2, arm=0)
    spirals(b=-0.3, r=disc_radius_scaled, rot_fac=1.91, fuz_fac=1.5, arm=1)

    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=2, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-2.09, fuz_fac=1.5, arm=1)

    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=0.4, fuz_fac=1.5, arm=1)

    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.5, fuz_fac=1.5, arm=0)
    spirals(b=-0.3, r=-disc_radius_scaled, rot_fac=-0.6, fuz_fac=1.5, arm=1)
    star_haze(scalar=9)

    model_expansion()

    # run tkinter loop
    root.mainloop()


if __name__ == '__main__':
    main()
