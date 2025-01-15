import LineProcessor

# Initialize LineProcessor
processor = LineProcessor.LineProcessor(tx_pin=19, rx_pin=18)
print("LineProcessor Initialized")

while True:
    processor.read_and_parse()
    smoothed_deltaX = processor.get_deltaX()
    if smoothed_deltaX is not None:
        print(f"Smoothed deltaX: {smoothed_deltaX}")
