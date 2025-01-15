import sensor, image, machine, pyb



# Initialize camera
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)




# Configure UART (UART3: TX=Pin P4, RX=Pin P5)
uart = pyb.UART(1, 115200)

print("OpenMV Line Detection and UART Transmission Ready")

while True:
    img = sensor.snapshot()
    lines = img.find_lines(threshold=1000, theta_margin=25, rho_margin=25)
    
    if lines:
        for line in lines:
            # Calculate deltaX
            deltaX = line.x2() - line.x1()
        
            # Format line data as a comma-separated string
            line_data = f"{line.x1()},{line.y1()},{line.x2()},{line.y2()},{line.theta()},{deltaX}\n"
            uart.write(line_data)  # Send line data over UART
            print("Sent:", line_data.strip())
