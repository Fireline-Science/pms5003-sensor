from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from .pms5003_sensor import MySensor


Registry.register_resource_creator(Sensor.SUBTYPE, MySensor.MODEL, ResourceCreatorRegistration(MySensor.new))