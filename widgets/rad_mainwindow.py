#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkRAD - tkinter Rapid Application Development library

    (c) 2013+ Raphaël SEBAN <motus@laposte.net>

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public
    License along with this program.

    If not, see: http://www.gnu.org/licenses/
"""



# lib imports

import traceback

import tkinter as TK

from tkinter import messagebox as MB

from . import rad_widget_base as RW

from . import rad_statusbar as SB

from ..xml import rad_xml_menu as XM

from ..core import tools



class RADMainWindow (RW.RADWidgetBase, TK.Tk):
    r"""
        Lightweight MainWindow class for people not using tkinter

        XML widget building on a mainframe;

        supports all RADWidgetBase app-wide services by default;

        supports on-board self.statusbar widget by default;

        supports on-board self.mainframe widget container by default;

        supports on-board RADXMLMenu self.topmenu by default;

        supports main window states 'maximized', 'minimized', 'normal'

        and 'hidden' in gettings and settings;

        implements connected slots for event signals "PendingTaskOn"

        and "PendingTaskOff";

        implements connected slot for confirmation dialog before really

        quitting application;

        will pop up a tkinter messagebox with last traceback on raised

        exceptions during inits;

        will also report entire traceback in stderr on raised

        exceptions during inits;
    """



    def __init__ (self, **kw):
        r"""
            class constructor - main inits

            no return value (void);
        """

        # super inits

        try:

            TK.Tk.__init__(self)

            RW.RADWidgetBase.__init__(self, tk_owner = None, **kw)

            self._init__main(**kw)

            self.init_widget(**kw)

            self.statusbar.notify(_("All inits done. OK."))

        except:

            MB.showerror(

                _("Caught exception"),

                _("An exception has occurred:\n\n{msg}")

                .format(msg = traceback.format_exc(limit = 1))
            )

            raise

            exit(1)

        # end try

    # end def



    def _init__main (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # main inits

        self._init_wm_protocols(**kw)

        self._init_members(**kw)

        self._init_options(**kw)

        self._init_geometry(**kw)

        self._init_title(**kw)

        self._init_mainframe(**kw)

        self._init_statusbar(**kw)

        self._init_topmenu(**kw)

        self._init_layout(**kw)

        self._init_events(**kw)

    # end def



    def _init_events (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # bind events

        self.bind("<Configure>", self.slot_root_changed)

        self.events.connect_dict(
            {
                "quit": self.slot_quit_app,

                "Quit": self.slot_quit_app,

                "quitapp": self.slot_quit_app,

                "QuitApp": self.slot_quit_app,

                "PendingTaskOn": self.slot_pending_task_on,

                "PendingTaskOff": self.slot_pending_task_off,
            }
        )

    # end def



    def _init_geometry (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # make main window resizable

        self.resizable(

            **kw.get("resizable", dict(width = True, height = True))
        )

        self.minsize(

            **kw.get("minsize", dict(width = 100, height = 100))
        )

        # main window geometry inits

        # caution: this is useful even while maximized               /!\

        self.geometry(

            tools.choose_str(

                kw.get("geometry"),

                self.options["geometry"].get("mainwindow"),

                "100x100",
            )
        )

        # maximize main window?

        self.set_window_state(

            tools.choose_str(

                kw.get("window_state"),

                self.options["geometry"].get("mainwindow_state"),

                "normal",
            )
        )

    # end def



    def _init_layout (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # layout inits

        self.rowconfigure(0, weight = 1)

        self.rowconfigure(1, weight = 0)

        self.columnconfigure(0, weight = 1)

    # end def



    def _init_mainframe (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # widget inits   ---   automagic gridding /!\

        _frame = TK.Label(

            self,

            text = _("Put here your own Frame() widget.")
        )

        self.mainframe = kw.get("mainframe", _frame)

        self.tk_owner = self.mainframe

        self.tk_children = self.mainframe.winfo_children

        self.mainframe.quit_app = self.slot_quit_app

    # end def



    def _init_members (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # member inits

        self.STATE = {

            "hidden": self.hide,

            "minimized": self.minimize,

            "maximized": self.maximize,

            "normal": self.show,
        }

        self.__pending_task = False

    # end def



    def _init_options (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # rc options default sections inits

        self.options.set_sections("geometry", "gui", "topmenu")

        # set some default values

        self.options.set_defaults(

            **kw.get(

                "rc_defaults",

                dict(

                    maximized = "0",

                    mainwindow = "640x480+20+20",

                    mainwindow_state = "normal",
                )
            )
        )

        # load options

        self.options.load()

    # end def



    def _init_statusbar (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # widget inits

        self.statusbar = kw.get("statusbar", SB.RADStatusBar(self))

    # end def



    def _init_title (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # main window title inits

        _app_title = None

        if hasattr(self.app, "APP") and tools.is_pdict(self.app.APP):

            _app_title = self.app.APP.get("title")

        # end if

        self.title(

            tools.choose_str(

                kw.get("title"),

                _app_title,

                _("Main Window"),

                "Main Window",
            )
        )

    # end def



    def _init_topmenu (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # widget inits

        self.topmenu = kw.get("topmenu", XM.RADXMLMenu(self))

        if isinstance(self.topmenu, XM.RADXMLMenu):

            self.topmenu.set_xml_filename(

                kw.get("topmenu_xml_filename", "topmenu")
            )

        # end if

    # end def



    def _init_wm_protocols (self, **kw):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # capture window manager's events handling

        self.protocol("WM_DELETE_WINDOW", self.slot_quit_app)

    # end def



    def _set_state (self, state):
        r"""
            protected method def;

            this could be overridden in subclass;

            no return value (void);
        """

        # param inits

        state = str(state).lower()

        # param controls - unsupported

        if state not in self.STATE:

            raise ValueError(

                _("main window's state should be one of {slist}.")

                .format(slist = str(tuple(self.STATE.keys())))
            )

            # reset value

            state = "normal"

        # end if

        # member inits

        self.__window_state = state

        # update rc options

        self.options["geometry"]["mainwindow_state"] = str(state)

    # end def



    def get_pending_task (self):
        r"""
            returns current "pending task" flag value;
        """

        return self.__pending_task

    # end def



    def get_window_state (self):
        r"""
            returns this main window state i.e. one of 'minimized',

            'maximized', 'normal' or 'hidden' string of chars;
        """

        return self.__window_state

    # end def



    def hide (self, *args, **kw):
        r"""
            hides this main window;

            no return value (void);
        """

        self.withdraw()

        self._set_state("hidden")

    # end def



    @property
    def mainframe (self):
        """
            @property handler for the mainframe widget container;

            developers may set their own widget building

            into a TK.Frame widget container and then set mainframe

            to that container e.g. self.mainframe = TK.Frame(self);

            RADMainWindow already comes with a preloaded widget

            for example giving;

            this can be overridden in subclasses by redefining

            self._init_mainframe() protected virtual method;
        """

        return self.__mainframe_widget

    # end def



    @mainframe.setter
    def mainframe (self, widget):

        if self.cast_widget(widget):

            self.__mainframe_widget = widget

            widget.grid(row = 0, column = 0, **self.GRID_OPTIONS)

        # end if

    # end def



    @mainframe.deleter
    def mainframe (self):

        del self.__mainframe_widget

    # end def



    def maximize (self, *args, **kw):
        r"""
            maximizes this main window;

            no return value (void);
        """

        self.deiconify()

        self.attributes("-zoomed", "1")

        self._set_state("maximized")

        # Tk() main window has some buggy behaviour sometimes        /!\

        self.update()

    # end def



    def minimize (self, *args, **kw):
        r"""
            minimizes (iconifies) this main window;

            no return value (void);
        """

        self.iconify()

        self._set_state("minimized")

    # end def



    def run (self):
        r"""
            enters tkinter events main loop;

            no return value (void);
        """

        self.mainloop()

    # end def



    def set_window_state (self, state):
        r"""
            sets this main window state i.e. one of 'minimized',

            'maximized', 'normal' or 'hidden' string of chars;

            sets also *REAL* window state along value;

            no return value (void);
        """

        # param inits

        state = str(state).lower()

        # get appropriate method call

        _method = self.STATE.get(state)

        if callable(_method):

            _method()

        else:

            raise ValueError(

                _("unsupported window state '{w_state}'.")

                .format(w_state = state)
            )

        # end if

    # end def



    def show (self, *args, **kw):
        r"""
            shows (deiconifies) this main window;

            no return value (void);
        """

        self.deiconify()

        self._set_state("normal")

    # end def



    def slot_pending_task_off (self, *args, **kw):
        r"""
            slot method for event signal "PendingTaskOff";

            no return value (void);
        """

        self.__pending_task = False

        self.statusbar.notify(_("An important task has finished."))

    # end def



    def slot_pending_task_on (self, *args, **kw):
        r"""
            slot method for event signal "PendingTaskOn";

            no return value (void);
        """

        self.__pending_task = True

        self.statusbar.notify(_("An important task has started."))

    # end def



    def slot_quit_app (self, *args, **kw):
        """
            slot method before quitting app definitely;

            asks for confirmation in dialog before acting;

            this should be overridden in subclass in order to

            meet your own needs;

            no return value (void);
        """

        if self.get_pending_task():

            MB.showwarning(

                _("Pending operation"),

                _(
                    "Some very important task is pending by now. "

                    "Please wait for completion and then retry."
                )
            )

        elif MB.askokcancel(

            _("Quit app?"),

            _("Are you sure you want to quit this application?")
        ):

            self.options.save()

            self.quit()

        # end if

    # end def



    def slot_root_changed (self, tk_event = None, *args, **kw):
        r"""
            slot method for tkinter event "<Configure>";

            manages special non-tkinter case of 'maximized' window

            state and updates rc config options on-the-fly;

            no return value (void);
        """

        # /!\ avoid useless calls from child widgets /!\

        if not isinstance(tk_event.widget, self.__class__):

            return

        # end if

        # inits

        _maximized = int(self.attributes("-zoomed"))

        if _maximized:

            self._set_state("maximized")

        else:

            self._set_state("normal")

            self.options["geometry"]\
                ["mainwindow"] = str(self.geometry())

        # end if

    # end def



    @property
    def statusbar (self):
        r"""
            @property handler for internal statusbar widget;

            developers may replace this widget with any other tkinter

            subclassed tk.Widget() object of their own;

            will raise TypeError if widget is not a tkinter

            subclassed tk.Widget() object;

            RADMainWindow already comes with a preloaded widget;

            this can be overridden in subclasses by redefining

            self._init_statusbar() protected virtual method;
        """

        return self.__statusbar_widget

    # end def



    @statusbar.setter
    def statusbar (self, widget):

        if self.cast_widget(widget):

            self.__statusbar_widget = widget

            widget.grid(row = 1, column = 0, **self.GRID_OPTIONS)

        # end if

    # end def



    @statusbar.deleter
    def statusbar (self):

        del self.__statusbar_widget

    # end def



    @property
    def topmenu (self):
        r"""
            @property handler for internal top menu object;

            developers may replace this object with any other tkinter

            subclassed tk.Menu() object of their own;

            will raise TypeError if object is not a tkinter subclassed

            tk.Menu() object or at least a tkRAD.xml.RADXMLMenu()

            derived object;

            RADMainWindow already comes with a preloaded top menu;

            this can be overridden in subclasses by redefining

            self._init_topmenu() protected virtual method;
        """

        return self.__menu_widget

    # end def



    @topmenu.setter
    def topmenu (self, widget):

        if isinstance(widget, (TK.Menu, XM.RADXMLMenu)):

            self.__menu_widget = widget

        else:

            raise TypeError(

                _(
                    "top menu must be of type tkinter.Menu "

                    "or at least of type tkRAD.xml.RADXMLMenu."
                )
            )

        # end if

    # end def



    @topmenu.deleter
    def topmenu (self):

        del self.__menu_widget

    # end def


# end class RADMainWindow
