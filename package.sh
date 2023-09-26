#!/bin/sh
# Create folders.
[ -e package ] && rm -r package
mkdir -p package/opt
mkdir -p package/usr/share/applications
mkdir -p package/usr/share/icons/hicolor/scalable/apps

# Copy files (change icon names, add lines for non-scaled icons)
cp -r dist/IITKFAuth package/opt/IITKFAuth
cp img/icon.svg package/usr/share/icons/hicolor/scalable/apps/icon.svg
cp IITKFAuth.desktop package/usr/share/applications

# Change permissions
find package/opt/IITKFAuth -type f -exec chmod 644 -- {} +
find package/opt/IITKFAuth/_internal/utils/authenticator-linux -type f -exec chmod 755 -- {} +
find package/opt/IITKFAuth -type d -exec chmod 755 -- {} +
find package/usr/share -type f -exec chmod 644 -- {} +
chmod +x package/opt/IITKFAuth/IITKFAuth