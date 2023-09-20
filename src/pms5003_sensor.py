import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from pms5003 import PMS5003, ReadTimeoutError

class MySensor(Sensor):
    # Subclass the Viam Arm component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("tuneni", "sensor"), "pms5003")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        sensor = cls(config.name)
        return sensor

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:

        pms5003 = PMS5003()

        try:
            readings = pms5003.read()
        except ReadTimeoutError:
            pms5003 = PMS5003()

        ultrafine_readings = readings.data[0]
        combustion_readings = readings.data[1]
        dust_pollen_readings = readings.data[2]

        data = {'Ultrafine': ultrafine_readings, 'Combustion': combustion_readings, 'Dust/Pollen': dust_pollen_readings}

        return data


async def main():
    particle = MySensor(name="particle")
    signal = await particle.get_readings()
    print(signal)

if __name__ == '__main__':
    asyncio.run(main())
