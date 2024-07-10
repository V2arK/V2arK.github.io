# V2arK.github.io

A personal website for Honglin Cao, @V2arK.

An undergrad of University of Waterloo, currently in Year 3.

This website is based on the template HTML5 UP, and some personal touch of adding masonry item support in Gallary.

Feel free to base your own website from this as well!

All contect info is inside the website!



## Extra information
The following is my personal notes on my linux setup.

- ROG G14 2023
- Fedora 40

#### Fedora suspend/hibernate immediently wake up

The issue was the remote wakeup feature of the ITE device (USB device 1-4), and I notice this issue because after wake up, `dmesg` has lines like `suspend error -16` for `btusb` devices.

```
echo "disabled" | sudo tee /sys/bus/usb/devices/1-4/power/wakeup
```

The above will fix the issue.