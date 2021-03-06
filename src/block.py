class Block:
    def __init__(self, position, mass):
        # a Block is defined by a mass & a velocity.
        # x is the position on x axis
        # negative velocity means the block is moving left.
        # Positive velocity means the block is moving right
        self.x = position
        self.mass = mass
        self.velocity = 0

    def update(self):
        # update position of block based on velocity
        # {and draw block in UI ?}
        # self.x += self.velocity
        # draw block ?
        pass

    def set_velocity(self, velocity):
        self.velocity = velocity

    def collide(self, collider):
        """
        calculates the final velocities for 2 blocks in a perfectly elastic collision.

        --------------------------------------------------------------------------------
            We will be using :

            IV = Initial Velocity
            FV = Final Velocity
            m = mass

            Using 2 equations :

            - [Conservation of kinetic energy] ?
                E1 : collider.IV + collider.FV
                   = self.IV + self.FV

            - Conservation of momentum :
                E2 : collider.m * collider.IV + self.m * self.IV
                   = collider.m * collider.FV + self.m * self.FV
        --------------------------------------------------------------------------------

            E1': collider.IV - self.IV
               = self.FV - collider.FV

        --------------------------------------------------------------------------------
            we then multiply E1' by collider.m
        --------------------------------------------------------------------------------

            E1": collider.m * collider.IV - collider.m * self.IV
               = collider.m * self.FV - collider.m * collider.FV

        --------------------------------------------------------------------------------
            finally we add E2 and E1"
        --------------------------------------------------------------------------------

            E3 : collider.m * collider.IV + self.m * self.IV + (collider.m * collider.IV - collider.m * self.IV)
               = collider.m * collider.FV + self.m * self.FV + (collider.m * self.FV - collider.m * collider.FV)

            <=>  collider.m * collider.IV + collider.m * collider.IV + self.m * self.IV - collider.m * self.IV
               = {collider.m * collider.FV - collider.m * collider.FV} + self.m * self.FV + collider.m * self.FV

            <=>  collider.m * (2 * collider.IV - self.IV) + self.m * self.IV
               = (self.m - collider.m) * self.FV

            E3': self.FV = (collider.m * (2 * collider.IV - self.IV) + self.m * self.IV) / (self.m + collider.m)

        --------------------------------------------------------------------------------
            we can then use E1 to find collider.FV once we have self.FV
        --------------------------------------------------------------------------------
        """
        new_velocity = (collider.mass * (2 * collider.velocity - self.velocity) + self.mass * self.velocity) / (self.mass + collider.mass)
        collider.set_velocity(self.velocity + new_velocity - collider.velocity)
        self.set_velocity(new_velocity)
