# sky_affinity
Affinity adjustment for ⛅ **Sky: Children of the Light** on AMD Ryzen 1000/2000/3000 CPUs

# How to use?
👇 👇 👇 👇 👇
- 🧮 Make sure your processor is a subjet of this, [i.e. AMD Ryzen with "core config" is "2 × something"](https://en.wikipedia.org/wiki/List_of_AMD_Ryzen_processors).
- 🔗 Go to [Releases page](https://github.com/kawashirov/sky_affinity/releases) on the right
- 📦 Download `sky_affinity.exe`
- ⌨ Press `Win+R`, type `shell:startup` and run it.
- 📂 Your system users' auto Startup folder should open.
- 📦 Put `sky_affinity.exe` into this folder (you might not see `.exe` part if file extensions are hidden by your explorer settings, but that's OK).
- 🏃‍♀️ Next and each other time you log into the system, `sky_affinity.exe` will start and run in background.
- 🏃‍♂️ Run `sky_affinity.exe`, and it will run immediatly, no restart required.
- 🖥 A console window might flash for a moment, but that's OK. ⚠ If you use **Windows Terminal**, then `sky_affinity.exe` will open there and **WILL NOT** run in background. 🤷‍♂️

👆 👆 👆 👆 👆

# Как этим пользоваться?
👇 👇 👇 👇 👇
- 🧮 Убедитесь что у вас соответсвующий процессор, [а именно AMD Ryzen где "core config" с "2 × что-то"](https://en.wikipedia.org/wiki/List_of_AMD_Ryzen_processors).
- 🔗 Перейдите на [страницу Releases](https://github.com/kawashirov/sky_affinity/releases) справа.
- 📦 Скачайте `sky_affinity.exe`
- ⌨ Нажмите `Win+R`, вставьте `shell:startup` и запустите.
- 📂 Должна открыться папка Startup автозапуска вашего пользователя системы.
- 📦 Закиньте `sky_affinity.exe` в эту папку (вы можете не видеть `.exe` если у вас в настроках проводника выключено отображение расширений, но это нормально).
- 🏃‍♀️ При следующем запуске системы `sky_affinity.exe` автоматически запустится и будет работать в фоне.
- 🏃‍♂️ Можете запустить `sky_affinity.exe` прямо сейчас, тогда вам не придется перезагружаться.
- 🖥 Может мигнуть консольное окно, но это нормально. ⚠ Если вы используете **Windows Terminal**, то `sky_affinity.exe` откроется в нём и **НЕ БУДЕТ** работать в фоне. 🤷‍♂️

👆 👆 👆 👆 👆


# Technical information
Read below only if you are nerd ☝🤓

### How does it work?
It passively monitors whether `Sky.exe` is running and ensures its CPU affinity is set to the **second half of threads**.
So, if you have CPU with 12 threads (logical cores), it will lock `Sky.exe` to cores 7-12 (6-11 if counting from 0).
The Windows scheduler should handle the rest.
Preferring second half over first half as some other software likes to bind itself to the first core for some reason.

### Why does this work?
On some older generation AMD Ryzen CPUs (mostly 1000/2000/3000 series) there is some latency when communicating across some cores.
This is because there are actually two "chips" under the hood and communicating across those "chips" is slower than within a single.
The game or Windows scheduler (not sure who exactly) can split its threads to differint "chips", which causes slowdowns and stutters some times.
**Sky: Children of the Light** isn't performance-heavy and runs fine on 2-4 cores.
So, we are locking the game into last half of cores, which usually belong to one "chip".
**This fixes stutters and lags on some systems.**
See [core-to-core-latency project page](https://github.com/nviennot/core-to-core-latency) for more info and use cases. You can measure delays by yourself!
Tested and confirmed on AMD Ryzen 2600 CPU.

### Notes
- It works in background, if you want to shut it down, kill all instances of `sky_affinity.exe` in Task Manager.
- It checks affinity periodically, so you or other software can't override affinity while `sky_affinity.exe` is running.
- The game normally runs as non-elevated process (with no admin rights), if you are running Sky as admin for some reason, then `sky_affinity.exe` will also need to be run with admin rights manually.
- The game needs at least two logical cores to run properly, so if your system has less than four logical cores, it will do nothing and exit.
- If you run another instance of `sky_affinity.exe` it will kill already running one.
- You might see there is actually two copies of `sky_affinity.exe` is running. That's OK. That's overhead of [Nuitka](https://nuitka.net/): one is the lanucher other is the program itself.
- If `sky_affinity.exe` can't be run for some reason, try to run it trough `cmd.exe` (console), there is should be more verbose errors.
- If you use **Windows Terminal**, Nuitka fails to hide console window, so new tab will be spawned and lasts all the user session. 🤷‍♂️ Not really want to make workaround for that lmao.

### How to remove?
- Go to Task Manager (press `Ctrl+Shift+Esc`).
- Kill all instances of `sky_affinity.exe` in Task Manager.
- Open Starup folder (press `Win+R` and run `shell:startup`).
- Remove `sky_affinity.exe` from Startup folder.


Have a nice day! 💐
