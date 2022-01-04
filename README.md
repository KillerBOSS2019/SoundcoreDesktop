## Disclaimer
This is an **unofficial** API for the Anker SoundCore Life Headphones. I am not partnered with Soundcore or Anker in any way.

## Supported Devices
The Anker Soundcore Life Q30 is the only device I currently own, making me only able to test this one. However, other devices such as the Q35 should still work properly despite this. If not, feel free to report an Issue or send a Pull Request.

## The Soundcore Life API
This API allows you to control your device's :
- Equalization Settings (Only Premade Equalizers are currently supported.)
- Noise Cancellation Mode : Active Noise Cancellation (Transport, Indoors and Outdoors), Transparency and Normal.

## The SoundcoreDesktop Application
An example SoundcoreDesktop application is also bundled with the standalone API in the `SoundcoreDesktop` folder.

![image](https://user-images.githubusercontent.com/55416314/126011831-b77996ae-1cb2-49b3-8cec-a9e26c19a4d4.png)
![image](https://user-images.githubusercontent.com/55416314/126011862-49f62487-d899-449f-9fc9-383d0d700d7c.png)
![image](https://user-images.githubusercontent.com/55416314/126011892-dc50b16c-1f12-4722-8c99-f7e0a35cd49a.png)

You will need to obtain your headphone's MAC Address. Most Bluetooth utilities, including those provided by your operating system, should allow you to find it easily.
After that is done, you will need to execute the Main.py and click on the Settings button.
It should open a new window with an input box. In that box, you will need to insert the address of your headset and then you can click Submit.
You'll now be able to control your device from your desktop.

Note that if the Soundcore Mobile Application is running and connected to your headphone, then the Desktop Application will **NOT** Work.
The Soundcore Devices can only support **one** application controlling it at a time. Exiting out of the Mobile Application should solve the issue.

The images inside of the GUI come from the official Soundcore App for Android. *They are copyrighted by Soundcore, and I do not recommend using them in your own projects.*

## Bug Reports / Contributions / Suggestions

You can report bugs or suggest features for both the API and the application by making an Issue, or you can contribute to the project by forking it and then sending a Pull Request. Any help will be very much appreciated. Thank you !
