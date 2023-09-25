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
        screen_text = "\n".join(f"{key}: {value}" for key, value in data.items())
        self.lcd_status("Sending PARTICLE readings: \n{}".format(screen_text))

        return data

    def lcd_status(self, text):
        # Create ST7735 LCD display class
        st7735 = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=270,
            spi_speed_hz=10000000
        )

        # Initialize display
        st7735.begin()
        WIDTH = st7735.width
        HEIGHT = st7735.height

        # Set up canvas
        img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Write and display the text at the top in white
        draw.text((0, 0), text, fill=(255, 255, 255))
        st7735.display(img)


async def main():
    particle = MySensor(name="particle")
    signal = await particle.get_readings()
    print(signal)

if __name__ == '__main__':
    asyncio.run(main())
