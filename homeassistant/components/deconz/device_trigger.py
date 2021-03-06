"""Provides device automations for deconz events."""
import voluptuous as vol

import homeassistant.components.automation.event as event

from homeassistant.components.device_automation import TRIGGER_BASE_SCHEMA
from homeassistant.components.device_automation.exceptions import (
    InvalidDeviceAutomationConfig,
)
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_EVENT,
    CONF_PLATFORM,
    CONF_TYPE,
)

from . import DOMAIN
from .config_flow import configured_gateways
from .deconz_event import CONF_DECONZ_EVENT, CONF_UNIQUE_ID
from .gateway import get_gateway_from_config_entry

CONF_SUBTYPE = "subtype"

CONF_SHORT_PRESS = "remote_button_short_press"
CONF_SHORT_RELEASE = "remote_button_short_release"
CONF_LONG_PRESS = "remote_button_long_press"
CONF_LONG_RELEASE = "remote_button_long_release"
CONF_DOUBLE_PRESS = "remote_button_double_press"
CONF_TRIPLE_PRESS = "remote_button_triple_press"
CONF_QUADRUPLE_PRESS = "remote_button_quadruple_press"
CONF_QUINTUPLE_PRESS = "remote_button_quintuple_press"
CONF_ROTATED = "remote_button_rotated"
CONF_ROTATION_STOPPED = "remote_button_rotation_stopped"
CONF_AWAKE = "remote_awakened"
CONF_MOVE = "remote_moved"
CONF_DOUBLE_TAP = "remote_double_tap"
CONF_SHAKE = "remote_gyro_activated"
CONF_FREE_FALL = "remote_falling"
CONF_ROTATE_FROM_SIDE_1 = "remote_rotate_from_side_1"
CONF_ROTATE_FROM_SIDE_2 = "remote_rotate_from_side_2"
CONF_ROTATE_FROM_SIDE_3 = "remote_rotate_from_side_3"
CONF_ROTATE_FROM_SIDE_4 = "remote_rotate_from_side_4"
CONF_ROTATE_FROM_SIDE_5 = "remote_rotate_from_side_5"
CONF_ROTATE_FROM_SIDE_6 = "remote_rotate_from_side_6"

CONF_TURN_ON = "turn_on"
CONF_TURN_OFF = "turn_off"
CONF_DIM_UP = "dim_up"
CONF_DIM_DOWN = "dim_down"
CONF_LEFT = "left"
CONF_RIGHT = "right"
CONF_OPEN = "open"
CONF_CLOSE = "close"
CONF_BOTH_BUTTONS = "both_buttons"
CONF_BUTTON_1 = "button_1"
CONF_BUTTON_2 = "button_2"
CONF_BUTTON_3 = "button_3"
CONF_BUTTON_4 = "button_4"
CONF_SIDE_1 = "side_1"
CONF_SIDE_2 = "side_2"
CONF_SIDE_3 = "side_3"
CONF_SIDE_4 = "side_4"
CONF_SIDE_5 = "side_5"
CONF_SIDE_6 = "side_6"


HUE_DIMMER_REMOTE_MODEL_GEN1 = "RWL020"
HUE_DIMMER_REMOTE_MODEL_GEN2 = "RWL021"
HUE_DIMMER_REMOTE = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1000,
    (CONF_SHORT_RELEASE, CONF_TURN_ON): 1002,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_LONG_RELEASE, CONF_TURN_ON): 1003,
    (CONF_SHORT_PRESS, CONF_DIM_UP): 2000,
    (CONF_SHORT_RELEASE, CONF_DIM_UP): 2002,
    (CONF_LONG_PRESS, CONF_DIM_UP): 2001,
    (CONF_LONG_RELEASE, CONF_DIM_UP): 2003,
    (CONF_SHORT_PRESS, CONF_DIM_DOWN): 3000,
    (CONF_SHORT_RELEASE, CONF_DIM_DOWN): 3002,
    (CONF_LONG_PRESS, CONF_DIM_DOWN): 3001,
    (CONF_LONG_RELEASE, CONF_DIM_DOWN): 3003,
    (CONF_SHORT_PRESS, CONF_TURN_OFF): 4000,
    (CONF_SHORT_RELEASE, CONF_TURN_OFF): 4002,
    (CONF_LONG_PRESS, CONF_TURN_OFF): 4001,
    (CONF_LONG_RELEASE, CONF_TURN_OFF): 4003,
}

