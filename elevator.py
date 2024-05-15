from statemachine import StateMachine, State


# Create elevator class to set key parameters and define methods to operate elevator. Utilized python state machine
# framework to help with maintaining state here. Please see these docs for official documentation:
# https://python-statemachine.readthedocs.io/en/latest/readme.html#a-more-useful-example
# https://pypi.org/project/python-statemachine/

class Elevator(StateMachine):
    # set states of the elevator
    idle_state = State(initial=True)
    button_pushed = State()
    transporting = State()
    opening_gates = State()
    closing_gates = State()
    finished_trip = State(final=True)

    elevator_requested = idle_state.to(button_pushed)
    opened_gates = (
        button_pushed.to(opening_gates, cond="opened gates")
        | button_pushed.to(button_pushed, unless="opened gates")
    )
    transport = transporting.to(closing_gates, cond="gates closed")
    finished_transport = transporting.to(finished_trip)

    def __init__(self, num_floors, elevator_available=False, max_occupancy=10, door_open=False):
        self.elevator_available = elevator_available
        self.num_floors = num_floors
        self.max_occupancy = max_occupancy
        self.door_open = door_open
        super(Elevator, self).__init__()


    def openDoors(self):
        if not self.door_open:
            self.door_open = True
        return

    def closeDoors(self):
        if self.door_open:
            self.door_open = False
        return

    def pushButton(self):
        if self.elevator_available:
            self.openDoors()
        return

    def transport(self, start_floor, end_floor):

        return

    def operateElevator(self):
        while self.elevator_available:
            self.openDoors()


# instantiate elevator class
new_elevator = Elevator(num_floors=2, elevator_available=False, max_occupancy=10)

# run elevator

new_elevator.pushButton()
