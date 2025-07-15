import esphome.codegen as cg
from esphome.components import jk_rs485_sniffer
import esphome.config_validation as cv
from esphome.const import CONF_ID

from ..jk_rs485_sniffer import CONF_JK_RS485_SNIFFER_ID, JK_RS485_SNIFFER_COMPONENT_SCHEMA, jk_rs485_sniffer_ns

AUTO_LOAD = ["jk_rs485_sniffer"]
CODEOWNERS = ["@syssi"]
MULTI_CONF = True

CONF_JK_RS485_BMS_ID = "jk_rs485_bms_id"
CONF_RS485_ADDRESS = "rs485_address"
CONF_CELL_INFO_UPDATE_INTERVAL = "cell_info_update_interval"
CONF_SETTINGS_UPDATE_INTERVAL = "settings_update_interval"
CONF_DEVICE_INFO_UPDATE_INTERVAL = "device_info_update_interval"

jk_rs485_bms_ns = cg.esphome_ns.namespace("jk_rs485_bms")
JkRS485Bms = jk_rs485_bms_ns.class_("JkRS485Bms", cg.PollingComponent, jk_rs485_sniffer.JkRS485SnifferDevice)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JkRS485Bms),
            cv.Required(CONF_RS485_ADDRESS): cv.int_,
            cv.Required(CONF_CELL_INFO_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
            cv.Required(CONF_SETTINGS_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
            cv.Required(CONF_DEVICE_INFO_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
        }
    )
    .extend(cv.polling_component_schema("5s"))
    .extend(jk_rs485_sniffer.jk_rs485_sniffer_device_schema())
)

JK_RS485_BMS_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_JK_RS485_BMS_ID): cv.use_id(JkRS485Bms),
    }
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])                               #definicion var: BMS (conf_id)
    await cg.register_component(var, config)                              #registro de var y su config
    await jk_rs485_sniffer.register_jk_rs485_bms_device(var, config)      #registro de SNIFFER_DEVICE
    cg.add(var.set_address(config[CONF_RS485_ADDRESS]))                   #JK_RS485_BMS --> address
    hub = await cg.get_variable(config[CONF_JK_RS485_SNIFFER_ID])
    #cg.add(getattr(hub, f"set_bms")(var))
    cg.add(var.set_sniffer_parent(hub))
    cg.add(hub.set_time_between_cell_info_ms(config[CONF_CELL_INFO_UPDATE_INTERVAL].total_milliseconds))
    cg.add(hub.set_time_between_settings_ms(config[CONF_SETTINGS_UPDATE_INTERVAL].total_milliseconds))
    cg.add(hub.set_time_between_device_info_ms(config[CONF_DEVICE_INFO_UPDATE_INTERVAL].total_milliseconds))
