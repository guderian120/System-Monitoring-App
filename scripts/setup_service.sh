#!/bin/bash
# Create systemd service file
cat <<EOF > /etc/systemd/system/python_exporter.service
[Unit]
Description=Python System Metrics Exporter
After=network.target

[Service]
User=root
WorkingDirectory=/opt/python_exporter
ExecStart=/usr/bin/python3 /opt/python_exporter/python_exporter.py
Restart=always

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
chmod 755 /opt/python_exporter/python_exporter.py
chown -R root:root /opt/python_exporter

# Open firewall ports if needed
if command -v ufw >/dev/null; then
    ufw allow 8000/tcp
    ufw allow 8001/tcp
fi

# Reload systemd
systemctl daemon-reload
systemctl enable python_exporter.service