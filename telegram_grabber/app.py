from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import Tk


class Application:
    def __init__(self) -> None:
        self._root = Tk()
        self._root.title("Telegram Chat/Channel History Downloader")

        self._setup_layout()

    def run(self) -> None:
        """Run application main loop."""
        self._root.mainloop()

    def download_history(self) -> None:
        """Download Telegram Chat/Channel history."""
        pass

    def _setup_layout(self) -> None:
        # API Keys
        Label(self._root, text="API ID:").grid(row=0, column=0)
        self.api_id_entry = Entry(self._root)
        self.api_id_entry.grid(row=0, column=1)
        Label(self._root, text="API Hash:").grid(row=1, column=0)
        self.api_hash_entry = Entry(self._root)
        self.api_hash_entry.grid(row=1, column=1)

        # Phone Number
        Label(self._root, text="Phone Number:").grid(row=2, column=0)
        self.phone_number_entry = Entry(self._root)
        self.phone_number_entry.grid(row=2, column=1)

        # Entity
        Label(self._root, text="Chat/Channel ID:").grid(row=3, column=0)
        self.entity_entry = Entry(self._root)
        self.entity_entry.grid(row=3, column=1)

        # Dates
        Label(self._root, text="Start Date:").grid(row=4, column=0)
        self.start_date = Entry(self._root)
        self.start_date.grid(row=4, column=1)
        Label(self._root, text="End Date:").grid(row=5, column=0)
        self.end_date = Entry(self._root)
        self.end_date.grid(row=5, column=1)

        # Download Button
        self.download_button = Button(self._root, text="Download History", command=self.download_history)
        self.download_button.grid(row=6, column=1)


def run() -> None:
    gui = Application()
    gui.run()


if __name__ == "__main__":
    run()
