import machine
import ssd1306
import config

scl = machine.Pin(config.SCL_PIN)
sda = machine.Pin(config.SDA_PIN)

i2c_oled = machine.I2C(scl=scl, sda=sda)
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

def displaytem(now, working):
    dateStr = "Date: {0}/{1}/{2}".format(
        str(now.day),
        str(now.month),
        str(now.year - 2000)
    )

    timeStr = "Time: {0}:{1}:{2}".format(
        str(now.hour),
        str(now.minute),
        str(now.second)
    )

    statusStr = "Working: {0}".format(
        str(working)
    )

    oled.fill(0)
    oled.text(dateStr,2,10,1)
    oled.text(timeStr,2,30,1)
    oled.text(statusStr,2,50,1)

    oled.show()