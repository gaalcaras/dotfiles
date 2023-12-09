/usr/bin/prime-offload
xset s off && xset -dpms
source /etc/X11/xinit/xinitrc.d/50-systemd-user.sh
eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK

[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

bluetoothctl power on

xrandr > $HOME/.xrandr_dump

xrandr --setprovideroutputsource modesseting NVIDIA-0
xrandr --auto

i3 >> $HOME/i3.log

