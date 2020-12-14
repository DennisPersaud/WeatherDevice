import time
import grovepi
import json
import socket

light_sensor = 0                # Connect the Grove Light Sensor to analog port A0
threshold = 1000                # Run script once sensor exceeds threshold resistance
green = 2                       # Connect the green LED to digital port D3
blue = 3                        # Connect the blue LED to digital port D4
red = 4                         # COnnect the red LED to digital port D5
temp_sensor = 6                 # Connect the Grove DHT sensor to port D6
blue = 0                        # The Blue colored temp_sensor
data = []                       # Initialize array to store data
frequency = 30                  # Record update frequency

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(green, "OUTPUT")
grovepi.pinMode(blue, "OUTPUT")
grovepi.pinMode(red, "OUTPUT")


def server():
    try:
        # Listen for connections
        s = socket.socket()
        host = '192.168.0.23'
        port = 8080
        s.bind((host, port))
        s.listen(1)
        # print(host)
        print("waiting for any incoming connections...")
        conn, addr = s.accept()
        print(addr, "has connected to the server.")
        return conn
    except Exception as e:
        print(e)
        pass


def sensor(connection):
    while True:

        # Get light data from light_sensor
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value

        if resistance <= threshold:
            # Create or overwrite json file to save incoming data
            try:
                file = open('./data.json', 'w')
            except Exception:
                pass

            # Get humidity and temperature data from temp_sensor
            humidity, temperature = grovepi.dht(temp_sensor, blue)

            # Low temperature condition
            if 60 < temperature < 85:
                if humidity < 80:
                    grovepi.digitalWrite(green, 1)
                else:
                    grovepi.digitalWrite(green, 0)
            # Mid temperature condition
            elif 85 < temperature < 95:
                if humidity < 80:
                    grovepi.digitalWrite(blue, 1)
                else:
                    grovepi.digitalWrite(blue, 0)
            # High temperature condition
            elif temperature > 95:
                grovepi.digitalWrite(red, 1)
            # High humidity condition
            elif humidity > 80:
                grovepi.digitalWrite(green, 1)
                grovepi.digitalWrite(blue, 1)
            # Turn off LEDs
            else:
                grovepi.digitalWrite(green, 0)
                grovepi.digitalWrite(red, 0)
                grovepi.digitalWrite(blue, 0)

            # Append data to array
            if humidity is not None and temperature is not None:
                temp = int(temperature)
                hum = int(humidity)
                data.append([temp, hum])
            else:
                pass

            # Display & save data
            print(data)
            json.dump(data, file)
            time.sleep(frequency)

            # Send data
            try:
                filename = 'data.json'
                file = open(filename, 'rb')
                file_data = file.read(1024)
                connection.send(file_data)
                print('Data sent.')
                time.sleep(4)
            except Exception:
                pass
        elif resistance > threshold:
            pass


if __name__ == '__main__':
    connection = server()
    sensor(connection)
