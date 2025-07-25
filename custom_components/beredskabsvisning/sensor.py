import logging
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([BeredskabsSensor(entry)])

class BeredskabsSensor(SensorEntity):
    def __init__(self, entry):
        self._name = entry.title
        self._id = entry.data.get("beredskabs_id")
        self._stationer = entry.data.get("stationer")
        self._dage = int(entry.data.get("dage"))
        self._overskrift = entry.data.get("overskrift")
        self._state = None
        self._entries = []

    @property
    def name(self):
        return f"{self._overskrift}"

    @property
    def state(self):
        return f"{len(self._entries)} hændelser"

    @property
    def extra_state_attributes(self):
        return {
            "entries": self._entries,
            "stationer": self._stationer,
            "periode": f"{self._dage} dage"
        }

    def update(self):
        # Erstat dette med rigtig datakilde!
        raw_data = [
            {"summary": "Station A slukker brand", "published": "23-07-2025"},
            {"summary": "Station B assisterer ved uheld", "published": "24-07-2025"}
        ]

        cutoff = datetime.now() - timedelta(days=self._dage)
        filtreret = []

        for e in raw_data:
            dato = datetime.strptime(e["published"], "%d-%m-%Y")
            if dato >= cutoff and any(s.strip() in e["summary"] for s in self._stationer.split(",")):
                filtreret.append(e)

        self._entries = filtreret
