from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import Container, Grid, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Label, Placeholder, Sparkline


class QuicklookTextualPlugin(VerticalGroup):
    """Quicklook plugin for Textual."""

    def compose(self) -> ComposeResult:
        yield Sparkline([0, 1, 2, 3, 4, 5], id="quicklookcpu")
        yield Sparkline([0, 1, 2, 3, 4, 5], id="quicklookmem")
        yield Sparkline([0, 1, 2, 3, 4, 5], id="quicklookload")


class CpuTextualPlugin(Container):
    """Quicklook plugin for Textual."""

    start_time = reactive(monotonic)
    time = reactive(0.0)

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("CPU", id="cputotal", classes="title"),
            Label("69%", id="cputotalvalue", classes="value ok"),
            Label("idle", id="cpuidel"),
            Label("69%", id="cpuidelvalue", classes="value careful"),
            Label("ctx_sw", id="cpuctxsw"),
            Label("69%", id="cpuctxswvalue", classes="value warning"),
            Label("user", id="cpuuser"),
            Label("69%", id="cpuuservalue", classes="value critical"),
            Label("irq", id="cpuirq"),
            Label("69%", id="cpuirqvalue", classes="value"),
            Label("inter", id="cpuinter"),
            Label("69%", id="cpuintervalue", classes="value"),
            Label("system", id="cpusystem"),
            Label("69%", id="cpusystemvalue", classes="value"),
            Label("nice", id="cpunice"),
            Label("69%", id="cpunicevalue", classes="value"),
            Label("swe_int", id="cpuswint"),
            Label("69%", id="cpuswintvalue", classes="value"),
            Label("iowait", id="cpuiowait"),
            Label("69%", id="cpuiowaitvalue", classes="value"),
            Label("steel", id="cpusteel"),
            Label("69%", id="cpusteelvalue", classes="value"),
            Label("guest", id="cpuguest"),
            Label("69%", id="cpuguestvalue", classes="value"),
            id="cpucontent",
        )

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.set_interval(1 / 60, self.update_time)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        # self.cputotalvalue.update(str(self.time))
        self.query_one("#cputotalvalue").update(str(self.time))


class GlancesTuiApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "main.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self):
        super().__init__()
        self.plugins = {
            "quicklook": None,
            "cpu": None,
            "gpu": None,
            "mem": None,
            "memswap": None,
            "load": None,
            "network": None,
            "diskio": None,
        }

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.plugins["quicklook"] = QuicklookTextualPlugin()
        self.plugins["cpu"] = CpuTextualPlugin()
        self.plugins["diskio"] = Placeholder(id="diskio")
        yield Header(id="header", show_clock=True)
        yield Container(
            Grid(
                self.plugins["quicklook"],
                self.plugins["cpu"],
                Placeholder(id="gpu", classes="remove"),
                Placeholder(id="mem"),
                Placeholder(id="memswap"),
                Placeholder(id="load"),
                id="top",
            ),
            Grid(
                VerticalScroll(
                    Placeholder(id="network"),
                    self.plugins["diskio"],
                    Placeholder(id="fs"),
                    Placeholder(id="sensors"),
                    id="sidebar",
                ),
                VerticalScroll(
                    Placeholder(id="vms"),
                    Placeholder(id="containers"),
                    Placeholder(id="processcount"),
                    Placeholder(id="processlist"),
                    id="process",
                ),
                id="middle",
            ),
            Grid(
                Placeholder(id="now"),
                Placeholder(id="alert"),
                id="bottom",
            ),
            id="data",
        )
        yield Footer(id="footer")

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # self.set_interval(1, self.update_data)
        self.title = "Glances"
        self.sub_title = "version X.Y.Z"

        self.plugins["diskio"].styles.height = 1

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = GlancesTuiApp()
    app.run()
