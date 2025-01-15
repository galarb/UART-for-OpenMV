from machine import UART, Pin

class LineProcessor:
    def __init__(self, tx_pin, rx_pin, baudrate=115200):
        """Initialize UART and buffer."""
        self.uart = UART(2, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.buffer = ""  # Buffer to store incoming data
        self.deltaX = None  # Most recent deltaX value
        self.prev_deltaX = None  # Previous deltaX for smoothing

    def read_and_parse(self):
        """Read from UART, parse data, and calculate deltaX."""
        if self.uart.any():  # Check if data is available
            self.buffer += self.uart.read().decode('utf-8')  # Append received data to the buffer

            # Process complete data (delimited by \n)
            if "\n" in self.buffer:
                lines = self.buffer.split("\n")  # Split buffer into lines
                for line in lines[:-1]:  # Process all complete lines
                    try:
                        x1, y1, x2, y2, theta, deltaX = map(int, line.split(','))
                        # Apply smoothing
                        if self.prev_deltaX == deltaX:
                            self.deltaX = deltaX  # Accept value only if it matches previous value
                        else:
                            self.deltaX = None  # Reject as noise
                        self.prev_deltaX = deltaX  # Update the previous value
                    except ValueError as e:
                        print("Error parsing data:", e)

                # Retain any incomplete line in the buffer
                self.buffer = lines[-1]

    def get_deltaX(self):
        """Return the most recent deltaX value (after smoothing)."""
        return self.deltaX

