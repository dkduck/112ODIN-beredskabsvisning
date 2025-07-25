from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "beredskabsvisning"

BEREDSKABS_IDS = {
    "1212": "Aarhus Brandvæsen",
    "1313": "København Brandvæsen",
    "1414": "Odense Brandvæsen"
}

STATIONER = {
    "aarhus": "Station Aarhus",
    "skejby": "Station Skejby",
    "trige": "Station Trige"
}

class BeredskabsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="112ODIN Beredskabsvisning", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beredskabs_id", default="1212"): vol.In(BEREDSKABS_IDS),
                vol.Optional("station", default="aarhus"): vol.In(STATIONER),
                vol.Optional("dage_tilbage", default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=10))
            })
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return BeredskabsOptionsFlow(config_entry)

class BeredskabsOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("beredskabs_id", default=self.config_entry.data.get("beredskabs_id", "1212")): vol.In(BEREDSKABS_IDS),
                vol.Optional("station", default=self.config_entry.data.get("station", "aarhus")): vol.In(STATIONER),
                vol.Optional("dage_tilbage", default=self.config_entry.data.get("dage_tilbage", 1)): vol.All(vol.Coerce(int), vol.Range(min=1, max=10))
            })
        )
