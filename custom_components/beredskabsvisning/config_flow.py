from homeassistant import config_entries
import voluptuous as vol

class BeredskabsConfigFlow(config_entries.ConfigFlow, domain="beredskabsvisning"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(
                title=user_input["overskrift"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("beredskabs_id"): str,
                vol.Required("stationer"): str,
                vol.Required("dage", default=7): int,
                vol.Required("overskrift"): str,
            })
        )
