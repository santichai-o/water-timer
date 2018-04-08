
import machine, utime
import urtc
import urequests
import display, wifi

import config

scl = machine.Pin(config.SCL_PIN)
sda = machine.Pin(config.SDA_PIN)

i2c_time = machine.I2C(scl=scl, sda=sda)

rtc = machine.RTC()
rtc = urtc.DS3231(i2c_time)
pin = machine.Pin

OUTPUT_PIN = pin(5, pin.OUT)

STATUS = False
WORKING = False

def init():
    try:
        wifi.connect()
    except Exception:
        # Catch exceptions so that device goes back to sleep if WiFi connect or
        # HTTP calls fail with exceptions
        pass
    #finally:
        #wifi.disconnect()

def sendStatus(secs, status):
    try:
        if wifi.connect():
            utcTime = 946684800 + secs - (7*60*60) #convert time to utc
            url = config.LOG_STATUS_URL.format(utcTime, status)
            req = urequests.get(url)
            req.close()

    except Exception:
        pass

def countdown(now, at):
    schedule = urtc.datetime_tuple(
                    year = now.year,
                    month = now.month,
                    day = now.day,
                    weekday = now.weekday,
                    hour = at[0],
                    minute = at[1],
                    second = 0
                )

    return urtc.tuple2seconds(now) -  urtc.tuple2seconds(schedule)

def check(now):
    global STATUS

    for at in config.AT_TIMES:
        _countdown = countdown(now, at)

        print("at {0}:{1} {2} secs".format(at[0],at[1],_countdown))

        if _countdown >= 0 and _countdown < config.WORK_DURATION:
            STATUS = True
            break
        else:
            STATUS = False

def does(secs):
    OUTPUT_PIN.value(1)
    sendStatus(secs, OUTPUT_PIN.value())

def stop(secs):
    OUTPUT_PIN.value(0)
    sendStatus(secs, OUTPUT_PIN.value())

def main():
    global STATUS
    global WORKING

    init()

    while True:
        now = rtc.datetime()

        check(now)

        if STATUS and WORKING == False:
            WORKING = True
            does(urtc.tuple2seconds(now))
            
        elif WORKING and STATUS == False:
            WORKING = False
            stop(urtc.tuple2seconds(now))

        display.displaytem(now, WORKING)

        utime.sleep(1.0)


if __name__ == "__main__":
    main()