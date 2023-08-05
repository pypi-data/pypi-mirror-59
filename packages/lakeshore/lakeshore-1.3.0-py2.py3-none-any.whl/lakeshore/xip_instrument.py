"""This module implements a parent class that contains all functionality shared by Lake Shore XIP instruments."""

import re

import serial

from .generic_instrument import GenericInstrument, InstrumentException


class RegisterBase:
    """Base class of the status register classes"""

    bit_names = []

    def __str__(self):
        return str(vars(self))


class StatusByteRegister(RegisterBase):
    """Class object representing the status byte register"""

    bit_names = [
        "",
        "",
        "error_available",
        "questionable_summary",
        "message_available_summary",
        "event_status_summary",
        "master_summary",
        "operation_summary"
    ]

    def __init__(self,
                 error_available,
                 questionable_summary,
                 message_available_summary,
                 event_status_summary,
                 master_summary,
                 operation_summary):
        self.error_available = error_available
        self.questionable_summary = questionable_summary
        self.message_available_summary = message_available_summary
        self.event_status_summary = event_status_summary
        self.master_summary = master_summary
        self.operation_summary = operation_summary


class StandardEventRegister(RegisterBase):
    """Class object representing the standard event register"""

    bit_names = [
        "operation_complete",
        "query_error",
        "device_specific_error",
        "execution_error",
        "command_error",
        "",
        "power_on"
    ]

    def __init__(self,
                 operation_complete,
                 query_error,
                 device_specific_error,
                 execution_error,
                 command_error,
                 power_on):
        self.operation_complete = operation_complete
        self.query_error = query_error
        self.device_specific_error = device_specific_error
        self.execution_error = execution_error
        self.command_error = command_error
        self.power_on = power_on


class XIPInstrumentException(Exception):
    """Names a new type of exception specific to XIP instrument connectivity."""


