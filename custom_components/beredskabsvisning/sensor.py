import feedparser
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, DEFAULT_NAME, FEED_URL

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([OdinSensor()], True)

class OdinSensor(Entity):
    def __init__(self):
        self._state = None
        self._attr_name = DEFAULT_NAME
        self._attr_unique_id = "sensor.112_odin"
        self._latest_title = None

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {"latest_title": self._latest_title}

    async def async_update(self):
        feed = feedparser.parse(FEED_URL)
        if feed.entries:
            self._latest_title = feed.entries[0].title
            self._state = "🆕 Beredskabsopslag modtaget"
        else:
            self._state = "Ingen nye opslag"
