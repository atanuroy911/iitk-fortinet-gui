#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/IITK Fortinet Authenticator.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/IITKFAuth.dmg" && rm "dist/IITKFAuth.dmg"
create-dmg \
  --volname "IITKFAuth" \
  --volicon "img/icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "IITK Fortinet Authenticator.app" 175 120 \
  --hide-extension "IITK Fortinet Authenticator.app" \
  --app-drop-link 425 120 \
  "dist/IITKFAuth.dmg" \
  "dist/dmg/"