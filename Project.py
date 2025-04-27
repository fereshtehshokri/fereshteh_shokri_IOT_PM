

'''

APM:

Salam daryaft shod

'''




#=============================== IMPORT NECESSARY LIBRARIES ===============================
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

#=============================== CLASS Device ===============================
class Device:
    def __init__(self, topic, mqtt_broker='localhost', port=1883, pin=None):
        """
        Initialize a device with its MQTT and GPIO settings.
        """
        self.topic = topic
        self.topic_list = self.topic.split('/')
        self.location = self.topic_list[0]
        self.group = self.topic_list[1]
        self.device_type = self.topic_list[2]
        self.device_name = self.topic_list[3]
        self.status = 'off'
        self.mqtt_broker = mqtt_broker
        self.port = port
        self.pin = pin
        
        try:
            # Initialize MQTT and GPIO
            self.connect_mqtt()
            self.setup_gpio()
        except Exception as e:
            print(f"Error during initialization: {e}")

    def connect_mqtt(self):
        """
        Connect to the MQTT broker.
        """
        try:
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.connect(self.mqtt_broker, self.port)
            print(f"Connected to MQTT broker at {self.mqtt_broker}:{self.port}")
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")

    def setup_gpio(self):
        """
        Setup GPIO pin based on device type.
        """
        GPIO.setmode(GPIO.BCM)
        if self.device_type == 'lamps':
            self.pin = 17
        elif self.device_type == 'doors':
            self.pin = 27
        elif self.device_type == 'fans':
            self.pin = 22
        else:
            raise ValueError("Unsupported device type!")
        GPIO.setup(self.pin, GPIO.OUT)
        print(f"GPIO setup done for device type: {self.device_type} on pin {self.pin}")

    def turn_on(self):
        """
        Turn on the device.
        """
        try:
            GPIO.output(self.pin, GPIO.HIGH)
            self.status = 'on'
            self.send_command('TURN_ON')
            print(f"{self.device_name} turned ON!")
        except Exception as e:
            print(f"Error turning on device '{self.device_name}': {e}")

    def turn_off(self):
        """
        Turn off the device.
        """
        try:
            GPIO.output(self.pin, GPIO.LOW)
            self.status = 'off'
            self.send_command('TURN_OFF')
            print(f"{self.device_name} turned OFF!")
        except Exception as e:
            print(f"Error turning off device '{self.device_name}': {e}")

    def send_command(self, command):
        """
        Send MQTT command to the device.
        """
        try:
            self.mqtt_client.publish(self.topic, command)
            print(f"Command '{command}' sent to topic '{self.topic}'")
        except Exception as e:
            print(f"Error sending command '{command}' to topic '{self.topic}': {e}")

    def get_status(self):
        """
        Get the current status of the device.
        """
        print(f"Device '{self.device_name}' is currently {self.status}")

#=============================== CLASS Sensor ===============================
class Sensor:
    def __init__(self, topic, pin=None):
        """
        Initialize a sensor with its topic and pin settings.
        """
        self.topic = topic
        self.topic_list = self.topic.split('/')
        self.location = self.topic_list[0]
        self.group = self.topic_list[1]
        self.sensor_type = self.topic_list[2]
        self.sensor_name = self.topic_list[3]
        self.pin = pin

    def read_sensor(self):
        """
        Simulate reading sensor data. Replace this with real sensor reading logic.
        """
        try:
            if self.sensor_type == 'temperature':
                return 25.0  # Simulated temperature value
            elif self.sensor_type == 'humidity':
                return 60.0  # Simulated humidity value
            else:
                raise ValueError("Unsupported sensor type!")
        except Exception as e:
            print(f"Error reading sensor '{self.sensor_name}': {e}")
            return None

    def get_status(self):
        """
        Get the current value of the sensor.
        """
        sensor_value = self.read_sensor()
        print(f"Sensor '{self.sensor_name}' value: {sensor_value}")

#=========================== CLASS Admin Panel ==============================
class AdminPanel:
    def __init__(self):
        """
        Initialize the admin panel to manage groups and devices.
        """
        self.groups = {}

    def create_group(self, group_name):
        """
        Create a new group for devices.
        """
        if group_name not in self.groups:
            self.groups[group_name] = []
            print(f"Group '{group_name}' created.")
        else:
            print(f"Group '{group_name}' already exists.")

    def add_device_to_group(self, group_name, device):
        """
        Add a device to a specific group.
        """
        if group_name in self.groups:
            self.groups[group_name].append(device)
            print(f"Device '{device.device_name}' added to group '{group_name}'.")
        else:
            print(f"Group '{group_name}' does not exist.")

    def create_device(self, group_name, device_type, name):
        """
        Create a new device and add it to a group.
        """
        if group_name in self.groups:
            topic = f"home/{group_name}/{device_type}/{name}"
            new_device = Device(topic)
            self.add_device_to_group(group_name, new_device)
        else:
            print(f"Group '{group_name}' does not exist.")

    def create_multiple_devices(self, group_name, device_type, number_of_devices):
        """
        Create multiple devices in a group.
        """
        if group_name in self.groups:
            for i in range(1, number_of_devices + 1):
                device_name = f"{device_type}{i}"
                self.create_device(group_name, device_type, device_name)
        else:
            print(f"Group '{group_name}' does not exist.")

    def turn_on_all_in_group(self, group_name):
        """
        Turn on all devices in a specific group.
        """
        if group_name in self.groups:
            all_devices = self.groups[group_name]
            for device in all_devices:
                device.turn_on()
        else:
            print(f"Group '{group_name}' does not exist.")

    def turn_off_all_in_group(self, group_name):
        """
        Turn off all devices in a specific group.
        """
        if group_name in self.groups:
            all_devices = self.groups[group_name]
            for device in all_devices:
                device.turn_off()
        else:
            print(f"Group '{group_name}' does not exist.")

    def get_status_in_group(self, group_name):
        """
        Get the status of all devices in a specific group.
        """
        if group_name in self.groups:
            all_devices = self.groups[group_name]
            for device in all_devices:
                device.get_status()
        else:
            print(f"Group '{group_name}' does not exist.")

#=============================== MAIN LOGIC =================================
if __name__ == "__main__":
    try:
        admin_panel = AdminPanel()

        # Create groups and devices
        admin_panel.create_group("kitchen")
        admin_panel.create_group("parking")
        admin_panel.create_multiple_devices("kitchen", "lamps", 5)
        admin_panel.create_multiple_devices("parking", "fans", 3)

        # Turn on/off devices in groups
        admin_panel.turn_on_all_in_group("kitchen")
        admin_panel.turn_off_all_in_group("parking")

        # Get status of devices
        admin_panel.get_status_in_group("kitchen")
        admin_panel.get_status_in_group("parking")
    except Exception as e:
        print(f"Error in main logic: {e}")
