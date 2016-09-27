import sublime
import sublime_plugin


class NormalModeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if (self.view.is_read_only()):
			self.view.set_read_only(False)
			self.view.set_status('normal_mode', 'INSERT')
		else:
			self.view.set_read_only(True)
			self.view.set_status('normal_mode', 'NORMAL')


class NormalModeListener(sublime_plugin.EventListener):
	@staticmethod
	def check_readonly(view):
		if view.is_read_only():
			view.set_status('normal_mode', 'NORMAL')
		else:
			view.set_status('normal_mode', 'INSERT')

	@staticmethod
	def enable_normal_mode(view):
		view.set_read_only(True)
		view.set_status('normal_mode', 'NORMAL')

	def on_activated_async(self, view):
		NormalModeListener.check_readonly(view)

	def on_load_async(self, view):
		NormalModeListener.enable_normal_mode(view)

	def on_new_async(self, view):
		view.set_status('normal_mode', 'INSERT')


def is_untitled(view):
	# is view a new untitled tab
	return view.size() and view.name


def plugin_loaded():
	for view in sublime.active_window().views():
		if is_untitled(view):
			NormalModeListener.enable_normal_mode(view)
		else:
			view.set_read_only(False)
			view.set_status('normal_mode', 'INSERT')