HUE_TAP_REMOTE_MODEL = "ZGPSWITCH"
HUE_TAP_REMOTE = {
    (CONF_SHORT_PRESS, CONF_BUTTON_1): 34,
    (CONF_SHORT_PRESS, CONF_BUTTON_2): 16,
    (CONF_SHORT_PRESS, CONF_BUTTON_3): 17,
    (CONF_SHORT_PRESS, CONF_BUTTON_4): 18,
}

SYMFONISK_SOUND_CONTROLLER_MODEL = "SYMFONISK Sound Controller"
SYMFONISK_SOUND_CONTROLLER = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_DOUBLE_PRESS, CONF_TURN_ON): 1004,
    (CONF_TRIPLE_PRESS, CONF_TURN_ON): 1005,
    (CONF_ROTATED, CONF_LEFT): 2001,
    (CONF_ROTATION_STOPPED, CONF_LEFT): 2003,
    (CONF_ROTATED, CONF_RIGHT): 3001,
    (CONF_ROTATION_STOPPED, CONF_RIGHT): 3003,
}

TRADFRI_ON_OFF_SWITCH_MODEL = "TRADFRI on/off switch"
TRADFRI_ON_OFF_SWITCH = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_LONG_RELEASE, CONF_TURN_ON): 1003,
    (CONF_SHORT_PRESS, CONF_TURN_OFF): 2002,
    (CONF_LONG_PRESS, CONF_TURN_OFF): 2001,
    (CONF_LONG_RELEASE, CONF_TURN_OFF): 2003,
}

TRADFRI_OPEN_CLOSE_REMOTE_MODEL = "TRADFRI open/close remote"
TRADFRI_OPEN_CLOSE_REMOTE = {
    (CONF_SHORT_PRESS, CONF_OPEN): 1002,
    (CONF_LONG_PRESS, CONF_OPEN): 1003,
    (CONF_SHORT_PRESS, CONF_CLOSE): 2002,
    (CONF_LONG_PRESS, CONF_CLOSE): 2003,
}

TRADFRI_REMOTE_MODEL = "TRADFRI remote control"
TRADFRI_REMOTE = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_SHORT_PRESS, CONF_DIM_UP): 2002,
    (CONF_LONG_PRESS, CONF_DIM_UP): 2001,
    (CONF_LONG_RELEASE, CONF_DIM_UP): 2003,
    (CONF_SHORT_PRESS, CONF_DIM_DOWN): 3002,
    (CONF_LONG_PRESS, CONF_DIM_DOWN): 3001,
    (CONF_LONG_RELEASE, CONF_DIM_DOWN): 3003,
    (CONF_SHORT_PRESS, CONF_LEFT): 4002,
    (CONF_LONG_PRESS, CONF_LEFT): 4001,
    (CONF_LONG_RELEASE, CONF_LEFT): 4003,
    (CONF_SHORT_PRESS, CONF_RIGHT): 5002,
    (CONF_LONG_PRESS, CONF_RIGHT): 5001,
    (CONF_LONG_RELEASE, CONF_RIGHT): 5003,
}

TRADFRI_WIRELESS_DIMMER_MODEL = "TRADFRI wireless dimmer"
TRADFRI_WIRELESS_DIMMER = {
    (CONF_ROTATED, CONF_LEFT): 3002,
    (CONF_ROTATED, CONF_RIGHT): 2002,
}

