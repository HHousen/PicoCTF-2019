# droids0

## Problem

> Where do droid logs go. Check out this file. You can also find the file in /problems/droids0_0_205f7b4a3b23490adffddfcfc45a2ca3.

* [APK File](./zero.apk)

## Solution

1. Open the APK file in [Android Studio](https://developer.android.com/studio). Clicking the button in the app logs the flag to logcat. I searched for `picoCTF` in logcat.
2. Android Studio Notes:
    * Virtual devices can be created in `Tools > AVD Manager`.
    * To change the storage location of the device ([source](https://stackoverflow.com/a/52059066)):
        1. Create a new virtual device. Don't launch the AVD after created successfully.
        2. In AVD Manager, right click on the new created AVD and select "Show on Disk".
        3. Move the folder that is called "yourAVDname.avd" to the desired location.
        4. Open the INI file that called "yourAVDname.ini" using text editor, then replace the value of path with your desired location path.
        5. Now, launch the AVD from AVD Manager.

### Flag

`picoCTF{a.moose.once.bit.my.sister}`
