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
- install `asusctl`, `supergfxctl`

#### `NVIDIA` driver setup

```bash
sudo dnf install akmod-nvidia # rhel/centos users can use kmod-nvidia instead
sudo dnf install xorg-x11-drv-nvidia-cuda #optional for cuda/nvdec/nvenc support
sudo dnf module install nvidia-driver:latest-dkms
```

reboot, then you should see two GPU appear in `nvtop`.

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

#### password-less `sudo`

add yourself to `wheel` usergroup: `sudo usermod -aG wheel <username>`

`visudo` (it's using `nano`), add line: `%wheel  ALL=(ALL)       NOPASSWD: ALL`

#### misc setup

create script `/etc/profile.d/user_setup.sh`:

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

#### softwares

```bash
# install fctix5 Chinese input
# you will need further setting after reboot
sudo dnf install fcitx5 fcitx5-configtool fcitx5-gtk fcitx5-autostart fcitx5-qt fcitx5-chinese-addons  fcitx5-data kcm-fcitx5 

# Latex support
sudo dnf install texlive-scheme-full 

# vs code
sudo dnf install code

# native wechat (only at fedora)
flatpak install flathub com.tencent.WeChat

# homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# mail client
sudo dnf install thunderbord

```

#### `GNOME` extensions

[clipboard indicator](https://extensions.gnome.org/extension/779/clipboard-indicator/)
[system stat](https://extensions.gnome.org/extension/3010/system-monitor-next/)
[input method panel](https://extensions.gnome.org/extension/261/kimpanel/)


#### my `.bashrc` (choose what you need)

```bash
# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
    for rc in ~/.bashrc.d/*; do
        if [ -f "$rc" ]; then
            . "$rc"
        fi
    done
fi
unset rc

export EDITOR=vim

# qol
alias sshnas="ssh v2ark@10.0.0.104"
alias sshcs="ssh h45cao@linux.student.cs.uwaterloo.ca"
alias open="xdg-open"
alias pipUpdate="pip3 list --outdated | grep wheel | awk '{print $1}' | xargs -n1 pip3 install -U"

# bashrc
alias sb="source ~/.bashrc"
alias vb="vim ~/.bashrc"
alias cb="code ~/.bashrc"

# CS488
alias build488="cmake ./ && make && ./CS488"
alias build488quiet=" cmake >> /dev/null 2>&1 ./ && make >> /dev/null 2>&1  && ./CS488"
alias zip488="zip -r A2.zip src screenshots README.md -x \"*GLEW*\" \"*GLFW*\" \"src/linalg.h\" \"src/gif.h\" \"src/stb*\""

# build project
alias bp="cd ~/FluidSim; cmake . && make && cd bin && ./*"

# functions

# Copy Full Filename
cff ()
{
  if [ -z "$1" ]; then
    echo "Usage: cfp file_name"
    return 1
  fi

  filepath=$(find $(pwd) | grep "$1" | head -1)

  echo "$filepath" | xclip -selection clipboard
  echo "Copied to clipboard: $filepath"

}

alias cpf="xclip-copyfile" # copy file to clipboard

mkcd ()
{
    mkdir -p -- "$1" &&
       cd -P -- "$1"
}

# oh my posh settings
# eval "$(oh-my-posh init bash)"
eval "$(oh-my-posh init bash --config ~/.config/oh-my-posh/clean-detailed.omp.json)"

# homebrew settings
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

```

#### Keybindings


Save the following [code](https://askubuntu.com/questions/26056/where-are-gnome-keyboard-shortcuts-stored) as `keybinding.pl`, `chmod 755 keybinding.pl`.
```pl
#!/usr/bin/perl

use strict;

my $action = '';
my $filename = '-';

for my $arg (@ARGV){
    if ($arg eq "-e" or $arg eq "--export"){
        $action = 'export';
    } elsif ($arg eq "-i" or $arg eq "--import"){
        $action = 'import';
    } elsif ($arg eq "-h" or $arg eq "--help"){
        print "Import and export keybindings\n";
        print " -e, --export <filename>\n";
        print " -i, --import <filename>\n";
        print " -h, --help\n";
        exit;
    } elsif ($arg =~ /^\-/){
        die "Unknown argument $arg";
    } else {
        $filename = $arg;
        if (!$action){
            if ( -e $filename){
                $action='import';
            } else {
                $action='export';
            }
        }
    }
}

$action='export' if (!$action);
if ($action eq 'export'){
    &export();
} else {
    &import();
}

sub export(){
    my $gsettingsFolders = [
        ['org.gnome.desktop.wm.keybindings','.'],
        ['org.gnome.settings-daemon.plugins.power','button'],
        ['org.gnome.settings-daemon.plugins.media-keys','.'],
    ];

    my $customBindings = [
    ];

    $filename = ">$filename";
    open (my $fh, $filename) || die "Can't open file $filename: $!";

    for my $folder (@$gsettingsFolders){
        my @keylist = split(/\n/, `gsettings list-recursively $folder->[0]`);
        foreach my $line (@keylist){
            if ($line =~ /^([^ ]+) ([^ ]+)(?: \@[a-z]+)? (.*)/){
                my ($path, $name, $value) = ($1,$2,$3);
                if ($name eq "custom-keybindings"){
                    $value =~ s/[\[\]\' ]//g;
                    my @c = split(/,/, $value);
                    $customBindings = \@c;
                } elsif ($name =~ /$folder->[1]/){
                    if ($value =~ /^\[|\'/){
                        if ($value =~ /^\[\'(?:disabled)?\'\]$/){
                            $value = '[]';
                        } 
                        print $fh "$path\t$name\t$value\n";
                    }
                }        
            } else {
                die "Could note parse $line";
            }
        }
    }   

    for my $folder (@$customBindings){
        my $gs = `gsettings list-recursively org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:$folder`;
        my ($binding) = $gs =~ /org.gnome.settings-daemon.plugins.media-keys.custom-keybinding binding (\'[^\n]+\')/g;
        my ($command) = $gs =~ /org.gnome.settings-daemon.plugins.media-keys.custom-keybinding command (\'[^\n]+\')/g;
        my ($name) = $gs =~ /org.gnome.settings-daemon.plugins.media-keys.custom-keybinding name (\'[^\n]+\')/g;
        $command =~ s/\"/\\\"/g;
        $command =~ s/^'(.*)'$/$1/g;
        $command =~ s/\'/\'\\\'\'/g;
        $command = "\'$command\'";
        print $fh "custom\t$name\t$command\t$binding\n"    
    }

    close($fh);
}

sub import(){

    $filename = "<$filename";
    open (my $fh, $filename) || die "Can't open file $filename: $!";

    my $customcount=0;

    while (my $line = <$fh>){
        chomp $line;
        if ($line){
            my @v = split(/\t/, $line);
            if (@v[0] eq 'custom'){
                my ($custom, $name, $command, $binding) = @v;
                print "Installing custom keybinding: $name\n";
                    print `gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$customcount/ name \"$name\"`;
                print `gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$customcount/ command \"$command\"`;
                print `gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$customcount/ binding \"$binding\"`;
                $customcount++;
            } else {
                my ($path, $name, $value) = @v;
                print "Importing $path $name\n";
                print `gsettings set \"$path\" \"$name\" \"$value\"`;
            }
        }       
    }
    if ($customcount > 0){
        my $customlist = "";
        for (my $i=0; $i<$customcount; $i++){
            $customlist .= "," if ($customlist);
            $customlist .= "'/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom$i/'";            
        }
        $customlist = "[$customlist]";
        print "Importing list of custom keybindings.\n";
        print `gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \"$customlist\"`;
    }

    close($fh);
}
```

Save the following as `keys.csv` (theses are my setup), and do `./keybindings.pl -i /tmp/keys.csv`.

```
org.gnome.desktop.wm.keybindings	activate-window-menu	['<Alt>space']
org.gnome.desktop.wm.keybindings	always-on-top	[]
org.gnome.desktop.wm.keybindings	begin-move	['<Alt>F7']
org.gnome.desktop.wm.keybindings	begin-resize	['<Alt>F8']
org.gnome.desktop.wm.keybindings	close	['<Super>q']
org.gnome.desktop.wm.keybindings	cycle-group	['<Alt>F6']
org.gnome.desktop.wm.keybindings	cycle-group-backward	['<Shift><Alt>F6']
org.gnome.desktop.wm.keybindings	cycle-panels	['<Control><Alt>Escape']
org.gnome.desktop.wm.keybindings	cycle-panels-backward	['<Shift><Control><Alt>Escape']
org.gnome.desktop.wm.keybindings	cycle-windows	['<Alt>Escape']
org.gnome.desktop.wm.keybindings	cycle-windows-backward	['<Shift><Alt>Escape']
org.gnome.desktop.wm.keybindings	lower	[]
org.gnome.desktop.wm.keybindings	maximize	['<Super>Up']
org.gnome.desktop.wm.keybindings	maximize-horizontally	[]
org.gnome.desktop.wm.keybindings	maximize-vertically	[]
org.gnome.desktop.wm.keybindings	minimize	['<Super>h']
org.gnome.desktop.wm.keybindings	move-to-center	[]
org.gnome.desktop.wm.keybindings	move-to-corner-ne	[]
org.gnome.desktop.wm.keybindings	move-to-corner-nw	[]
org.gnome.desktop.wm.keybindings	move-to-corner-se	[]
org.gnome.desktop.wm.keybindings	move-to-corner-sw	[]
org.gnome.desktop.wm.keybindings	move-to-monitor-down	['<Super><Shift>Down']
org.gnome.desktop.wm.keybindings	move-to-monitor-left	['<Super><Shift>Left']
org.gnome.desktop.wm.keybindings	move-to-monitor-right	['<Super><Shift>Right']
org.gnome.desktop.wm.keybindings	move-to-monitor-up	['<Super><Shift>Up']
org.gnome.desktop.wm.keybindings	move-to-side-e	[]
org.gnome.desktop.wm.keybindings	move-to-side-n	[]
org.gnome.desktop.wm.keybindings	move-to-side-s	[]
org.gnome.desktop.wm.keybindings	move-to-side-w	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-1	['<Super><Shift>Home']
org.gnome.desktop.wm.keybindings	move-to-workspace-10	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-11	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-12	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-2	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-3	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-4	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-5	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-6	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-7	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-8	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-9	[]
org.gnome.desktop.wm.keybindings	move-to-workspace-down	['<Control><Shift><Alt>Down']
org.gnome.desktop.wm.keybindings	move-to-workspace-last	['<Super><Shift>End']
org.gnome.desktop.wm.keybindings	move-to-workspace-left	['<Shift><Control><Super>Left']
org.gnome.desktop.wm.keybindings	move-to-workspace-right	['<Shift><Control><Super>Right']
org.gnome.desktop.wm.keybindings	move-to-workspace-up	['<Control><Shift><Alt>Up']
org.gnome.desktop.wm.keybindings	panel-main-menu	[]
org.gnome.desktop.wm.keybindings	panel-run-dialog	['<Alt>F2']
org.gnome.desktop.wm.keybindings	raise	[]
org.gnome.desktop.wm.keybindings	raise-or-lower	[]
org.gnome.desktop.wm.keybindings	set-spew-mark	[]
org.gnome.desktop.wm.keybindings	show-desktop	[]
org.gnome.desktop.wm.keybindings	switch-applications	['<Super>Tab', '<Alt>Tab']
org.gnome.desktop.wm.keybindings	switch-applications-backward	['<Shift><Super>Tab', '<Shift><Alt>Tab']
org.gnome.desktop.wm.keybindings	switch-group	['<Super>Above_Tab', '<Alt>Above_Tab']
org.gnome.desktop.wm.keybindings	switch-group-backward	['<Shift><Super>Above_Tab', '<Shift><Alt>Above_Tab']
org.gnome.desktop.wm.keybindings	switch-input-source	[]
org.gnome.desktop.wm.keybindings	switch-input-source-backward	[]
org.gnome.desktop.wm.keybindings	switch-panels	['<Control><Alt>Tab']
org.gnome.desktop.wm.keybindings	switch-panels-backward	['<Shift><Control><Alt>Tab']
org.gnome.desktop.wm.keybindings	switch-to-workspace-1	['<Super>Home']
org.gnome.desktop.wm.keybindings	switch-to-workspace-10	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-11	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-12	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-2	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-3	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-4	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-5	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-6	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-7	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-8	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-9	[]
org.gnome.desktop.wm.keybindings	switch-to-workspace-down	['<Control><Alt>Down']
org.gnome.desktop.wm.keybindings	switch-to-workspace-last	['<Super>End']
org.gnome.desktop.wm.keybindings	switch-to-workspace-left	['<Super>Page_Up', '<Super><Alt>Left', '<Control><Alt>Left']
org.gnome.desktop.wm.keybindings	switch-to-workspace-right	['<Super>Page_Down', '<Super><Alt>Right', '<Control><Alt>Right']
org.gnome.desktop.wm.keybindings	switch-to-workspace-up	['<Control><Alt>Up']
org.gnome.desktop.wm.keybindings	switch-windows	[]
org.gnome.desktop.wm.keybindings	switch-windows-backward	[]
org.gnome.desktop.wm.keybindings	toggle-above	[]
org.gnome.desktop.wm.keybindings	toggle-fullscreen	[]
org.gnome.desktop.wm.keybindings	toggle-maximized	['<Alt>F10']
org.gnome.desktop.wm.keybindings	toggle-on-all-workspaces	[]
org.gnome.desktop.wm.keybindings	unmaximize	['<Super>Down', '<Alt>F5']
org.gnome.settings-daemon.plugins.power	power-button-action	'hibernate'
org.gnome.settings-daemon.plugins.media-keys	battery-status	[]
org.gnome.settings-daemon.plugins.media-keys	battery-status-static	['XF86Battery']
org.gnome.settings-daemon.plugins.media-keys	calculator	[]
org.gnome.settings-daemon.plugins.media-keys	calculator-static	['XF86Calculator']
org.gnome.settings-daemon.plugins.media-keys	control-center	[]
org.gnome.settings-daemon.plugins.media-keys	control-center-static	['XF86Tools']
org.gnome.settings-daemon.plugins.media-keys	decrease-text-size	[]
org.gnome.settings-daemon.plugins.media-keys	eject	[]
org.gnome.settings-daemon.plugins.media-keys	eject-static	['XF86Eject']
org.gnome.settings-daemon.plugins.media-keys	email	[]
org.gnome.settings-daemon.plugins.media-keys	email-static	['XF86Mail']
org.gnome.settings-daemon.plugins.media-keys	help	['', '<Super>F1']
org.gnome.settings-daemon.plugins.media-keys	hibernate	[]
org.gnome.settings-daemon.plugins.media-keys	hibernate-static	['XF86Suspend', 'XF86Hibernate']
org.gnome.settings-daemon.plugins.media-keys	home	[]
org.gnome.settings-daemon.plugins.media-keys	home-static	['XF86Explorer']
org.gnome.settings-daemon.plugins.media-keys	increase-text-size	[]
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-down	[]
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-down-static	['XF86KbdBrightnessDown']
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-toggle	[]
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-toggle-static	['XF86KbdLightOnOff']
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-up	[]
org.gnome.settings-daemon.plugins.media-keys	keyboard-brightness-up-static	['XF86KbdBrightnessUp']
org.gnome.settings-daemon.plugins.media-keys	logout	['<Control><Alt>Delete']
org.gnome.settings-daemon.plugins.media-keys	magnifier	['<Alt><Super>8']
org.gnome.settings-daemon.plugins.media-keys	magnifier-zoom-in	['<Alt><Super>equal']
org.gnome.settings-daemon.plugins.media-keys	magnifier-zoom-out	['<Alt><Super>minus']
org.gnome.settings-daemon.plugins.media-keys	media	[]
org.gnome.settings-daemon.plugins.media-keys	media-static	['XF86AudioMedia']
org.gnome.settings-daemon.plugins.media-keys	mic-mute	[]
org.gnome.settings-daemon.plugins.media-keys	mic-mute-static	['XF86AudioMicMute']
org.gnome.settings-daemon.plugins.media-keys	next	[]
org.gnome.settings-daemon.plugins.media-keys	next-static	['XF86AudioNext', '<Ctrl>XF86AudioNext']
org.gnome.settings-daemon.plugins.media-keys	on-screen-keyboard	[]
org.gnome.settings-daemon.plugins.media-keys	pause	[]
org.gnome.settings-daemon.plugins.media-keys	pause-static	['XF86AudioPause']
org.gnome.settings-daemon.plugins.media-keys	play	[]
org.gnome.settings-daemon.plugins.media-keys	play-static	['XF86AudioPlay', '<Ctrl>XF86AudioPlay']
org.gnome.settings-daemon.plugins.media-keys	playback-forward	[]
org.gnome.settings-daemon.plugins.media-keys	playback-forward-static	['XF86AudioForward']
org.gnome.settings-daemon.plugins.media-keys	playback-random	[]
org.gnome.settings-daemon.plugins.media-keys	playback-random-static	['XF86AudioRandomPlay']
org.gnome.settings-daemon.plugins.media-keys	playback-repeat	[]
org.gnome.settings-daemon.plugins.media-keys	playback-repeat-static	['XF86AudioRepeat']
org.gnome.settings-daemon.plugins.media-keys	playback-rewind	[]
org.gnome.settings-daemon.plugins.media-keys	playback-rewind-static	['XF86AudioRewind']
org.gnome.settings-daemon.plugins.media-keys	power	[]
org.gnome.settings-daemon.plugins.media-keys	power-static	['XF86PowerOff']
org.gnome.settings-daemon.plugins.media-keys	previous	[]
org.gnome.settings-daemon.plugins.media-keys	previous-static	['XF86AudioPrev', '<Ctrl>XF86AudioPrev']
org.gnome.settings-daemon.plugins.media-keys	rfkill	[]
org.gnome.settings-daemon.plugins.media-keys	rfkill-bluetooth	[]
org.gnome.settings-daemon.plugins.media-keys	rfkill-bluetooth-static	['XF86Bluetooth']
org.gnome.settings-daemon.plugins.media-keys	rfkill-static	['XF86WLAN', 'XF86UWB', 'XF86RFKill']
org.gnome.settings-daemon.plugins.media-keys	rotate-video-lock	[]
org.gnome.settings-daemon.plugins.media-keys	rotate-video-lock-static	['<Super>o', 'XF86RotationLockToggle']
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-cycle	[]
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-cycle-static	['XF86MonBrightnessCycle']
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-down	[]
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-down-static	['XF86MonBrightnessDown']
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-up	[]
org.gnome.settings-daemon.plugins.media-keys	screen-brightness-up-static	['XF86MonBrightnessUp']
org.gnome.settings-daemon.plugins.media-keys	screenreader	['<Alt><Super>s']
org.gnome.settings-daemon.plugins.media-keys	screensaver	['<Super>l']
org.gnome.settings-daemon.plugins.media-keys	screensaver-static	['XF86ScreenSaver']
org.gnome.settings-daemon.plugins.media-keys	search	[]
org.gnome.settings-daemon.plugins.media-keys	search-static	['XF86Search']
org.gnome.settings-daemon.plugins.media-keys	stop	[]
org.gnome.settings-daemon.plugins.media-keys	stop-static	['XF86AudioStop']
org.gnome.settings-daemon.plugins.media-keys	suspend	[]
org.gnome.settings-daemon.plugins.media-keys	suspend-static	['XF86Sleep']
org.gnome.settings-daemon.plugins.media-keys	toggle-contrast	[]
org.gnome.settings-daemon.plugins.media-keys	touchpad-off	[]
org.gnome.settings-daemon.plugins.media-keys	touchpad-off-static	['XF86TouchpadOff']
org.gnome.settings-daemon.plugins.media-keys	touchpad-on	[]
org.gnome.settings-daemon.plugins.media-keys	touchpad-on-static	['XF86TouchpadOn']
org.gnome.settings-daemon.plugins.media-keys	touchpad-toggle	[]
org.gnome.settings-daemon.plugins.media-keys	touchpad-toggle-static	['XF86TouchpadToggle', '<Ctrl><Super>XF86TouchpadToggle']
org.gnome.settings-daemon.plugins.media-keys	volume-down	[]
org.gnome.settings-daemon.plugins.media-keys	volume-down-precise	[]
org.gnome.settings-daemon.plugins.media-keys	volume-down-precise-static	['<Shift>XF86AudioLowerVolume', '<Ctrl><Shift>XF86AudioLowerVolume']
org.gnome.settings-daemon.plugins.media-keys	volume-down-quiet	[]
org.gnome.settings-daemon.plugins.media-keys	volume-down-quiet-static	['<Alt>XF86AudioLowerVolume', '<Alt><Ctrl>XF86AudioLowerVolume']
org.gnome.settings-daemon.plugins.media-keys	volume-down-static	['XF86AudioLowerVolume', '<Ctrl>XF86AudioLowerVolume']
org.gnome.settings-daemon.plugins.media-keys	volume-mute	[]
org.gnome.settings-daemon.plugins.media-keys	volume-mute-quiet	[]
org.gnome.settings-daemon.plugins.media-keys	volume-mute-quiet-static	['<Alt>XF86AudioMute']
org.gnome.settings-daemon.plugins.media-keys	volume-mute-static	['XF86AudioMute']
org.gnome.settings-daemon.plugins.media-keys	volume-up	[]
org.gnome.settings-daemon.plugins.media-keys	volume-up-precise	[]
org.gnome.settings-daemon.plugins.media-keys	volume-up-precise-static	['<Shift>XF86AudioRaiseVolume', '<Ctrl><Shift>XF86AudioRaiseVolume']
org.gnome.settings-daemon.plugins.media-keys	volume-up-quiet	[]
org.gnome.settings-daemon.plugins.media-keys	volume-up-quiet-static	['<Alt>XF86AudioRaiseVolume', '<Alt><Ctrl>XF86AudioRaiseVolume']
org.gnome.settings-daemon.plugins.media-keys	volume-up-static	['XF86AudioRaiseVolume', '<Ctrl>XF86AudioRaiseVolume']
org.gnome.settings-daemon.plugins.media-keys	www	[]
org.gnome.settings-daemon.plugins.media-keys	www-static	['XF86WWW']
custom	'terminal'	'gnome-terminal'	'<Super>t'
custom	'suspend'	'systemctl suspend'	'Launch1'

```