AQARA_CUBE_MODEL = "lumi.sensor_cube"
AQARA_CUBE = {
    (CONF_ROTATE_FROM_SIDE_1, CONF_SIDE_2): 6002,
    (CONF_ROTATE_FROM_SIDE_1, CONF_SIDE_3): 3002,
    (CONF_ROTATE_FROM_SIDE_1, CONF_SIDE_4): 4002,
    (CONF_ROTATE_FROM_SIDE_1, CONF_SIDE_5): 1002,
    (CONF_ROTATE_FROM_SIDE_1, CONF_SIDE_6): 5002,
    (CONF_ROTATE_FROM_SIDE_2, CONF_SIDE_1): 2006,
    (CONF_ROTATE_FROM_SIDE_2, CONF_SIDE_3): 3006,
    (CONF_ROTATE_FROM_SIDE_2, CONF_SIDE_4): 4006,
    (CONF_ROTATE_FROM_SIDE_2, CONF_SIDE_5): 1006,
    (CONF_ROTATE_FROM_SIDE_2, CONF_SIDE_6): 5006,
    (CONF_ROTATE_FROM_SIDE_3, CONF_SIDE_1): 2003,
    (CONF_ROTATE_FROM_SIDE_3, CONF_SIDE_2): 6003,
    (CONF_ROTATE_FROM_SIDE_3, CONF_SIDE_4): 4003,
    (CONF_ROTATE_FROM_SIDE_3, CONF_SIDE_5): 1003,
    (CONF_ROTATE_FROM_SIDE_3, CONF_SIDE_6): 5003,
    (CONF_ROTATE_FROM_SIDE_4, CONF_SIDE_1): 2004,
    (CONF_ROTATE_FROM_SIDE_4, CONF_SIDE_2): 6004,
    (CONF_ROTATE_FROM_SIDE_4, CONF_SIDE_3): 3004,
    (CONF_ROTATE_FROM_SIDE_4, CONF_SIDE_5): 1004,
    (CONF_ROTATE_FROM_SIDE_4, CONF_SIDE_6): 5004,
    (CONF_ROTATE_FROM_SIDE_5, CONF_SIDE_1): 2001,
    (CONF_ROTATE_FROM_SIDE_5, CONF_SIDE_2): 6001,
    (CONF_ROTATE_FROM_SIDE_5, CONF_SIDE_3): 3001,
    (CONF_ROTATE_FROM_SIDE_5, CONF_SIDE_4): 4001,
    (CONF_ROTATE_FROM_SIDE_5, CONF_SIDE_6): 5001,
    (CONF_ROTATE_FROM_SIDE_6, CONF_SIDE_1): 2005,
    (CONF_ROTATE_FROM_SIDE_6, CONF_SIDE_2): 6005,
    (CONF_ROTATE_FROM_SIDE_6, CONF_SIDE_3): 3005,
    (CONF_ROTATE_FROM_SIDE_6, CONF_SIDE_4): 4005,
    (CONF_ROTATE_FROM_SIDE_6, CONF_SIDE_5): 1005,
    (CONF_MOVE, CONF_SIDE_1): 2000,
    (CONF_MOVE, CONF_SIDE_2): 6000,
    (CONF_MOVE, CONF_SIDE_3): 3000,
    (CONF_MOVE, CONF_SIDE_4): 4000,
    (CONF_MOVE, CONF_SIDE_5): 1000,
    (CONF_MOVE, CONF_SIDE_6): 5000,
    (CONF_DOUBLE_TAP, CONF_SIDE_1): 2002,
    (CONF_DOUBLE_TAP, CONF_SIDE_2): 6002,
    (CONF_DOUBLE_TAP, CONF_SIDE_3): 3003,
    (CONF_DOUBLE_TAP, CONF_SIDE_4): 4004,
    (CONF_DOUBLE_TAP, CONF_SIDE_5): 1001,
    (CONF_DOUBLE_TAP, CONF_SIDE_6): 5005,
    (CONF_AWAKE, ""): 7000,
    (CONF_FREE_FALL, ""): 7008,
    (CONF_SHAKE, ""): 7007,
}

