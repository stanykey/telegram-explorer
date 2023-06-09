# Telegram Explorer

This is an educational project. It is based on my friend's nephew's lab task.

The current status can be described as `almost beta`:
- the main window isn't resizable
- no `save\export` button (easy to add, but it's time to sleep :))
- concurrent-related issues must be here due it was the experiment: UI + asyncio

But, the goals were passed, and it was fun: I remembered the time when I was a student and did programming in Borland C++ Builder


## Task description
- need to obtain the history of Telegram chat for a certain period
- the preferred language is Python


### My educational aims
- [x] investigate how to work with [Telegram API](https://core.telegram.org/api)
    - [x] look at popular Python packages for work with it
- [x] implement cli-tool (POC) via the selected library
- [x] implement the gui-application
    - [x] learn how to build gui-apps with the [tkinter](https://docs.python.org/3/library/tkinter.html) library
    - [x] adapt to be able to work with asyncio
    - [x] enhance ui (need to try to prettify)
        - [x] themes
        - [x] show a progress bar on async operations
        - [ ] make the main window resizable


#### References
- [pyrogram](https://docs.pyrogram.org): modern, elegant and asynchronous framework for Telegram API
- [click](https://palletsprojects.com/p/click/): Python package for creating beautiful command line interfaces
- [tkinter tutorial](https://www.pythonguis.com/tkinter-tutorial):  building simple GUI applications with Tk & Python
- [tkinter grid detailed](https://www.pythontutorial.net/tkinter/tkinter-grid): introduction to the Tkinter grid geometry manager
- [ttkwidgets's documentation](https://ttkwidgets.readthedocs.io/en/latest/index.html)
- [yet one tkinter tutorial](https://effbot.org/tkinter-in-python-tkinter-tutorial)
