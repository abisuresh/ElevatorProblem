from statemachine import StateMachine, State


# Create elevator class to set key parameters and define methods to operate elevator. Utilized python state machine
# framework to help with maintaining state here. Please see these docs for official documentation:
# https://python-statemachine.readthedocs.io/en/latest/readme.html#a-more-useful-example
# https://pypi.org/project/python-statemachine/

class Elevator(StateMachine):
    # set states of the elevator
    idle_state = State(initial=True)
    button_pushed = State()
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
            opening_gates.to(transporting, cond="transport_active")
            | opening_gates.to(opening_gates, unless="transport_active")
    )
    finishing_transport = transporting.to(closing_gates, cond="door_closed")
    completed_transport = closing_gates.to(finished_trip)

    def __init__(self, num_floors, door_open=False, door_closed = False, transport_active = False, elevator_available=False, max_occupancy=10):
        self.door_open = door_open
        self.door_closed = door_closed
        self.transport_active = transport_active
        self.elevator_available = elevator_available
        self.num_floors = num_floors
        self.max_occupancy = max_occupancy
        self.current_floor = 1
        super(Elevator, self).__init__()

    def pushButton(self):
        if self.elevator_available:
            self.openDoors()
        return

    def openDoors(self):
        self.door_open = True
        self.door_closed = False
        return

    def closeDoors(self):
        self.door_open = False
        self.door_closed = True
        return

    def transport(self, end_floor):
        self.transport_active = True
        self.elevator_available = False
        self.current_floor = end_floor
        return


# instantiate elevator class
new_elevator = Elevator(num_floors=2, elevator_available=False, max_occupancy=10)

# run elevator
new_elevator.elevator_available = False
new_elevator.pushButton()
new_elevator.finishing_transport


#%%
