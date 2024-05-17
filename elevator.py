from statemachine import StateMachine, State

# Create elevator class to set key parameters and define methods to operate elevator. Utilized python state machine
# framework to help with maintaining state here. Please see these docs for official documentation:
# https://python-statemachine.readthedocs.io/en/latest/readme.html#a-more-useful-example
# https://pypi.org/project/python-statemachine/

class Elevator:
    def __init__(self, transport_active=False):
        self.door_open = False
        self.door_closed = True
        self.transport_active = transport_active
        super(Elevator, self).__init__()

    def on_start_elevator(self):
        self.door_open = True
        self.door_closed = False
        print("Elevator started, Door opened")

    def on_close_door(self):
        self.door_open = False
        self.door_closed = True
        print("Door closed")

    def on_transporting_persons(self):
        self.transport_active = True
        print("Elevator moving")

    def on_finishing_transport(self):
        self.transport_active = False
        self.door_open = True
        self.door_closed = False
        print("Elevator arrived and stopped, Door opened")

    def on_completed_transport(self):
        self.door_open = False
        self.door_closed = True
        print("Completed Transport, Door closed")


class ElevatorControl(StateMachine):

    # set states of the elevator
    idle = State(initial=True)
    button_pushed = State()
    opening_gates = State()
    transporting = State()
    closing_gates = State()
    finished_trip = State(final=True)

    elevator_requested = idle.to(button_pushed)

    start_elevator = (
            button_pushed.to(opening_gates, cond="door_closed")
            | opening_gates.to(opening_gates)
    )
    close_door = (
            opening_gates.to(closing_gates, cond="door_open")
            | closing_gates.to(closing_gates)
    )
    transporting_persons = closing_gates.to(transporting)
    finishing_transport = transporting.to(opening_gates, cond="door_closed")
    completed_transport = opening_gates.to(closing_gates)
    final = closing_gates.to(finished_trip)


# instantiate elevator classes
new_elevator = Elevator()
new_elevator_control = ElevatorControl(new_elevator)

# run elevator
new_elevator_control.elevator_requested()
new_elevator_control.start_elevator()
new_elevator_control.close_door()
new_elevator_control.transporting_persons()
new_elevator_control.finishing_transport()
new_elevator_control.completed_transport()
new_elevator_control.final()

# %%

#%%
