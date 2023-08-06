"""This component provides HA sensor support for Ring Door Bell/Chimes."""
from datetime import timedelta
import logging

from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ATTRIBUTION, DOMAIN, SIGNAL_UPDATE_RING

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)

# Sensor types: Name, category, device_class
SENSOR_TYPES = {
    "ding": ["Ding", ["doorbots", "authorized_doorbots"], "occupancy"],
    "motion": ["Motion", ["doorbots", "authorized_doorbots", "stickup_cams"], "motion"],
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Ring binary sensors from a config entry."""
    ring = hass.data[DOMAIN][config_entry.entry_id]
    devices = ring.devices()

    sensors = []

    for device_type in ("doorbots", "authorized_doorbots", "stickup_cams"):
        for sensor_type in SENSOR_TYPES:
            if device_type not in SENSOR_TYPES[sensor_type][1]:
                continue

            for device in devices[device_type]:
                sensors.append(RingBinarySensor(ring, device, sensor_type))

    async_add_entities(sensors, True)


class RingBinarySensor(BinarySensorDevice):
    """A binary sensor implementation for Ring device."""

    def __init__(self, ring, device, sensor_type):
        """Initialize a sensor for Ring device."""
        self._sensor_type = sensor_type
        self._ring = ring
        self._device = device
        self._name = "{0} {1}".format(
            self._device.name, SENSOR_TYPES.get(self._sensor_type)[0]
        )
        self._device_class = SENSOR_TYPES.get(self._sensor_type)[2]
        self._state = None
        self._unique_id = f"{self._device.id}-{self._sensor_type}"
        self._disp_disconnect = None

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._disp_disconnect = async_dispatcher_connect(
            self.hass, SIGNAL_UPDATE_RING, self._update_callback
        )

    async def async_will_remove_from_hass(self):
        """Disconnect callbacks."""
        if self._disp_disconnect:
            self._disp_disconnect()
            self._disp_disconnect = None

    @callback
    def _update_callback(self):
        """Call update method."""
        self.async_schedule_update_ha_state(True)
        _LOGGER.debug("Updating Ring binary sensor %s (callback)", self.name)

    @property
    def should_poll(self):
        """Return False, updates are controlled via the hub."""
        return False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return True if the binary sensor is on."""
        return self._state

    @property
    def device_class(self):
        """Return the class of the binary sensor."""
        return self._device_class

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._unique_id

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name,
            "model": self._device.model,
            "manufacturer": "Ring",
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION

        if self._device.alert and self._device.alert_expires_at:
            attrs["expires_at"] = self._device.alert_expires_at
            attrs["state"] = self._device.alert.get("state")

        return attrs

    async def async_update(self):
        """Get the latest data and updates the state."""
        self._state = any(
            alert["kind"] == self._sensor_type
            and alert["doorbot_id"] == self._device.id
            for alert in self._ring.active_alerts()
        )
