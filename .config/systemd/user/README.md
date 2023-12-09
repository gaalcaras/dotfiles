# Systemd Units and Timers

## Units and timers overview

`email-sync` and `vdir-sync` run every 15 minutes. Each script then decides if it's time to update and sync. With the `--daily` parameter, then it's about twice a day.

## Useful commands

Enable service or timer and start immediately:

```
systemctl --user enable --now email-sync.service
systemctl --user enable --now email-sync.timer
```

Check if everything is running smoothly:

```
systemctl --user status email-sync.timer
```

After changing files, reload daemon:

```
systemctl --user daemon-reload
```

To get an overview of all timers, run:

```
systemctl --user list-timers
```

