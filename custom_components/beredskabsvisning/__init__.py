"""112ODIN Beredskabsvisning integration."""
DOMAIN = "beredskabsvisning"

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry
    return True
