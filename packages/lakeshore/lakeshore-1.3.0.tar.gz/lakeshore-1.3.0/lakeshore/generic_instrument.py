"""This module implements a parent class that contains basic functionality for communicating with Lake Shore instruments."""
import logging
import select
import socket
from threading import Lock
from time import sleep

import serial
from serial.tools.list_ports import comports


class InstrumentException(Exception):
    """Names a new type of exception specific to general instrument connectivity."""


class GenericInstrument:
    """Parent class that implements functionality to connect to generic instruments"""

    vid_pid = []
    logger = logging.getLogger(__name__)

    def __init__(self, serial_number, com_port, baud_rate, data_bits, stop_bits, parity, flow_control,
                 handshaking, timeout, ip_address, tcp_port, connection=None):
        # Initialize values common to all instruments
        self.device_serial = None
        self.device_tcp = None
        self.dut_lock = Lock()
        self.serial_number = None

        # Raise an error if serial and TCP parameters are passed. Otherwise connect to the instrument using one of them.
        if ip_address is not None:
            if com_port is not None:
                raise ValueError("Two different connection methods provided.")
            else:
                self.connect_tcp(ip_address, tcp_port, timeout)
        else:
            if connection is None:
                self.connect_usb(serial_number, com_port, baud_rate, data_bits, stop_bits, parity,
                                 timeout, handshaking, flow_control)
            else:
                self.device_serial = connection

        # Query the instrument identification information and store it in variables
        try:
            idn_response = self._get_identity()
            self.firmware_version = idn_response[3]
            self.serial_number = idn_response[2]
            self.model_number = idn_response[1]
        except InstrumentException:
            print('Instrument found but unable to communicate. Please check interface settings on the instrument.')
            raise

        # Check to make sure the serial number matches what was provided if connecting over TCP
        if ip_address is not None and serial_number is not None and serial_number != self.serial_number:
            raise InstrumentException("Instrument found but the serial number does not match. " +
                                      "serial number provided is " + serial_number +
                                      ", serial number found is " + self.serial_number)

    def __del__(self):
        if self.device_serial is not None:
            self.device_serial.close()
        if self.device_tcp is not None:
            self.device_tcp.close()

    def command(self, command_string):
        """Send a command to the instrument

            Args:
                command_string (str):
                    A serial command
        """

        # Query the instrument over serial. If serial is not configured, use TCP.
        with self.dut_lock:
            # Send command to the instrument over serial. If serial is not configured, send it over TCP.
            if self.device_serial is not None:
                self._usb_command(command_string)
            elif self.device_tcp is not None:
                self._tcp_command(command_string)
            else:
                raise Exception("No connections configured")

            self.logger.info('Sent command to %s: %s', self.serial_number, command_string)

    def query(self, query_string):
        """Send a query to the instrument and return the response

            Args:
                query_string (str):
                    A serial query ending in a question mark

            Returns:
               The instrument query response as a string.

        """

        # Query the instrument over serial. If serial is not configured, use TCP.
        with self.dut_lock:
            if self.device_serial is not None:
                response = self._usb_query(query_string)
            elif self.device_tcp is not None:
                response = self._tcp_query(query_string)
            else:
                raise InstrumentException("No connections configured")

            self.logger.info('Sent query to %s: %s', self.serial_number, query_string)
            self.logger.info('Received response from %s: %s', self.serial_number, response)

        return response

    def connect_tcp(self, ip_address, tcp_port, timeout):
        """Establishes a TCP connection with the instrument on the specified IP address"""

        self.device_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device_tcp.settimeout(timeout)
        self.device_tcp.connect((ip_address, tcp_port))

        # Send the instrument a line break, wait 100ms, and clear the input buffer so that
        # any leftover communications from a prior session don't gum up the works.
        self.device_tcp.send(b'\n')
        sleep(0.1)
        while True:
            read_objects, _, _ = select.select([self.device_tcp], [], [], 0.0)
            if not read_objects:
                break
            for read_object in read_objects:
                read_object.recv(1)

    def disconnect_tcp(self):
        """Disconnect the TCP connection"""

        self.device_tcp.close()
        self.device_tcp = None

    def connect_usb(self, serial_number=None, com_port=None, baud_rate=None, data_bits=None,
                    stop_bits=None, parity=None, timeout=None, handshaking=None, flow_control=None):
        """Establish a serial USB connection"""

        # Scan the ports for devices matching the VID and PID combos of the instrument
        for port in comports():
            if (port.vid, port.pid) in self.vid_pid:
                # If the com port argument is passed, check for a match
                if port.device == com_port or com_port is None:
                    # If the serial number argument is passed, check for a match
                    if port.serial_number == serial_number or serial_number is None:
                        # Establish a connection with device using the instrument's serial communications parameters
                        self.device_serial = serial.Serial(port.device,
                                                           baudrate=baud_rate,
                                                           bytesize=data_bits,
                                                           stopbits=stop_bits,
                                                           xonxoff=handshaking,
                                                           timeout=timeout,
                                                           parity=parity,
                                                           rtscts=flow_control)

                        # Send the instrument a line break, wait 100ms, and clear the input buffer so that
                        # any leftover communications from a prior session don't gum up the works
                        self.device_serial.write(b'\n')
                        sleep(0.1)
                        self.device_serial.reset_input_buffer()

                        break
        else:
            if com_port is None and serial_number is None:
                raise InstrumentException("No serial connections found")
            else:
                raise InstrumentException(
                    "No serial connections found with a matching COM port and/or matching serial number")

    def disconnect_usb(self):
        """Disconnect the USB connection"""

        self.device_serial.close()
        self.device_serial = None

    def _tcp_command(self, command):
        """Send a command over the TCP connection"""

        self.device_tcp.send(command.encode('utf-8') + b'\n')

    def _tcp_query(self, query):
        """Query over the TCP connection"""

        self._tcp_command(query)

        total_response = ""

        # Continuously receive data from the buffer until a line break
        while True:

            # Receive the data and raise an error on timeout
            try:
                response = self.device_tcp.recv(4096).decode('utf-8')
            except socket.timeout:
                raise InstrumentException("Connection timed out")

            # Add received information to the response
            total_response += response

            # Return the response once it ends with a line break
            if total_response.endswith("\r\n"):
                return total_response.rstrip()

    def _usb_command(self, command):
        """Send a command over the serial USB connection"""

        self.device_serial.write(command.encode('ascii') + b'\n')

    def _usb_query(self, query):
        """Query over the serial USB connection"""

        self._usb_command(query)
        response = self.device_serial.readline().decode('ascii')

        # If nothing is returned, raise a timeout error.
        if not response:
            raise InstrumentException("Communication timed out")

        return response.rstrip()

    def _get_identity(self):
        return self.query('*IDN?').split(',')
