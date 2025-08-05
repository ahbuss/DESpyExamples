from simkit.base import SimEntityBase
from math import nan, isnan
from simkit.rand import RandomVariate, DiscreteUniform

class SimplestShooter(SimEntityBase):
    def __init__(self, all_ships, number_missiles, response_time, travelTime):
        SimEntityBase.__init__(self)

        self.all_ships = all_ships.copy()
        self.number_missiles = number_missiles
        self.response_time = response_time
        self.travel_time = travelTime
        self.uniform = RandomVariate.instance("DiscreteUniform", min=0, max=len(all_ships) - 1)

        self.remaining_missiles = nan
        self.remaining_ships = None

    def reset(self):
        SimEntityBase.reset(self)
        self.remaining_ships = self.all_ships.copy()
        self.remaining_missiles = self.number_missiles

    def run(self):
        self.notify_state_change("remaining_ships", self.remaining_ships.copy())
        self.notify_state_change("remaining_missiles", self.remaining_missiles)

        self.schedule("choose_target", self.response_time)

    def choose_target(self):
        index = self.uniform.generate() if len(self.remaining_ships) > 0 else nan
        if not isnan(index):
            target = self.remaining_ships[index]

            self.schedule("launch", 0.0, target)

    def launch(self, target):
        self.remaining_missiles -= 1
        self.notify_state_change("remaining_missiles", self.remaining_missiles)

        self.schedule("impact", self.travel_time, target)

    def impact(self, target):
        if self.remaining_missiles > 0 and  len(self.remaining_ships) > 0:
            self.schedule("choose_target", self.response_time)

    def destroyed(self, target):
        self.remaining_ships.remove(target)
        self.notify_state_change("remaining_ships", self.remaining_ships.copy())

        self.uniform.max = len(self.remaining_ships) - 1


class Adjudicator(SimEntityBase):
    def __init__(self, prob_destroyed):
        SimEntityBase.__init__(self)
        self.prob_destroyed = prob_destroyed
        self.uniform = RandomVariate.instance("Uniform", min=0.0, max=1.0)

        self.number_tries = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_tries = 0;

    def run(self):
        self.notify_state_change("number_tries", self.number_tries)

    def impact(self, target):
        self.number_tries += 1
        self.notify_state_change("number_tries", self.number_tries)
        if self.uniform.generate() < self.prob_destroyed:
            self.schedule("destroyed", 0.0, target)

class Ship(SimEntityBase):
    def __init__(self):
        SimEntityBase.__init__(self)

        self.alive = True

    def reset(self):
        SimEntityBase.reset(self)
        self.alive = True

    def run(self):
        self.notify_state_change("alive", self.alive)

    def destroyed(self, target):
        if target == self:
            self.alive = False
            self.notify_state_change("alive", self.alive)