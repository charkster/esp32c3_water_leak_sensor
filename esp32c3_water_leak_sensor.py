# latest Dec 12, 2025 version needed for esp32.wake_on_gpio
import machine
import network
import time
import ntptime
import utime
import esp32
import umail   # this needs to be a file saved on esp32s3

time.sleep(1) # this is needed to connect with Thonny (for debug)
d0 = machine.Pin(2, machine.Pin.IN)
esp32.wake_on_gpio((d0,), esp32.WAKEUP_ALL_LOW) # 220k pullup needed on D0

if (d0.value() == 0):
    wake = True
else:
    wake = False

def get_battery_voltage():
    adc = machine.ADC(machine.Pin(4)) # voltage divider by 2, 400k resistors
    adc.atten(machine.ADC.ATTN_11DB)
    sum = 0.0
    for n in range(0,10):
        sum += adc.read_u16()/65535*3.0 # not sure why 3.0 is more accurate than 2.5
    return (sum*2.0)/10.0

def connect_to_wifi():
    # Your network credentials
    ssid = 'your_ssid'
    password = 'your_password'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.ifconfig(('192.168.0.204', '255.255.255.0', '192.168.0.1', '205.171.3.25')) # put your static IP here
    time.sleep_ms(1000)
    wlan.active(True)
    time.sleep_ms(1000)
    wlan.connect(ssid, password)

    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if wlan.isconnected():
        print('connected')
        ntptime.timeout = 5
        try:
            ntptime.settime() # this is GMT
        except:
            try:
                ntptime.settime() # try again
            except:
                machine.reset()
        rtc = machine.RTC()
        utc_shift = -7 # Phoenix Arizona
        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)
        return True
    else:
        print(wlan.status())
        return False

def sendEmail(battery_voltage=0.0, wake=False):
    t = time.localtime()
    date = str("{:2d}/{:2d}/{:4d} {:2d}:{:02d}:{:02d}".format(t[1],t[2],t[0],t[3],t[4],t[5]))
    #initialize SMTP server and login
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Email details
    sender_email = 'your@gmail.com'
    sender_name = 'esp32c3 email'
    sender_app_password = 'your_3rd_party_gmail_password'
    recipient_email ='destination@gmail.com'
    if (wake):
        email_subject ='Water Leak Detected!!'
    else:
        email_subject ='Water Leak Sensor low battery'
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    if (wake):
        smtp.write("WATER LEAK DETECTED!!!, battery is {:.03f}V\n".format(battery_voltage))
    else:
        smtp.write("Battery voltage too low, it is {:.03f}V\n".format(battery_voltage))
    smtp.write(date)
    smtp.send()
    smtp.quit()

battery_voltage = get_battery_voltage()
if (battery_voltage < 3.1 or wake):
    if ( connect_to_wifi() ):
        sendEmail(battery_voltage,wake)
        time.sleep(5) # allow for manual testing
        if (d0.value() == 0): 
            sleep.time(24*60*60) # if leak still detected, wait for 1 day before checking again (so that constant emails are not sent)
        machine.reset() # disconnect from wifi and get ready for deepsleep again
machine.deepsleep(7*24*60*60*1000) # wake up once a week
