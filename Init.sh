#!/bin/bash

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Install UFW if not present
echo "Installing/Checking UFW..."
apt-get update
apt-get install ufw -y

# Reset UFW to default settings
ufw --force reset

# Basic UFW Configuration
echo "Configuring UFW..."
ufw default deny incoming
ufw default allow outgoing

# Allow specific services based on the machine's role
HOSTNAME=$(hostname)

case $HOSTNAME in
    "Torchic")
        # SMB Ports
        ufw allow 445/tcp
        ufw allow 139/tcp
        ;;
    "Chikorita")
        # MySQL Port
        ufw allow 3306/tcp
        ;;
    "Dialga")
        # Apache Ports
        ufw allow 80/tcp
        ufw allow 443/tcp
        ;;
esac

# Always allow these ports (competition requirement)
ufw allow 8000/tcp
ufw allow 9997/tcp

# Enable UFW
echo "Enabling UFW..."
ufw --force enable

# Password change section
echo "Starting password change process..."

# Get list of users excluding system users
USERS=$(awk -F: '$3 >= 1000 && $1 != "nobody" {print $1}' /etc/passwd)

# Change passwords for each user
for user in $USERS; do
    # Skip greyteam user as per rules
    if [[ $user == *"greyteam"* ]]; then
        echo "Skipping greyteam user as per competition rules..."
        continue
    fi
    
    # Prompt for new password
    echo "Enter new password for user: $user"
    read -s NEW_PASS

    # Change password
    echo "$user:$NEW_PASS" | chpasswd
    
    # Store passwords securely (only readable by root)
    echo "$user:$NEW_PASS" >> /root/password_changes.txt
done

# Secure the password file
chmod 600 /root/password_changes.txt

echo "Script completed!"
echo "Password changes have been logged to /root/password_changes.txt"
echo "UFW Status:"
ufw status verbose