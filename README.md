# plugin.program.autocompletion
Plugin to provide autocompletion for the virtual keyboard (needs skin support)

This is a fork of the famous autocompletion plugin by phil65.
Since the release of kodi 17 (krypton) phils addon has issues on android devices.
Therefore I decided to create a workaround for this issue.

In this version, the json calls have been modified, so that they work reliable on android, too.
Also, a setting for the port has been added, because this version needs the control service enabled.
The settings need to look like:

![alt text](https://user-images.githubusercontent.com/24923705/29002624-e7c80d06-7aa6-11e7-904b-222f280a8ff9.png)

The port has to match the port in the autocompletion settings.

Here are the complete installation steps:

1. Uninstall all old versions of "plugin.program.autocompletion"
2. Download this repo as .zip file
3. Install the .zip file from the previous step
4. Enable the setting "System - Services - Control - Allow remote control via HTTP" (see image above)
5. Check if the port in the previouly made system settings matches the port of the autocompletion settings
6. Enjoy (hopefully)

I tested this plugin successfully in the following environment:
- Device:         Amazon Fire Tv Stick 1
- Firmware:       Fire OS 5.2.4.1 (no root)
- Platform:       Android
- Kodi:           Kodi 17.3 (Krypton, ARMV7A 32 Bit)
- Skin:           Aeon Nox 5

All credits for this great addon go to phil65 .
