import collections
import sys
import time
import traceback

import typing

if typing.TYPE_CHECKING:
	import psutil


class Main():
	PROCESS_NAME = 'sky.exe'

	def __init__(self):
		self.cpu_count = 1
		self.sky_affinity = [0, 1]

	@staticmethod
	def get_exe_safe(p: 'psutil.Process') -> 'str|None':
		try:
			return p.exe()
		except OSError:
			return None

	@classmethod
	def ensure_single_process(cls):
		try:
			import psutil
			own_process = psutil.Process()
			own_exe = own_process.exe()

			own_processes = set()
			queue = collections.deque()  # type: collections.deque[psutil.Process]
			queue.append(own_process)
			while len(queue) > 0:
				other_ps = queue.pop()
				if other_ps is None or other_ps in own_processes:
					continue
				other_exe = cls.get_exe_safe(other_ps)
				if other_exe is None or other_exe != own_exe:
					continue
				own_processes.add(other_ps)
				queue.append(other_ps.parent())
				for child in other_ps.children():
					queue.append(child)

			print(f"Detected {len(own_processes)} own processes: {own_processes!r}")

			to_kill = list()
			for other_ps in psutil.process_iter():
				try:
					if other_ps is None or other_ps in own_processes:
						continue
					other_exe = cls.get_exe_safe(other_ps)
					if other_exe is None or other_exe != own_exe:
						continue
					print(f"Detected already running copy: {other_ps}")
					to_kill.append(other_ps)
				except Exception as exc:
					print(f"Process {other_ps} error: {exc}")

			if len(to_kill) < 1:
				return

			print(f"Have to kill {len(to_kill)} already running copies...")
			for kill_process in to_kill:
				try:
					kill_process.kill()
					print(f"Killed: {kill_process}")
				except Exception as exc:
					print(f"Failed to kill {kill_process}, error: {exc}")

		except Exception as exc:
			print(f"Failed to check single-process: {exc}")

	def sig_bind(self):
		try:
			import signal
			signal.signal(signal.SIGINT, self.sig_exit_handler)
			signal.signal(signal.SIGBREAK, self.sig_exit_handler)
			print(f"Bound signal handlers!")
		except Exception as exc:
			print(f"Failed to bind handlers: {exc}")

	@staticmethod
	def sig_exit_handler(signum, frame):
		print(f"Exit via {signum=}, {frame=}")
		sys.exit(1)

	def set_own_affinity(self):
		try:
			import psutil
			own_affinity = list(range(self.cpu_count // 2))
			print(f"Preferred own affinity: {own_affinity}")
			own_process = psutil.Process()
			own_process.cpu_affinity(own_affinity)
			print(f"Set own affinity: {own_process.cpu_affinity()}")
		except Exception as exc:
			print(f"Failed to set own affinity: {exc}")

	@staticmethod
	def set_own_nice():
		try:
			import psutil
			own_process = psutil.Process()
			own_process.nice(psutil.HIGH_PRIORITY_CLASS)
			print(f"Set own CPU priority: {own_process.nice()}")
		except Exception as exc:
			print(f"Failed to set own CPU priority class: {exc}")

	@staticmethod
	def set_own_ionice():
		try:
			import psutil
			own_process = psutil.Process()
			own_process.ionice(psutil.IOPRIO_HIGH)
			print(f"Set own IO priority: {own_process.ionice()}")
		except Exception as exc:
			print(f"Failed to set own IO priority class: {exc}")

	def prepare(self):
		try:
			import psutil

			self.sig_bind()
			self.ensure_single_process()

			self.cpu_count = cpu_count = psutil.cpu_count(logical=True)
			if cpu_count < 4:
				print(f"There is only {cpu_count} threads on the system.")
				return False
			self.sky_affinity = list(range(cpu_count // 2, cpu_count))
			print(f"Preferred sky affinity: {self.sky_affinity}")

			self.set_own_affinity()
			self.set_own_nice()
			self.set_own_ionice()
		except Exception as exc:
			print(f"Error preparing: {exc}")
			traceback.print_exception(exc)
			return False
		return True

	def try_process(self, process: 'psutil.Process'):
		if process is None:
			return
		if process.name().lower() != self.PROCESS_NAME:
			return
		# print(f"Found sky.exe: {process}")

		cur_affinity = process.cpu_affinity()
		if cur_affinity != self.sky_affinity:
			print(f"Changing {process} affinity: {cur_affinity} -> {self.sky_affinity}")
			process.cpu_affinity(self.sky_affinity)

	def try_process_loop(self):
		while True:
			try:
				import psutil
				psutil.process_iter.cache_clear()
				for process in psutil.process_iter():
					try:
						self.try_process(process)
					except Exception as exc:
						print(f"Process {process} error: {exc}")
						traceback.print_exception(exc)
			except Exception as exc:
				print(f"Error: {exc}")
				traceback.print_exception(exc)
				time.sleep(30)
			else:
				time.sleep(10)

	def main(self):
		if not self.prepare():
			return
		self.try_process_loop()
