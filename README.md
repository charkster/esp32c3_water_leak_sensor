# esp32c3_water_leak_sensor
Water Leak sensor that emails me when a leak is detected or battery needs to be replaced. Implemented in MicroPython.

This uses deepsleep to save battery power. The Dec 2025 esp32c3 generic MicroPython release or later is needed as the esp32.wake_on_gpio() function is very new (well done [meirarmon](https://github.com/meirarmon)!) .
I ordered the sensor from [here](https://www.etsy.com/listing/1835505749/leak-sensor-for-esphome-arduino-esp32?sr_prefetch=1).

This sensor is active-low and needs a pull-up to 3.3V on the RTC gpio pin (I use gpio2 which is RTC compatible). I really wish the pull-up was included on the board. If you are using lightsleep, it is possible to software configure the gpio pin for a pull-up... but this is not possible for RTC pins.
I used two 400k resistor to make a voltage divider to measure the regulated 3.3V. If this voltage is measured to be less than 3.1V a low-battery warning email will be sent.

What's the difference between lightsleep and deepsleep... 16.45mA for lightsleep and 0.167mA for deepsleep. The majority of the 0.167mA in deepsleep is the 5V -> 3.3V regulator. If you had a battery that was 3.3V and did not use the 5V -> 3.3V regulator, deepsleep is 0.0385mA (wow!). My 3 AAA alkaline batteries have a combined 1800mAh, which should allow me 2 years of monitoring time before needing to be replaced. If I used AA batteries I probably could do 5 years.

umail.py can be downloaded from [here](https://github.com/charkster/esp32s3_mcp9808_temp_csv_email_and_webpage) and is the only file which needs to be downloaded to the esp32c3 (along with esp32c3_water_leak_sensor.py renamed as main.py).

![picture](https://github.com/charkster/esp32c3_water_leak_sensor/blob/main/water_leak_sensor_setup.jpg)
