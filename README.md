# sky_affinity
Affinity adjustment for ⛅ **Sky: Children of the Light** on Ryzen 1000/2000/3000 CPUs

# How to use?
- Go to [Releases page](https://github.com/kawashirov/sky_affinity/releases) on the right
- Download `sky_affinity.exe`
- Press `Win+R`, type `shell:startup` and run it.
- Your System Users' auto Startup folder should open
- Put `sky_affinity.exe` into this folder (you might not see `.exe` part if file extensions are hidden by your explorer settings, but that's OK)
- Next time you log into the system, `sky_affinity.exe` will start and run in background
- Run `sky_affinity.exe`, and it will run in background immediatly, no restart required.
- A console window might flash for a moment, but that's OK.

### Notes
- It works in background, if you want to shut it down, kill all instances of `sky_affinity.exe` in Task Manager.
- It checks affinity periodically, so you or other software can't override affinity while `sky_affinity.exe` is running.
- The game normally runs as non-elevated process (with no admin rights), if you are running Sky as admin for some reason, then `sky_affinity.exe` will also need to be run with admin rights manually.

### How does it work?
It passively monitors whether `Sky.exe` is running and ensures its CPU affinity is set to the **second half of threads**.
So, if you have CPU with 12 threads (logical cores), it will lock `Sky.exe` to cores 7-12 (6-11 if counting from 0).
The Windows scheduler should handle the rest.
Preferring second half over first half as some other software likes to bind itself to the first core for some reason.

### Why does this work?
On some older generation Ryzen CPUs (mostly 1000/2000/3000 series) there is some latency when communicating accross some cores.
This is because there are actually two "chips" under the hood and communicating across those "chips" is slower than within a single.
**Sky: Children of the Light** isn't performance-heavy and runs fine on 2-4 cores.
So, we are locking the game into last half of cores, which usually belong to one "chip".
**This fixes some stutters and lags on some systems.**

### How to remove?
- Kill all instances of `sky_affinity.exe` in Task Manager.
- Remove `sky_affinity.exe` from `shell:startup` folder.


Have a nice day! 💐
