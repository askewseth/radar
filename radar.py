#!/usr/bin/env python3

import serial
import logging
import time
import os
import sys
import csv
import re
import traceback
from functools import reduce

class Radar:
    """
    This is a helper class used to interface with the Omnipresense radar devices. To date it has only been used with
    the OPS243-A model, but many of the models are similar and this likely will work fine with other variations that
    have doppler capabilities.
    """

    def __init__(self):
        self._serial_connection = None
        # Handle busy serial port
        for _retry in range(5):
            try:
                self._serial_connection = serial.Serial(
                    port="/dev/ttyACM0",
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1,
                    writeTimeout=2
                )
                break
            except Exception as e:
                print("Caught connection error: ", e)
                if _retry < 10:
                    time.sleep(3)
                    pass
                else:
                    raise
        self._configure_serial_device()

    def _configure_serial_device(self):
        """
        This private method sends all of the device setup parameters required to properly record. Each configuration
        parameter is a two character string. Details of the parameters can be found in document AN-010 from
        Omnipresense (at the time of writing the most recent location is here:
        https://omnipresense.com/wp-content/uploads/2019/10/AN-010-Q_API_Interface.pdf)
        """
        self._serial_connection.flushInput()
        self._serial_connection.flushOutput()

    def send_serial_command(self, command):
        """
        This method takes a text string and sends it over the serial connection to the radar device.

        Parameters
        ----------
        command : str
            This is command string being sent to the radar device.
        """
        self._serial_connection.flushInput()
        data_for_send_str = command
        data_for_send_bytes = str.encode(data_for_send_str)
        self._serial_connection.write(data_for_send_bytes)
        # Initialize message verify checking
        ser_message_start = '{'
        ser_write_verify = False
        # Print out module response to command string
        while not ser_write_verify:
            data_rx_bytes = self._serial_connection.readline()
            data_rx_length = len(data_rx_bytes)
            if data_rx_length != 0:
                data_rx_str = str(data_rx_bytes)
                if data_rx_str.find(ser_message_start):
                    ser_write_verify = True

    def read_serial_buffer(self):
        """
        This method reads the current serial buffer from the radar device.

        Returns
        -------
        String:
            This is the string of text on the serial buffer for the radar device
        """
        ops_rx_bytes = self._serial_connection.readline()
        ops_rx_string = ops_rx_bytes.decode()
        return str(ops_rx_string)

    def write_to_file(self, data):
        """
        Data is all written to ./data
        
        Eventual Format is ./data/<year>/<month>/<day>.csv

        Current Format is ./data/data.csv
        """


        if not os.path.isdir("./data"):
            print("Making directory")
            os.mkdir("./data")

        print("Raw Data: ", data)
        data = data.replace("-", "")
        split_data = data.split()
        regex = r'^[-]?([0-9]+\.?[0-9]*|\.[0-9]+)$'
        split_data = list(filter(lambda x: re.match(regex, x), split_data))
        floats = list(map(lambda x: float(x), split_data))
        if len(floats) > 0:
            max_float = reduce(max, floats)
            current_time = time.strftime("%m/%d/%Y-%H:%M:%S")
            print("Using processed data: ", max_float) 
            with open("./data/data.csv", "a") as f:
                f.write("{},{}\n".format(str(max_float),current_time))
        else:
            print("No data found")


    
    def run(self):
        while True:
            self.write_to_file(self.read_serial_buffer())


if __name__ == "__main__":
    while True:
        try: 
            print("Starting up...")
            radar = Radar()
            print("Made Radar")
            radar.run()
        except Exception as e:
            print("------------------------------------")
            print("Caught Exception: ", e)
            print(traceback.format_exc())
            print("------------------------------------")
    
