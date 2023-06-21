#!/usr/bin/env python3

""" This is just a small script which takes a list of .desktop files as command line
    arguments, and sets any running Icon Task Lists on the Budgie Panel to show those
    apps.

    e.g.
        "set-tasklist firefox.desktop nemo.desktop org.gnome.gedit.desktop"

    After logout / login, the Icon Task List will show Firefox, Nemo Files, and Gedit.
    Any .desktop files that do not appear to exist will be ignored.

    The main use case for this was so that I could make a script to automate restoring
    Budgie Panel applet preferences after reinstalling or resetting the Budgie Panel,
    instead of having to manually add / remove desired Icon Task List apps every time.
"""

import gi.repository
#gi.require_version('Gio', '3.0')
from gi.repository import Gio
import sys
from PanelUUID import *

def set_icon_tasklists(tasklists, desktop_files):
    # Sets the Icon Task List to the provided desktop files
    for item in tasklists:
        apppath = panel_path +"instance/icon-tasklist/{" + item + "}/"
        tasklist_settings = Gio.Settings.new_with_path(base_schema + ".icon-tasklist", apppath)
        tasklist_settings.set_strv("pinned-launchers", desktop_files)

def is_desktop_file(file):
    try:
        launcher = Gio.DesktopAppInfo.new(file)
        return True
    except:
        # Bad error checkng, but if it fails, desktop file probably doesn't exist
        return False

if __name__ == "__main__":
    desktop_files = []
    for i in range(len(sys.argv)):
        if i > 0:
            desktop_item = sys.argv[i]
            if is_desktop_file(desktop_item):
                # Just a check to see if the desktop file actually exists
                desktop_files.append(desktop_item)
            else:
                search = Gio.DesktopAppInfo.search(desktop_item)
                if len(search) > 0:
                    # remove any returned items that we don't have an
                    # actual .desktop file for
                    for index, item in enumerate(search[0]):
                        if not is_desktop_file(item):
                            del search[0][index]
                    # and if the highest scored list is empty afterwards,
                    # chances are the 2nd spot is false matches, so lets
                    # just clear it so we can skip this parameter
                    if len(search[0]) == 0:
                        search = []
                if len(search) > 0:   
                    matches = search[0]
                    this_match = matches[0]
                    current = Gio.DesktopAppInfo.new(this_match)
                    # Sometimes, there can be items with equal score, but one may
                    # be set to not display in the menu. Chances are, we don't want
                    # this one. (*cough* VSCode). If any other items have the highest
                    # score and are NOT hidden, we will use the first one that fits 
                    # this criteria
                    isbad = current.get_nodisplay()
                    if isbad and len(search[0]) > 0:
                        found = False
                        for newcheck in search[0]:
                            lookat = Gio.DesktopAppInfo.new(newcheck)
                            if not found and not (lookat.get_nodisplay()):
                                this_match = newcheck
                                found = True
                    desktop_files.append(this_match)
                else:
                    print(desktop_item, "not found. Skipping.")

    all_tasklists = get_applet_UUIDs("Icon Task List")
    if all_tasklists == []:
        print("Error: Icon Task List not found on any panels.")
        sys.exit(1)
    else:
        if desktop_files != []:
            print("The following items will be used:\n")
            for index, item in enumerate(desktop_files):
                result = Gio.DesktopAppInfo.new(item)
                print(index + 1,") ", sys.argv[index + 1], sep="")
                print("  Name: ", result.get_name())
                print("  File: ", item)
                print()
            set_icon_tasklists(all_tasklists, desktop_files)
            print("Please logout / login to complete")
        else:
            print("Please specify desktop files to add.")
            sys.exit(2)
