from statemachine import StateMachine, State
from statemachine.exceptions import InvalidDefinition


# Create elevator class to set key parameters and define methods to operate elevator. Utilized python state machine
# framework to help with maintaining state here. Please see these docs for official documentation:
# https://python-statemachine.readthedocs.io/en/latest/readme.html#a-more-useful-example
# https://pypi.org/project/python-statemachine/

class Elevator:
    def __init__(self, num_floors=2, door_open=False, max_occupancy=10, door_closed=False):
        self.door_open = door_open
        self.door_closed = door_closed
        self.num_floors = num_floors
        self.max_occupancy = max_occupancy

    def push_button(self):
        self.open_doors()

    def open_doors(self):
        self.door_open = True
        self.door_closed = False

    def close_doors(self):
        self.door_open = False
        self.door_closed = True


class ElevatorControl(StateMachine):
    # set states of the elevator
    idle_state = State(initial=True, enter="push_button")
    button_pushed = State()
    # internal button too
    opening_gates = State()
    transporting = State()
    closing_gates = State()
    finished_trip = State(final=True)

    elevator_requested = idle_state.to(button_pushed)
    opened_gates = (
            button_pushed.to(opening_gates, cond="door_open")
            | button_pushed.to(button_pushed, unless="door_open")
    )
    transporting_persons = (
            opening_gates.to(transporting, cond="transport")
            | opening_gates.to(opening_gates, unless="transport")
    )
    finishing_transport = transporting.to(closing_gates, cond="door_closed")
    completed_transport = closing_gates.to(finished_trip)

    def __init__(self, elevator_available=False, transport_active=False):
        self.current_floor = 1
        self.elevator_available = elevator_available
        self.transport_active = transport_active
        super(ElevatorControl, self).__init__()

    def transport(self, end_floor):
        self.transport_active = True
        self.elevator_available = False
        self.current_floor = end_floor


# instantiate elevator classes
new_elevator = Elevator(num_floors=2)
new_elevator_control = ElevatorControl(elevator_available=False)

# run elevator
new_elevator_control.elevator_available = False
new_elevator.push_button()
new_elevator_control.finishing_transport

# %%

# add in loop from actions page
