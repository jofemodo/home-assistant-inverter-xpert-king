# Home Assistant Inverter Axpert King
Home Assistant Integration for reading data from Axpert King (also known as Voltronic Axpert III) inverters via USB cable (HID Raw Device). 

## Features

- Get most of live values and current config params from inverter
- Add energy sensors for integration with energy usage
- Tracks daily energy consumption
- Sync inverter date and time (not working!)

## Todo

- Clear code
- Add options to change config params

## Notes

This code was written for couple of days without any skills in Python and HA architecture. That is first time I've used Python, so anyone is welcome to make this code better.
Due to low baud rate in inverter this integration can slow down your HA, so keep this in mind and if you can help with optimizing - you are welcome.

## Connecting Inverter using USB cable

@Jofemodo has adapted the original code from @astraliens to work with direct USB connection to the HA server (HID Raw Device).

To get things working with HA, you must grant read/write access to the HID raw device. The way you do depends on your HA setup.
In my case, using hassios on a RPi4, i chose to add an udev rule like this:

    echo -e "KERNEL==\"hidraw*\", MODE=\"0666\"" > /etc/udev/rules.d/99-hidraw.rules 

After connecting the inverter to your HA server using a "micro-USB to type-B" cable,
you need to add `home-assistant-inverter-xpert-king` integration using HACS to your HA.
In you HA go to *Main Menu -> HACS -> Integrations*, in top right corner press 3 dots and click to
"Custom Repositories". 
Add repository `https://github.com/jofemodo/home-assistant-inverter-xpert-king` and category `Integration`. 
After this step close modal add repository window and press "Explore & Download Repositories" blue button
at the bottom right corner of screen and search for `Inverter Axpert King` integration.
Press on it and in right bottom corner of screen press "Download" button. 
After this you can simply add it like regular integration, specifiying the device file name where inverter
is connected (i.e. /dev/hidraw0). In several seconds integration get data from inverter, create all found
sensors and will update them constantly.

## Date and Time sync

This integration can sync your inverter date and time, but keep in mind that it will set date and time received from HA server, so before sync ensure you HA server date and time actual.
@jofemodo didn't get this to work using the USB connection. I suspect it's an issue related with the firmware version.

## Energy consumption monitoring

You can add `Total energy all time` sensor to your energy consumption monitoring to calculate your spents

## Donations

You can say thanks by donating for buying pizza to @astraliens at:

<a href="https://www.buymeacoffee.com/astraliens" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Pizza" height="41" width="174"></a>
