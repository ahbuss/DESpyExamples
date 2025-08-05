from SimplestShooter import SimplestShooter, Adjudicator, Ship
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper

all_ships = [Ship(), Ship(), Ship()]
number_missiles = 40
response_time = 5
travel_time = 10

simplest_shooter = SimplestShooter(all_ships, number_missiles, response_time, travel_time)
print(simplest_shooter.describe())

prob_destroyed = 0.2;
adjudicator = Adjudicator(prob_destroyed)
print(adjudicator.describe())

simplest_shooter.add_sim_event_listener(adjudicator)
adjudicator.add_sim_event_listener(simplest_shooter)
for ship in all_ships:
    adjudicator.add_sim_event_listener(ship)

simple_state_change_dumper = SimpleStateChangeDumper()
simplest_shooter.add_state_change_listener(simple_state_change_dumper)
adjudicator.add_state_change_listener(simple_state_change_dumper)
for ship in all_ships:
    ship.add_state_change_listener(simple_state_change_dumper)

EventList.verbose = True

EventList.reset()
EventList.start_simulation()

print("Simulation ended at time {t}".format(t=EventList.simtime))
print("it took {n} tries to destroy {s} ships".format(n = adjudicator.number_tries,
                                                      s=len(all_ships) - len(simplest_shooter.remaining_ships)))