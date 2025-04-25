"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations
from .inverter.inverterclient import InverterClient

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This hub always returns 3 inverters.
import asyncio
import random

from homeassistant.core import HomeAssistant
import time
import logging
_LOGGER = logging.getLogger(__name__)

class Hub:
    manufacturer = "Inverter"

    def __init__(self, hass: HomeAssistant, device: str) -> None:
        """Init hub."""
        self._id = "0"
        self._device = device
        self._hass = hass
        #self.init_inverter()

    async def init_inverter(self):
        self.inverter_client=InverterClient(self._device)
        self.inverter_client.connect()
        self.inverter_client.get_basic_info()

        self._name = f"Inverter {self._id}: {self._device}"
        self.manufacturer=self.inverter_client.manufacturer
        self.inverter = Inverter(self._id, self._name, self)
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity with inverter"""
        #await asyncio.sleep(1)
        return self.inverter_client.get_mode()


class Inverter:
    """inverter (device for HA)."""

    def __init__(self, inverterid: str, name: str, hub: Hub) -> None:
        """Init inverter."""
        self._id = inverterid
        self.hub = hub
        self.name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()

        self.model=self.hub.inverter_client.model
        self.firmware_version=self.hub.inverter_client.firmware_version

    @property
    def inverter_id(self) -> str:
        """Return ID for inverter."""
        return self._id

    @property
    def position(self):
        """Return position for inverter."""
        return self._current_position

    async def set_position(self, position: int) -> None:
        """
        Set cover to the given position.

        State is announced a random number of seconds later.
        """
        self._target_position = position

        # Update the moving status, and broadcast the update
        self.moving = position - 50
        await self.publish_updates()

        self._loop.create_task(self.delayed_update())

    async def delayed_update(self) -> None:
        """Publish updates, with a random delay to emulate interaction with device."""
        await asyncio.sleep(20)
        self.moving = 0
        await self.publish_updates()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Inverter changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""
        self._current_position = self._target_position
        for callback in self._callbacks:
            callback()

    def get_available_params(self, data_type):
        return self.hub.inverter_client.GetInverterDataByCommandSync(data_type)

    @property
    def online(self) -> float:
        """Inverter is online."""
        #  Returns True if online,
        # False if offline.
        #self.update_data()
        return self.hub.inverter_client.connected

    def reconnect(self):
        return self.hub.inverter_client.reconnect()
