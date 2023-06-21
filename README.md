This is just a small script which takes a list of applications as command line
arguments, and sets any running Icon Task Lists on the Budgie Panel to show those
apps.

While it is best to specify the exact desktop file

e.g.

`./set-tasklist firefox.desktop nemo.desktop org.gnome.gedit.desktop`

you can specify the app name and it will make its best guess (usually accurate but at the mercy of Gio.DesktopAppInfo.Search)

e.g.

`./set-tasklist firefox nemo gedit "Budgie Desktop Settings"`

Then after logout/login, the apps should appear on Icon Task List.

The main use case for this was so that I could make a script to automate restoring
Budgie Panel applet preferences after reinstalling or resetting the Budgie Panel,
instead of having to manually add / remove desired Icon Task List apps every time.
