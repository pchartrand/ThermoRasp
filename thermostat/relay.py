from gpiozero import LED

class Relay(object):
    def __init__(self, pin):
        self.relay = LED(pin)

    def on(self):
        self.relay.on()

    def off(self):
        self.relay.off()