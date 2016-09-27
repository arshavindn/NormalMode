import sublime
import sublime_plugin


def check_readonly(view):
  if view.is_read_only():
    view.set_status('normal_mode', 'NORMAL')
  else:
    view.set_status('normal_mode', 'INSERT')


def enable_normal_mode(view):
  view.set_read_only(True)
  view.set_status('normal_mode', 'NORMAL')


def disable_normal_mode(view):
  view.set_read_only(False)
  view.set_status('normal_mode', 'INSERT')


def enable_normal_mode_check(view):
  if view.settings().get('is_widget') is None:
    enable_normal_mode(view)


def disable_normal_mode_check(view):
  if view.settings().get('is_widget') is None:
    disable_normal_mode(view)


def toggle_view(view):
  if (view.is_read_only()):
    disable_normal_mode_check(view)
  else:
    enable_normal_mode_check(view)


def is_untitled(view):
  # is view a new untitled tab
  return view.size() and view.name


class NormalModeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    toggle_view(self.view)


class NormalModeListener(sublime_plugin.EventListener):
  def on_activated_async(self, view):
    check_readonly(view)

  def on_load_async(self, view):
    enable_normal_mode_check(view)

  def on_new_async(self, view):
    view.set_status('normal_mode', 'INSERT')


def plugin_loaded():
  for view in sublime.active_window().views():
    if is_untitled(view):
     enable_normal_mode(view)
    else:
      disable_normal_mode(view)
