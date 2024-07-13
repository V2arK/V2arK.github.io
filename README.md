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

#### hibernate setup

Firstly, follows the [guide to enable hibernate on Fedora 35 / Framework laptop](https://community.frame.work/t/guide-framework-16-hibernate-w-swapfile-setup-on-fedora-40/53080).

Then, I found out there are preferials stopping the laptop from getting into hibernate / suspend state. Some dig into `dmesg` shows it's the bluetooth's and usb's issue. So, change the `/usr/lib/systemd/system-sleep/hibernate-pre-post.sh` to contain:

```bash
#!/bin/bash
WiFiModule=mt7921e

case "$1 $2" in
  "pre hibernate" | "pre suspend-then-hibernate")
    modprobe -r $WiFiModule
    rfkill block bluetooth
    ;;
  "post hibernate" | "post suspend-then-hibernate")
    modprobe $WiFiModule
    rfkill unblock bluetooth
    ;;
  *)
    :
    ;;
esac
```
(Disable bluetooth / enable bluetooth)

#### misc setup

install `asusctl`, `supergfxctll`, then create script `/etc/profile.d/user_setup.sh`:

```bash
# Anime matrix
asusctl anime --enable-display true
asusctl anime --off-when-unplugged true >> /dev/null 2>&1

# fan curve (quiet setting)
asusctl fan-curve -m quiet -D 30c:0,40c:0,50c:0,60c:0,70c:35,80c:55,90c:65,100c:65 -e true -f gpu >> /dev/null 2>&1
asusctl fan-curve -m quiet -D 30c:0,40c:0,50c:0,60c:0,70c:35,80c:55,90c:65,100c:65 -e true -f cpu >> /dev/null 2>&1

# fixing cannot suspend issue (disable usb auto wakeup)
echo "disabled" | sudo tee /sys/bus/usb/devices/1-4/power/wakeup >> /dev/null 2&>2
```
(this script will be run on log in)