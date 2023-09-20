systemctl daemon-reload
systemctl start unibot
systemctl enable unibot
systemctl status unibot

project service file location:
- /etc/systemd/system/unibot.service