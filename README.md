# esp32c3_water_leak_sensor
Water Leak sensor that emails me when a leak is detected or battery needs to be replaced. Implemented in MicroPython.

This uses deepsleep to save battery power. The Dec 2025 esp32c3 generic MicroPython release or later is needed as the esp32.wake_on_gpio() function is very new (well done [meirarmon](https://github.com/meirarmon)!) .
I ordered the sensor from [here](https://www.etsy.com/listing/1835505749/leak-sensor-for-esphome-arduino-esp32?sr_prefetch=1).

This sensor is active-low and needs a pull-up to 3.3V on the RTC gpio pin (I use gpio2 which is RTC compatible). I wish the pull-up was included on the board as well as a high resistance voltage divider for the 3.3V to be measured by ADC channel. If you are using lightsleep, it is possible to software configure the gpio pin for a pull-up... but this is not possible for RTC pins.
I used two 400k resistors to make a voltage divider to measure the regulated 3.3V. If this voltage is measured to be less than 3.1V a low-battery warning email will be sent.

What's the difference between sleep, lightsleep and deepsleep at 5V... 17mA for sleep, 0.350mA for lightsleep and 0.170mA for deepsleep. The majority of the 0.170mA in deepsleep is the 5V -> 3.3V regulator. If you had a battery that was 3.3V and did not use the 5V -> 3.3V regulator, deepsleep is 0.0285mA (wow!). My 3 AAA alkaline batteries have a combined 1800mAh, which should allow me 2 years of monitoring time before needing to be replaced. Normal capacity rechargable AAA batteries are 1.2V, and I measured the series voltage to be 3.7V. This can be directly connected to the 3.3V pin on the ESP32C3 Xiao board (which allows the ultra low 28uA consumption in deepsleep). Be sure not to use high-capacity rechargable batteries as they are closer to 1.3V... I measure over 4V with 3 in series, which is bad to connect to the ESP32C3's 3.3V pin (as the datasheet says that it should not exceed 3.7V). 

umail.py can be downloaded from [here](https://github.com/charkster/esp32s3_mcp9808_temp_csv_email_and_webpage) and is the only file which needs to be downloaded to the esp32c3 (along with esp32c3_water_leak_sensor.py renamed as main.py).

![picture](https://github.com/charkster/esp32c3_water_leak_sensor/blob/main/water_leak_sensor_setup.jpg)
