import gi.repository
from gi.repository import Gio

base_schema = "com.solus-project"
panel_schema = base_schema + ".budgie-panel"
panel_path = "/com/solus-project/budgie-panel/"

def get_applet_UUIDs(applet_name):
    # Returns the UUIDs of all applets with the given name currently on the panel
    applets = []
    found_applets = []
    panel_settings = Gio.Settings(schema=panel_schema)
    allpanels_list = panel_settings.get_strv("panels")
    for p in allpanels_list:
        # Search each Budgie Panel and get a list of all the installed applets
        curr_panel_path = panel_path + "panels/{" + p + "}/"
        curr_panel_subject_settings = Gio.Settings.new_with_path(panel_schema + ".panel", curr_panel_path)
        active_applets = curr_panel_subject_settings.get_strv("applets")
        for app in active_applets:
            # Search all installed applets and see which ones have the given name
            curr_apppath = panel_path + "applets/{" + app + "}/"
            curr_app_settings = Gio.Settings.new_with_path(panel_schema + ".applet", curr_apppath)
            name = curr_app_settings.get_string("name")
            if name == applet_name:
                found_applets.append(app)
    return found_applets

