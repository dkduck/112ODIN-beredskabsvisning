from homeassistant.components.sensor import SensorEntity
import feedparser

DOMAIN = "beredskabsvisning"

async def async_setup_entry(hass, entry, async_add_entities):
    beredskabs_id = entry.options.get("beredskabs_id", "1212")
    station = entry.options.get("station", "aarhus")
    dage_tilbage = entry.options.get("dage_tilbage", 1)

    feed_url = f"http://www.odin.dk/RSS/RSS.aspx?beredskabsID={beredskabs_id}"
    async_add_entities([OdinSensor(feed_url, station, dage_tilbage)], True)

class OdinSensor(SensorEntity):
    def __init__(self, feed_url, station, dage_tilbage):
        self._attr_name = f"112 ODIN - {station}"
        self._feed_url = feed_url
        self._station = station
        self._dage_tilbage = dage_tilbage
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    def update(self):
        feed = feedparser.parse(self._feed_url)
        for entry in feed.entries:
            if self._station.lower() in entry.summary.lower():
                self._attr_native_value = entry.title
                self._attr_extra_state_attributes = {
                    "published": entry.published,
                    "summary": entry.summary,
                    "link": entry.link
                }
                break
