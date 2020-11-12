# Projector Screen Control

Control a motorized projector screen using a web application hosted on a Raspberry Pi.

## systemd

```
$ cat /etc/systemd/system/projector.service
[Unit]
Description=Projector web control
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/env python3 /home/alex/screen/src/controller/controller.py

[Install]
WantedBy=multi-user.target
```

```
$ cat /etc/systemd/system/harmony-projector.service
[Unit]
Description=Watch Harmony hub for projector activity status
After=projector.service

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/env python3 /home/alex/screen/src/controller/harmony_sync.py

[Install]
WantedBy=multi-user.target
```