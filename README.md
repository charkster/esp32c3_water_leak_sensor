# esp32c3_water_leak_sensor
Water Leak sensor that emails me when a leak is detected or battery needs to be replaced. Implemented in MicroPython.

This uses deepsleep to save battery power. The Dec 2025 esp32c3 generic MicroPython release or later is needed as the esp32.wake_on_gpio() function is very new (well done [meirarmon](https://github.com/meirarmon)!) .
I ordered the sensor from [here](https://www.etsy.com/listing/1835505749/leak-sensor-for-esphome-arduino-esp32?sr_prefetch=1).

This sensor is active-low and needs a pull-up to 3.3V on the RTC gpio pin (I use gpio2 which is RTC compatible). I wish the pull-up was included on the board as well as a high resistance voltage divider for the 3.3V to be measured by ADC channel. If you are using lightsleep, it is possible to software configure the gpio pin for a pull-up... but this is not possible for RTC pins.
I used two 400k resistors to make a voltage divider to measure the regulated 3.3V. If this voltage is measured to be less than 3.1V a low-battery warning email will be sent.

What's the difference between sleep, lightsleep and deepsleep at 5V... 17mA for sleep, 0.350mA for lightsleep and 0.170mA for deepsleep. The majority of the 0.170mA in deepsleep is the 5V -> 3.3V regulator. If you had a battery that was 3.3V and did not use the 5V -> 3.3V regulator, deepsleep is 0.0285mA (wow!). Here is the problem, you only get the low deepsleep current if VDDA is 3.3V or less. I am measuring 0.1mA when VDDA is 3.5V and 3mA when VDDA is 3.7V. The sleep current does not automatically get lower when VDDA drops... if I start out with 3.7V and it lowers to 3.3V, I still see the higher current draw. I experimented with LIR2032H batteries which have a voltage range of 3.0 to 3.8V, and had to drain them to half capacity to get the voltage down to 3.3V. ESP32C3's deepsleep voltage range is horrible. 

umail.py can be downloaded from [here](https://github.com/charkster/esp32s3_mcp9808_temp_csv_email_and_webpage) and is the only file which needs to be downloaded to the esp32c3 (along with esp32c3_water_leak_sensor.py renamed as main.py).

![picture](https://github.com/charkster/esp32c3_water_leak_sensor/blob/main/water_leak_sensor_setup.jpg)
