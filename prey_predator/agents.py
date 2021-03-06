from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        alive = True

        if self.model.grass: 

            self.energy -= 1

            # Eating
            cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                grass_patch.fully_grown = False
                self.energy += self.model.sheep_gain_from_food

            # Dying
            if self.energy < 0:
                alive = False
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)

        if alive and self.random.random() < self.model.sheep_reproduce:
            # Reproducing:
            self.energy /= 2
            baby = Sheep(self.model.next_id(), self.pos, self.model, self.moore, self.energy / 2)
            self.model.grid.place_agent(baby, self.pos)
            self.model.schedule.add(baby)
        


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 5

        # Eating
        cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Dying
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        # Reproducing
        else:
            if self.random.random() < self.model.wolf_reproduce:
                self.energy /= 2
                baby = Wolf(self.model.next_id(), self.pos, self.model, self.moore, self.energy / 2)
                self.model.grid.place_agent(baby, baby.pos)
                self.model.schedule.add(baby)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)

        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):

        if not self.fully_grown:
            if self.countdown > 0:
                self.countdown -= 1     
            else:
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
                

