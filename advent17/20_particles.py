import math

from Util import test, from_file


class Particle:
    def __init__(self, num, x, y, z, vx, vy, vz, ax, ay, az):
        self.num = num
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.vx = int(vx)
        self.vy = int(vy)
        self.vz = int(vz)
        self.ax = int(ax)
        self.ay = int(ay)
        self.az = int(az)

        self.min_speed = 1000000000
        self.min_dist = 1000000000
        self.min_found = False

    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

        distance = abs(self.z) + abs(self.y) + abs(self.x)
        length = math.sqrt(self.vz ** 2 + self.vy ** 2 + self.vx ** 2)

        if length < self.min_speed:
            self.min_speed = length

        if distance < self.min_dist:
            self.min_dist = distance
        else:
            if length > self.min_speed:
                self.min_found = True

    def __str__(self):
        return "%3d: min d: %3s, min s: %0.3f" % (self.num, self.min_dist, self.min_speed)


def parse(lines):
    particles = []

    for i, line in enumerate(lines):
        p, v, a = line.strip().split(", ")

        x, y, z = p[3:-1].split(",")
        vx, vy, vz = v[3:-1].split(",")
        ax, ay, az = a[3:-1].split(",")

        particles.append(Particle(i, x, y, z, vx, vy, vz, ax, ay, az))

    return particles


def simulate_brut(lines):
    particles = parse(lines)
    steps = 0

    while steps < 2000:

        min_dist = 100000000
        min_part = {}
        for particle in particles:
            particle.update()

            distance = abs(particle.z) + abs(particle.y) + abs(particle.x)

            if distance < min_dist:
                min_dist = distance
                if min_dist not in min_part:
                    min_part[min_dist] = []
                min_part[min_dist].append(particle.num)

        print("On step %d: %d min particles at dist %d: %s" % (steps, len(min_part[min_dist]), min_dist, min_part[min_dist]))
        steps += 1

    print("min dist: %d" % min_dist )
    return min_part[min_dist][0]



def simulate_brut_part_2(lines):
    particles = parse(lines)
    steps = 0

    while steps < 2000:
        collisions = {}
        for particle in particles:
            particle.update()

            coord = (particle.x, particle.y, particle.z)
            if coord not in collisions:
                collisions[coord] = []
            collisions[coord].append(particle)

        particles = []
        for sub_particles in collisions.values():
            if len(sub_particles) > 1:
                continue
            particles.append(sub_particles[0])

        print("On step %d: %d particles left" % (steps, len(particles)))
        steps += 1

    return len(particles)


def main():
    # test(0, simulate(from_file("test_inputs/20_particles")))
    #
    # answer = simulate(from_file("inputs/20_particles"))
    test(344, simulate_brut(from_file("inputs/20_particles")))

    print(simulate_brut_part_2(from_file("inputs/20_particles")))


if __name__ == '__main__':
    main()