AQARA_DOUBLE_WALL_SWITCH_MODEL = "lumi.remote.b286acn01"
AQARA_DOUBLE_WALL_SWITCH = {
    (CONF_SHORT_PRESS, CONF_LEFT): 1002,
    (CONF_LONG_PRESS, CONF_LEFT): 1001,
    (CONF_DOUBLE_PRESS, CONF_LEFT): 1004,
    (CONF_SHORT_PRESS, CONF_RIGHT): 2002,
    (CONF_LONG_PRESS, CONF_RIGHT): 2001,
    (CONF_DOUBLE_PRESS, CONF_RIGHT): 2004,
    (CONF_SHORT_PRESS, CONF_BOTH_BUTTONS): 3002,
    (CONF_LONG_PRESS, CONF_BOTH_BUTTONS): 3001,
    (CONF_DOUBLE_PRESS, CONF_BOTH_BUTTONS): 3004,
}

AQARA_DOUBLE_WALL_SWITCH_WXKG02LM_MODEL = "lumi.sensor_86sw2"
AQARA_DOUBLE_WALL_SWITCH_WXKG02LM = {
    (CONF_SHORT_PRESS, CONF_LEFT): 1002,
    (CONF_SHORT_PRESS, CONF_RIGHT): 2002,
    (CONF_SHORT_PRESS, CONF_BOTH_BUTTONS): 3002,
}

AQARA_MINI_SWITCH_MODEL = "lumi.remote.b1acn01"
AQARA_MINI_SWITCH = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_DOUBLE_PRESS, CONF_TURN_ON): 1004,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_LONG_RELEASE, CONF_TURN_ON): 1003,
}

AQARA_ROUND_SWITCH_MODEL = "lumi.sensor_switch"
AQARA_ROUND_SWITCH = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1000,
    (CONF_SHORT_RELEASE, CONF_TURN_ON): 1002,
    (CONF_DOUBLE_PRESS, CONF_TURN_ON): 1004,
    (CONF_TRIPLE_PRESS, CONF_TURN_ON): 1005,
    (CONF_QUADRUPLE_PRESS, CONF_TURN_ON): 1006,
    (CONF_QUINTUPLE_PRESS, CONF_TURN_ON): 1010,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_LONG_RELEASE, CONF_TURN_ON): 1003,
}

AQARA_SQUARE_SWITCH_MODEL = "lumi.sensor_switch.aq3"
AQARA_SQUARE_SWITCH = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_DOUBLE_PRESS, CONF_TURN_ON): 1004,
    (CONF_LONG_PRESS, CONF_TURN_ON): 1001,
    (CONF_LONG_RELEASE, CONF_TURN_ON): 1003,
    (CONF_SHAKE, ""): 1007,
}

AQARA_SQUARE_SWITCH_WXKG11LM_2016_MODEL = "lumi.sensor_switch.aq2"
AQARA_SQUARE_SWITCH_WXKG11LM_2016 = {
    (CONF_SHORT_PRESS, CONF_TURN_ON): 1002,
    (CONF_DOUBLE_PRESS, CONF_TURN_ON): 1004,
    (CONF_TRIPLE_PRESS, CONF_TURN_ON): 1005,
    (CONF_QUADRUPLE_PRESS, CONF_TURN_ON): 1006,
}

