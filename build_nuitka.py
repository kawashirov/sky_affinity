import subprocess
import sys
import signal
import time
import datetime

if __name__ == '__main__':
	APP_VERSION = "0.1.0.0"
	APP_NAME="sky_affinity"

	url = 'https://github.com/kawashirov/'
	nofollow = [
		# Т.к. мы только на шындовс, можно выкинуть ненужное.
		'psutil._psaix', 'psutil._psbsd', 'psutil._pslinux', 'psutil._psosx', 'psutil._psposix',  'psutil._pssunos'
	]

	nuitka_cmd = [
		sys.executable,
		'-m', 'nuitka',
		# '--msvc=latest',
		'--low-memory',
		'--jobs=8',

		'--assume-yes-for-downloads',
		'--warn-implicit-exceptions',
		'--warn-unusual-code',
		'--show-progress',
		'--show-modules',
		#
		'--copyright=kawashirov',
		'--company-name=kawashirov',
		f'--product-name={APP_NAME}',
		f'--file-version={APP_VERSION}',
		f'--product-version={APP_VERSION}',
		f'--file-description={url}',
		# '--windows-uac-admin',
		'--windows-console-mode=hide',
		'--onefile-tempdir-spec={TEMP}\\' + APP_NAME + '_{PID}_{TIME}',
		#
		f'--include-package={APP_NAME}',
		f'--include-package-data={APP_NAME}',
		'--python-flag=-OO',
		'--follow-stdlib',
		*(f'--nofollow-import-to={m}' for m in nofollow),
		#
		f'--onefile', APP_NAME,
		'-o', f'{APP_NAME}.exe'
	]

	time_begin = time.monotonic()
	try:
		with subprocess.Popen(nuitka_cmd, stdin=subprocess.DEVNULL) as proc:
			while proc.poll() is None:
				try:
					proc.wait()
				except KeyboardInterrupt:
					proc.send_signal(signal.SIGBREAK)
	finally:
		dt = datetime.timedelta(seconds=time.monotonic() - time_begin)
		print(f'Nuitka building time spent: {dt!s}')
