# Qtile config for ArchCosta

import os
import re
import socket
import subprocess
from libqtile import _, bar, layout, widget
from libqtile.config import Click, Drag, DropDown, Group, Key, KeyChord, Match, ScratchPad, Screen
from libqtile.core.manager import Qtile
from libqtile.lazy import lazy

# Mod keys
mod = "mod4"
alt = "mod1"

# Terminal
terminal = "alacritty"
browser = "firefox"
file_manager = "thunar"

# Colors (Dracula)
colors = {
    "bg": "#282a36",
    "fg": "#f8f8f2",
    "fg_alt": "#6272a4",
    "hi": "#6272a4",
    "ac": "#bd93f9",
    "gr": "#50fa7b",
    "rd": "#ff5555",
    "or": "#ffb86c",
    "yl": "#f1fa8c",
    "pu": "#ff79c6",
    "cy": "#8be9fd",
}

# Font
font = "JetBrains Mono Nerd Font"
fontsize = 12

# Key bindings
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to next window"),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Split/Join windows
    Key([mod], "s", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides"),
    Key([mod, "shift"], "s", lazy.layout.flip(), desc="Flip layout"),

    # Window sizing
    Key([mod], "i", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "m", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset window sizes"),

    # Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),

    # Floating
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="Toggle floating"),

    # Kill window
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    # Restart/Quit
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Logout"),

    # Applications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show run"), desc="Run dialog"),

    # System
    Key([mod, "shift"], "x", lazy.spawn("i3lock -i /usr/share/backgrounds/archlinux/archlinux-logo.png -t"), desc="Lock screen"),
    Key([], "Print", lazy.spawn("scrot '%Y-%m-%d_$wx$h.png' -e 'mv $f ~/Pictures/'"), desc="Screenshot"),
    Key([mod], "Print", lazy.spawn("scrot -u '%Y-%m-%d_$wx$h.png' -e 'mv $f ~/Pictures/'"), desc="Screenshot window"),
]

# Mouse bindings
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button1", lazy.window.bring_to_front()),
]

# Workspaces
groups = [
    Group("1", label="一"),
    Group("2", label="二"),
    Group("3", label="三"),
    Group("4", label="四"),
    Group("5", label="五"),
    Group("6", label="六"),
    Group("7", label="七"),
    Group("8", label="八"),
    Group("9", label="九"),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name), desc="Move window to group {}".format(i.name)),
    ])

# ScratchPad
groups.append(
    ScratchPad("scratchpad", [
        DropDown("term", "alacritty", opacity=0.8),
        DropDown("fm", "thunar", opacity=0.8),
    ])
)

keys.extend([
    Key([mod], "z", lazy.group["scratchpad"].dropdown_toggle("term")),
    Key([mod], "x", lazy.group["scratchpad"].dropdown_toggle("fm")),
])

# Layouts
layouts = [
    layout.Columns(
        border_focus=colors["ac"],
        border_normal=colors["bg"],
        border_width=2,
        margin=4,
        num_columns=2,
        split=False,
    ),
    layout.Max(),
    layout.Tile(
        border_focus=colors["ac"],
        border_normal=colors["bg"],
        border_width=2,
        margin=4,
        master_match=None,
        ratio=0.5,
        ratio_increment=0.05,
        shift_windows=False,
    ),
    layout.MonadTall(
        border_focus=colors["ac"],
        border_normal=colors["bg"],
        border_width=2,
        change_size=20,
        margin=8,
        ratio=0.5,
    ),
    layout.Floating(
        border_focus=colors["pu"],
        border_normal=colors["bg"],
        border_width=2,
    ),
]

# Widgets
widget_defaults = dict(
    font=font,
    fontsize=fontsize,
    padding=8,
    foreground=colors["fg"],
    background=colors["bg"],
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    return [
        widget.GroupBox(
            active=colors["fg"],
            borderwidth=0,
            center_aligned=True,
            disable_drag=True,
            fontsize=18,
            foreground=colors["fg"],
            hide_unused=False,
            highlight_method="text",
            inactive=colors["fg_alt"],
            margin=4,
            margin_x=4,
            margin_y=4,
            other_current_screen_border=colors["ac"],
            other_screen_border=colors["bg"],
            padding=4,
            padding_x=4,
            padding_y=4,
            printafari=False,
            rounded=True,
            this_current_screen_border=colors["ac"],
            this_screen_border=colors["bg"],
            urgent_alert_method="text",
            urgent_border=colors["rd"],
            urgent_text=colors["rd"],
            use_mouse_wheel=True,
        ),
        widget.Prompt(),
        widget.WindowName(),
        widget.Chord(
            chords_colors={
                "launch": (colors["rd"], colors["bg"]),
                "resize": (colors["gr"], colors["bg"]),
            },
            name_format="{ctx_group_id}:{ctx_name}",
            prompt="{name}:{group}",
        ),
        widget.CPU(
            format=" {percent}%",
            mouse_callbacks={},
            update_interval=1.0,
        ),
        widget.Memory(
            format=" {MemUsed: .0f}{mm}",
            measure_mem="M",
            mouse_callbacks={},
            update_interval=1.0,
        ),
        widget.DF(
            format="{uf}{m} ({r:.0f}%)",
            mouse_callbacks={},
            partition="/",
            visible_on_warn=True,
        ),
        widget.Temperature(
            cpu_format="{tzname} {temp:.0f}°C",
            crit_temp=80,
            format="{temp:.0f}°C",
            mouse_callbacks={},
            tag_sensor_core="cpu Package",
            tag_sensor_tdie="Tdie",
            threshold=70,
            update_interval=1.0,
        ),
        widget.Volume(
            fmt=" vol {}",
            get_volume_command=None,
            mixer_app="pulseaudio-ctl",
            mouse_callbacks={},
            theme_path=None,
            volume_app="pulseaudio-ctl",
            volume_down_command=None,
            volume_up_command=None,
        ),
        widget.Battery(
            charge_char="⚡",
            discharge_char="🔋",
            empty_char="✕",
            format="{char} {percent:2.0%}",
            full_char="100%",
            notify_discharged=False,
            notification_timeout=5,
            show_short_text=False,
            unknown_char="?",
            update_interval=5,
        ),
        widget.Clock(
            format="%Y-%m-%d %H:%M",
            timezone=None,
            update_interval=1.0,
        ),
        widget.Systray(
            icon_size=16,
            padding=4,
            screen=None,
        ),
        widget.QuickExit(
            countdown_format="{}",
            default_text="⏻",
            display_format="{seconds}",
            duration=5,
            fontsize=16,
            padding=8,
            timer_interval=1.0,
        ),
    ]

def init_screens():
    return [
        Screen(
            bottom=bar.Bar(
                widgets=init_widgets_list(),
                size=26,
                background=colors["bg"],
                border_width=[2, 0, 0, 0],
                border_color=colors["bg"],
                margin=[4, 8, 0, 8],
            ),
        ),
    ]

screens = init_screens()

# Drag floating windows
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# Auto-start
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])
