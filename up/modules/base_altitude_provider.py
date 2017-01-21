from up.commands.altitude_command import AltitudeCommand, AltitudeCommandHandler
from up.base_started_module import BaseStartedModule


class BaseAltitudeProvider(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__altitude = 0
        self.__arduino_provider = None
        self.__altitude_change_handle = None
        self.__altitude_change_handle = None

    def _execute_start(self):
        super()._execute_start()
        self.__altitude_change_handle = self.up.command_executor.register_command(AltitudeCommand.NAME, AltitudeCommandHandler(self))
        return True

    def _execute_stop(self):
        super()._execute_stop()
        self.up.command_executor.unregister_command(AltitudeCommand.NAME, self.__altitude_change_handle)

    def _on_altitude_changed(self, new_alt):
        cmd = AltitudeCommand()
        cmd.data = {'altitude': new_alt}
        self.up.command_executor.execute_command(cmd)

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self, value):
        self.__altitude = value
        self._on_altitude_changed(value)