REMOTES = {
    HUE_DIMMER_REMOTE_MODEL_GEN1: HUE_DIMMER_REMOTE,
    HUE_DIMMER_REMOTE_MODEL_GEN2: HUE_DIMMER_REMOTE,
    HUE_TAP_REMOTE_MODEL: HUE_TAP_REMOTE,
    SYMFONISK_SOUND_CONTROLLER_MODEL: SYMFONISK_SOUND_CONTROLLER,
    TRADFRI_ON_OFF_SWITCH_MODEL: TRADFRI_ON_OFF_SWITCH,
    TRADFRI_OPEN_CLOSE_REMOTE_MODEL: TRADFRI_OPEN_CLOSE_REMOTE,
    TRADFRI_REMOTE_MODEL: TRADFRI_REMOTE,
    TRADFRI_WIRELESS_DIMMER_MODEL: TRADFRI_WIRELESS_DIMMER,
    AQARA_CUBE_MODEL: AQARA_CUBE,
    AQARA_DOUBLE_WALL_SWITCH_MODEL: AQARA_DOUBLE_WALL_SWITCH,
    AQARA_DOUBLE_WALL_SWITCH_WXKG02LM_MODEL: AQARA_DOUBLE_WALL_SWITCH_WXKG02LM,
    AQARA_MINI_SWITCH_MODEL: AQARA_MINI_SWITCH,
    AQARA_ROUND_SWITCH_MODEL: AQARA_ROUND_SWITCH,
    AQARA_SQUARE_SWITCH_MODEL: AQARA_SQUARE_SWITCH,
    AQARA_SQUARE_SWITCH_WXKG11LM_2016_MODEL: AQARA_SQUARE_SWITCH_WXKG11LM_2016,
}

TRIGGER_SCHEMA = TRIGGER_BASE_SCHEMA.extend(
    {vol.Required(CONF_TYPE): str, vol.Required(CONF_SUBTYPE): str}
)


def _get_deconz_event_from_device_id(hass, device_id):
    """Resolve deconz event from device id."""
    deconz_config_entries = configured_gateways(hass)
    for config_entry in deconz_config_entries.values():

        gateway = get_gateway_from_config_entry(hass, config_entry)
        for deconz_event in gateway.events:

            if device_id == deconz_event.device_id:
                return deconz_event

    return None


async def async_validate_trigger_config(hass, config):
    """Validate config."""
    config = TRIGGER_SCHEMA(config)

    device_registry = await hass.helpers.device_registry.async_get_registry()
    device = device_registry.async_get(config[CONF_DEVICE_ID])

    trigger = (config[CONF_TYPE], config[CONF_SUBTYPE])

    if device.model not in REMOTES or trigger not in REMOTES[device.model]:
        raise InvalidDeviceAutomationConfig

    return config


async def async_attach_trigger(hass, config, action, automation_info):
    """Listen for state changes based on configuration."""
    device_registry = await hass.helpers.device_registry.async_get_registry()
    device = device_registry.async_get(config[CONF_DEVICE_ID])

    trigger = (config[CONF_TYPE], config[CONF_SUBTYPE])

    trigger = REMOTES[device.model][trigger]

    deconz_event = _get_deconz_event_from_device_id(hass, device.id)
    if deconz_event is None:
        raise InvalidDeviceAutomationConfig

    event_id = deconz_event.serial

    event_config = {
        event.CONF_PLATFORM: "event",
        event.CONF_EVENT_TYPE: CONF_DECONZ_EVENT,
        event.CONF_EVENT_DATA: {CONF_UNIQUE_ID: event_id, CONF_EVENT: trigger},
    }

    event_config = event.TRIGGER_SCHEMA(event_config)
    return await event.async_attach_trigger(
        hass, event_config, action, automation_info, platform_type="device"
    )


async def async_get_triggers(hass, device_id):
    """List device triggers.

    Make sure device is a supported remote model.
    Retrieve the deconz event object matching device entry.
    Generate device trigger list.
    """
    device_registry = await hass.helpers.device_registry.async_get_registry()
    device = device_registry.async_get(device_id)

    if device.model not in REMOTES:
        return

    triggers = []
    for trigger, subtype in REMOTES[device.model].keys():
        triggers.append(
            {
                CONF_DEVICE_ID: device_id,
                CONF_DOMAIN: DOMAIN,
                CONF_PLATFORM: "device",
                CONF_TYPE: trigger,
                CONF_SUBTYPE: subtype,
            }
        )

    return triggers