class XIPInstrument(GenericInstrument):
    """Parent class that implements functionality shared by all XIP instruments"""

    def __init__(self, serial_number, com_port, baud_rate, flow_control, timeout, ip_address, tcp_port, **kwargs):
        # Initialize values common to all XIP instruments
        GenericInstrument.__init__(self, serial_number, com_port, baud_rate, 8, 1, serial.PARITY_NONE, flow_control,
                                   False, timeout, ip_address, tcp_port, **kwargs)
        self.status_byte_register = StatusByteRegister
        self.standard_event_register = StandardEventRegister
        self.operation_register = None
        self.questionable_register = None

    def command(self, *commands, **kwargs):
        """Send a SCPI command or multiple commands to the instrument

            Args:
                commands (str):
                    Any number of SCPI commands.

            Kwargs:
                check_errors (bool):
                    Chooses whether to query the SCPI error queue and raise errors as exceptions. True by default.

        """

        check_errors = kwargs.get("check_errors", True)

        # Group all commands into a single string with SCPI delimiters.
        command_string = ";:".join(commands)

        # Pass the string to the query function if it contains a question mark.
        if check_errors:
            # Do a query which will automatically check the errors.
            self.query(command_string)
        else:
            with self.dut_lock:
                # Send command to the instrument over serial. If serial is not configured, send it over TCP.
                if self.device_serial is not None:
                    self._usb_command(command_string)
                elif self.device_tcp is not None:
                    self._tcp_command(command_string)
                else:
                    raise InstrumentException("No connections configured")

                self.logger.info('Sent SCPI command to %s: %s', self.serial_number, command_string)

    def query(self, *queries, **kwargs):
        """Send a SCPI query or multiple queries to the instrument and return the response(s)

            Args:
                queries (str):
                    Any number of SCPI queries or commands.

            Kwargs:
                check_errors (bool):
                    Chooses whether to query the SCPI error queue and raise errors as exceptions. True by default.

            Returns:
               The instrument query response as a string.

        """

        check_errors = kwargs.get("check_errors", True)

        # Group all commands and queries a single string with SCPI delimiters.
        query_string = ";:".join(queries)

        # Append the query with an additional error buffer query.
        if check_errors:
            query_string += ";:SYSTem:ERRor:ALL?"

        # Query the instrument over serial. If serial is not configured, use TCP.
        with self.dut_lock:
            if self.device_serial is not None:
                response = self._usb_query(query_string)
            elif self.device_tcp is not None:
                response = self._tcp_query(query_string)
            else:
                raise InstrumentException("No connections configured")

            self.logger.info('Sent SCPI query to %s: %s', self.serial_number, query_string)
            self.logger.info('Received SCPI response from %s: %s', self.serial_number, response)

        if check_errors:
            # Split the responses to each query, remove the last response which is to the error buffer query,
            # and check whether it contains an error
            response_list = re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', response)
            error_response = response_list.pop()
            self._error_check(error_response)
            response = ';'.join(response_list)

        return response

    @staticmethod
    def _error_check(error_response):
        """Evaluates the instrument response"""

        # If the error buffer returns an error, raise an exception with that includes the error.
        if "No error" not in error_response:
            raise XIPInstrumentException("SCPI command error(s): " + error_response)

    def get_status_byte(self):
        """Returns named bits of the status byte register and their values"""

        response = self.query("*STB?", check_errors=False)
        status_register = self._interpret_status_register(response, self.status_byte_register)

        return status_register

    def get_service_request_enable_mask(self):
        """Returns the named bits of the status byte service request enable register.
        This register determines which bits propagate to the master summary status bit"""

        response = self.query("*SRE?", check_errors=False)
        status_register = self._interpret_status_register(response, self.status_byte_register)

        return status_register

    def set_service_request_enable_mask(self, register_mask):
        """Configures values of the service request enable register bits.
        This register determines which bits propagate to the master summary bit

            Args:
                register_mask (StatusByteRegister):
                    A StatusByteRegister class object with all bits configured true or false.
        """

        integer_representation = self._configure_status_register(register_mask)
        self.command("*SRE " + str(integer_representation), check_errors=False)

    def get_standard_events(self):
        """Returns the names of the standard event register bits and their values"""

        response = self.query("*ESR?", check_errors=False)
        status_register = self._interpret_status_register(response, self.standard_event_register)

        return status_register

    def get_standard_event_enable_mask(self):
        """Returns the names of the standard event enable register bits and their values.
        These values determine which bits propagate to the standard event register"""

        response = self.query("*ESE?", check_errors=False)
        status_register = self._interpret_status_register(response, self.standard_event_register)

        return status_register

    def set_standard_event_enable_mask(self, register_mask):
        """Configures values of the standard event enable register bits.
        These values determine which bits propagate to the standard event register

            Args:
                register_mask (StandardEventRegister):
                    A StandardEventRegister class object with all bits configured true or false.
        """

        integer_representation = self._configure_status_register(register_mask)
        self.command("*ESE " + str(integer_representation), check_errors=False)

    def get_present_operation_status(self):
        """Returns the names of the operation status register bits and their values"""

        response = self.query("STATus:OPERation:CONDition?", check_errors=False)
        status_register = self._interpret_status_register(response, self.operation_register)

        return status_register

    def get_operation_events(self):
        """Returns the names of operation event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.query("STATus:OPERation:EVENt?", check_errors=False)
        status_register = self._interpret_status_register(response, self.operation_register)

        return status_register

    def get_operation_event_enable_mask(self):
        """Returns the names of the operation event enable register bits and their values.
        These values determine which operation bits propagate to the operation event register."""

        response = self.query("STATus:OPERation:ENABle?", check_errors=False)
        status_register = self._interpret_status_register(response, self.operation_register)

        return status_register

    def set_operation_event_enable_mask(self, register_mask):
        """Configures the values of the operation event enable register bits.
        These values determine which operation bits propagate to the operation event register.

            Args:
                register_mask ([Instrument]OperationRegister):
                    An instrument specific OperationRegister class object with all bits configured true or false.
        """

        integer_representation = self._configure_status_register(register_mask)
        self.command("STATus:OPERation:ENABle " + str(integer_representation), check_errors=False)

    def get_present_questionable_status(self):
        """Returns the names of the questionable status register bits and their values"""

        response = self.query("STATus:QUEStionable:CONDition?", check_errors=False)
        status_register = self._interpret_status_register(response, self.questionable_register)

        return status_register

    def get_questionable_events(self):
        """Returns the names of questionable event status register bits that are currently high.
        The event register is latching and values are reset when queried."""

        response = self.query("STATus:QUEStionable:EVENt?", check_errors=False)
        status_register = self._interpret_status_register(response, self.questionable_register)

        return status_register

    def get_questionable_event_enable_mask(self):
        """Returns the names of the questionable event enable register bits and their values.
        These values determine which questionable bits propagate to the questionable event register."""

        response = self.query("STATus:QUEStionable:ENABle?", check_errors=False)
        status_register = self._interpret_status_register(response, self.questionable_register)

        return status_register

    def set_questionable_event_enable_mask(self, register_mask):
        """Configures the values of the questionable event enable register bits.
        These values determine which questionable bits propagate to the questionable event register.

            Args:
                register_mask ([Instrument]QuestionableRegister):
                    An instrument specific QuestionableRegister class object with all bits configured true or false.
        """

        integer_representation = self._configure_status_register(register_mask)
        self.command("STATus:QUEStionable:ENABle " + str(integer_representation), check_errors=False)

    def reset_status_register_masks(self):
        """Resets status register masks to preset values"""
        self.command("STATus:PRESet", check_errors=False)

    @staticmethod
    def _interpret_status_register(integer_representation, register):
        """Translates the integer representation of a register state into a named array"""

        # Create a dictionary to temporarily store the bit states
        bit_states = {}

        # Assign the boolean value of each bit in the integer to the corresponding status register bit name
        for count, bit_name in enumerate(register.bit_names):
            if bit_name:
                mask = 0b1 << count
                bit_states[bit_name] = bool(int(integer_representation) & mask)

        return register(**bit_states)

    @staticmethod
    def _configure_status_register(mask_register):
        """Translates from a named array to an integer representation value"""

        # Check whether an integer was passed. If so, return it.
        if isinstance(mask_register, int):
            return mask_register

        # If a class was passed, call a function to turn it back into an integer representation
        integer_representation = 0

        # Add up the boolean values of a list of named instrument states
        # while being careful to account for unnamed entries in the register bit names list
        for count, bit_name in enumerate(mask_register.bit_names):

            if bit_name:
                integer_representation += int(getattr(mask_register, bit_name)) << count

        return integer_representation

    def modify_service_request_mask(self, bit_name, value):
        """Gets the service request enable mask, changes a bit, and sets the register.

            Args:
                bit_name (str):
                    The name of the bit to modify.

                value (bool):
                    Determines whether the bit masks (false) or passes (true) the corresponding state.

        """

        mask_register = self.get_service_request_enable_mask()

        setattr(mask_register, bit_name, value)

        self.set_service_request_enable_mask(mask_register)

    def modify_standard_event_register_mask(self, bit_name, value):
        """Gets the standard event register mask, changes a bit, and sets the register

            Args:
                bit_name (str):
                    The name of the bit to modify.

                value (bool):
                    Determines whether the bit masks (false) or passes (true) the corresponding state.

        """

        mask_register = self.get_standard_event_enable_mask()

        setattr(mask_register, bit_name, value)

        self.set_standard_event_enable_mask(mask_register)

    def modify_operation_register_mask(self, bit_name, value):
        """Gets the operation condition register mask, changes a bit, and sets the register

            Args:
                bit_name (str):
                    The name of the bit to modify.

                value (bool):
                    Determines whether the bit masks (false) or passes (true) the corresponding state.

        """

        mask_register = self.get_operation_event_enable_mask()

        setattr(mask_register, bit_name, value)

        self.set_operation_event_enable_mask(mask_register)

    def modify_questionable_register_mask(self, bit_name, value):
        """Gets the questionable condition register mask, changes a bit, and sets the register

            Args:
                bit_name (str):
                    The name of the bit to modify.

                value (bool):
                    Determines whether the bit masks (false) or passes (true) the corresponding state.

        """

        mask_register = self.get_questionable_event_enable_mask()

        setattr(mask_register, bit_name, value)

        self.set_questionable_event_enable_mask(mask_register)

    def reset_measurement_settings(self):
        """Resets measurement settings to their default values."""
        self.command("SYSTEM:PRESET")

    def factory_reset(self):
        """Resets all system information such as settings, wi-fi connections, date and time, etc."""
        self.command("SYSTEM:FACTORYRESET")

    def _get_identity(self):
        return self.query('*IDN?', check_errors=False).split(',')
