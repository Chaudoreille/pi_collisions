class Block {
    def __init__(position, mass) :
        self.x = x
        self.mass = mass
        self.velocity = 0

    def update() :
        self.x += velocity
        ## draw block

    def setVelocity(velocity) :
        self.velocity = velocity

    def collide(collider : Block) :
        newVelocity = (collider.mass * (2 * collider.velocity - self.velocity) + self.mass * self.velocity) / (self.mass + collider.mass)
        collider.setVelocity(self.velocity + newVelocity - collider.velocity)
        this.setVelocity(newVelocity)

}
