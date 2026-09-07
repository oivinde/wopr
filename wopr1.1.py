#!/usr/bin/env python3
"""
WOPR TERMINAL
=============
A self-running, looping, character-based homage to the WOPR / IMSAI 8080
terminal from the 1983 film WarGames. Pure ANSI + Python standard library,
no dependencies.

Run:    python3 wopr.py
Quit:   Ctrl+C
Slower: python3 wopr.py --slow
Faster: python3 wopr.py --fast
Once:   python3 wopr.py --once     (play the sequence one time, then exit)

Everything below is an original re-creation for nostalgia's sake: the boot
banter, the game list, the map, and the countdown are all generated at
runtime, not a transcript of the film.
"""

import sys
import time
import random
import shutil
import signal
import argparse

# ---------------------------------------------------------------------------
# Look & feel
# ---------------------------------------------------------------------------

FG_COLOR = "\033[1;38;2;138;210;255m"  # bold #8AD2FF
RESET = "\033[0m"  # full reset -- only for restoring the terminal on exit
CLEAR = "\033[2J\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
BLINK = "\033[5m"
UNBLINK = "\033[25m"  # turns blink back off WITHOUT touching color/bold

SPEED = 1.0  # multiplier, smaller = faster. Adjusted by CLI flags.


def cols_rows():
    sz = shutil.get_terminal_size(fallback=(80, 24))
    return sz.columns, sz.lines


def cleanup(*_):
    sys.stdout.write(SHOW_CURSOR + RESET + "\n")
    sys.stdout.flush()
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def sleep(seconds):
    time.sleep(max(0.0, seconds * SPEED))


def type_out(text, cps=42, jitter=0.35, end="\n", pause_after=0.0, center=False):
    """Typewriter-print a line of text, character by character."""
    cols, _ = cols_rows()
    if center:
        pad = max(0, (cols - len(text)) // 2)
        sys.stdout.write(" " * pad)
    base_delay = 1.0 / cps
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        sleep(base_delay * (1 + random.uniform(-jitter, jitter)))
    sys.stdout.write(end)
    sys.stdout.flush()
    if pause_after:
        sleep(pause_after)


def type_block(lines, cps=42, line_pause=0.15, pause_after=0.0, center=False):
    for line in lines:
        type_out(line, cps=cps, center=center)
        sleep(line_pause)
    if pause_after:
        sleep(pause_after)


def blank(n=1):
    for _ in range(n):
        print()


def clear():
    sys.stdout.write(CLEAR)
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Scene 1: boot / dial-up / login
# ---------------------------------------------------------------------------

def scene_boot():
    clear()
    type_block([
        "IMSAI 8080 SYSTEM",
        "64K RAM SYSTEM  38911 BASIC BYTES FREE",
        "",
    ], cps=60, line_pause=0.25)
    sleep(0.4)

    type_out("AUTO-DIAL ENGAGED. SCANNING EXCHANGE...", cps=45, pause_after=0.3)
    number = "".join(random.choice("0123456789") for _ in range(7))
    number = f"{number[:3]}-{number[3:]}"
    type_out(f"DIALING {number} ...", cps=45)
    sleep(0.6)
    for _ in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(0.4)
    print()
    type_out("CONNECT 300", cps=45, pause_after=0.6)
    blank()
    type_out("PACKET NET SESSION ESTABLISHED.", cps=45, pause_after=0.6)


def scene_login():
    clear()
    logins = ["JOSHUA", "FALKEN", "PENCIL", "LINGUINI", "PROTEUS", "BACKGAMMON"]
    type_out("SEARCHING FOR BACKDOOR ACCOUNT...", cps=45, pause_after=0.3)
    for _ in range(6):
        guess = random.choice(logins)
        type_out(f"TRYING LOGIN: {guess}{'.' * random.randint(2,5)} DENIED", cps=90)
        sleep(0.12)
    sleep(0.3)
    type_out("TRYING LOGIN: JOSHUA... ACCEPTED", cps=45, pause_after=0.8)
    blank()
    type_out("GREETINGS PROFESSOR FALKEN.", cps=38, pause_after=1.0)
    blank()
    type_out("HELLO.", cps=38, pause_after=0.6)
    type_out("HOW ARE YOU FEELING TODAY?", cps=38, pause_after=1.0)
    blank()
    type_out("I'M FINE. HOW ARE YOU?", cps=38, pause_after=0.8)
    blank()
    type_out("EXCELLENT. IT'S BEEN A LONG TIME. CAN YOU EXPLAIN THE REMOVAL OF", cps=38)
    type_out("YOUR USER ACCOUNT ON 6/23/73?", cps=38, pause_after=1.0)
    blank()
    type_out("PEOPLE SOMETIMES MAKE MISTAKES.", cps=38, pause_after=0.8)
    blank()
    type_out("YES THEY DO.", cps=38, pause_after=1.0)
    blank()
    type_out("SHALL WE PLAY A GAME?", cps=38, pause_after=1.2)


# ---------------------------------------------------------------------------
# Scene 2: game list
# ---------------------------------------------------------------------------

GAMES = [
    "FALKEN'S MAZE",
    "BLACK JACK",
    "GIN RUMMY",
    "HEARTS",
    "BRIDGE",
    "CHECKERS",
    "CHESS",
    "POKER",
    "FIGHTER COMBAT",
    "GUERRILLA ENGAGEMENT",
    "DESERT WARFARE",
    "AIR-TO-GROUND ACTIONS",
    "THEATERWIDE TACTICAL WARFARE",
    "THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE",
    "GLOBAL THERMONUCLEAR WAR",
]


def scene_menu():
    clear()
    type_out("LIST GAMES", cps=45, pause_after=0.5)
    blank()
    for g in GAMES:
        type_out(g, cps=90)
        sleep(0.05)
    blank(2)
    type_out("LET'S PLAY GLOBAL THERMONUCLEAR WAR.", cps=38, pause_after=1.0)
    blank()
    type_out("WOULDN'T YOU PREFER A GOOD GAME OF CHESS?", cps=38, pause_after=1.0)
    blank()
    type_out("LATER. LET'S PLAY GLOBAL THERMONUCLEAR WAR.", cps=38, pause_after=1.0)
    blank()
    type_out("FINE.", cps=38, pause_after=0.8)


# ---------------------------------------------------------------------------
# Scene 3: Global Thermonuclear War -- tactical map + DEFCON countdown
#
# The two landmasses are hand-drawn ASCII art (not a hand-rolled coastline
# attempt), placed side by side. A short target legend is appended below
# each drawing's country label -- it never touches the artwork itself --
# and a trajectory line is drawn between the two blocks in the gap when a
# launch is "in flight". Every frame is rebuilt from a fixed-height
# background, so the redraw logic (draw_frame) always moves the cursor up
# exactly as many lines as it writes -- no drift, no duplication.
# ---------------------------------------------------------------------------

USA_ART = [
    " ,------~~v,                ",
    " |'         Ż\\   ,__/Ż||    ",
    "/             \\,/     /     ",
    "|                    /      ",
    "\\                   |       ",
    " \\                 /        ",
    "  ^Ż~_            /         ",
    "      '~~,  ,Ż~Ż\\ \\         ",
    "          \\/     \\/         ",
    "                            ",
    "                            ",
    "   UNITED STATES            ",
]

USSR_ART = [
    "              _--^\\",
    "            _/    /,_",
    "   ,,   ,,/^      Ż  vŻv-__",
    "   |'~^Ż                   Ż\\",
    " _/                     _  /^",
    "/                   ,~~^/|ŻŻ",
    "|          __,,  v__\\   \\/",
    " ^~       /    ~Ż  //",
    "   \\~,  ,/         Ż",
    "      ~~",
    "",
    "      SOVIET UNION",
]

# Just flavor text for the "SRC -> TGT" status line -- not shown on the
# map itself, since the map is the artwork alone with no legend beneath it.
USSR_SITE_NAMES = ["PLESETSK", "SITE-4", "SITE-7"]
TARGET_ORDER = ["LAS VEGAS", "SEATTLE"]  # fixed target order, per spec


def _pad_block(block, width, height):
    block = list(block) + [""] * (height - len(block))
    return [line.ljust(width) for line in block]


# USA is the left block, Soviet Union the right block.
BLOCK_H = max(len(USSR_ART), len(USA_ART))
LEFT_W = max(len(l) for l in USA_ART)
RIGHT_W = max(len(l) for l in USSR_ART)
GAP_W = 8
CANVAS_W = LEFT_W + GAP_W + RIGHT_W


def build_map_background():
    left = _pad_block(USA_ART, LEFT_W, BLOCK_H)
    right = _pad_block(USSR_ART, RIGHT_W, BLOCK_H)
    return [l + " " * GAP_W + r for l, r in zip(left, right)]


# Fixed points ON the artwork itself (row, local column within each block)
# that missile trajectories fly between -- not the text legend below. The
# launch always starts from the same silo point inside the Soviet outline
# (now the right-hand block); each named US target has its own point
# inside the American outline (the left-hand block) so the missile
# visibly crosses both landmasses on its way there.
LAUNCH_POINT_LOCAL = (3, 22)  # inside USSR_ART, offset by LEFT_W + GAP_W below
TARGET_POINTS = {
    "LAS VEGAS": (7, 4),   # inside USA_ART, global column == local column
    "SEATTLE": (2, 4),
}


def _line_points(r0, c0, r1, c1, steps):
    """`steps` interpolated (row, col) points from (r0, c0) to (r1, c1),
    used to animate a trajectory growing across the whole canvas."""
    pts = []
    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 1.0
        pts.append((round(r0 + (r1 - r0) * t), round(c0 + (c1 - c0) * t)))
    return pts


def draw_frame(lines, first=False):
    if not first:
        sys.stdout.write(f"\033[{len(lines)}A")
    for line in lines:
        sys.stdout.write("\033[2K" + line + "\n")
    sys.stdout.flush()


def type_prompt_input(prompt, answer, cps=22, pause_after=0.5):
    """Print a prompt, then simulate the (autonomous) 'user' typing an
    answer into it character by character, followed by Enter. There's no
    real keyboard involved -- this is a self-running demo -- but visually
    it reads exactly like someone answering WOPR's questions."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    sleep(0.3)
    base_delay = 1.0 / cps
    for ch in answer:
        sys.stdout.write(ch)
        sys.stdout.flush()
        sleep(base_delay * (1 + random.uniform(-0.3, 0.3)))
    sys.stdout.write("\n")
    sys.stdout.flush()
    if pause_after:
        sleep(pause_after)


def _new_launch(targets, index):
    """Start a launch at a fixed target, cycling through `targets` in the
    order given (index increases with every completed launch)."""
    tgt_name = targets[index % len(targets)]
    src_name = random.choice(USSR_SITE_NAMES)
    launch_row, launch_col_local = LAUNCH_POINT_LOCAL
    r0, c0 = launch_row, LEFT_W + GAP_W + launch_col_local
    r1, c1 = TARGET_POINTS[tgt_name]
    steps = max(abs(r1 - r0), abs(c1 - c0)) + 1
    return {
        "src": src_name, "tgt": tgt_name,
        "r0": r0, "c0": c0, "r1": r1, "c1": c1, "steps": steps,
        "progress": 0, "impacted": False, "hold": 0,
    }


def _render_map_frame(background, launch, defcon):
    grid = [list(line) for line in background]
    pts = _line_points(launch["r0"], launch["c0"], launch["r1"], launch["c1"], launch["steps"])
    head_char = "<" if launch["c1"] < launch["c0"] else ">"
    n_visible = max(1, round(launch["steps"] * min(1.0, launch["progress"] / launch["steps"])))
    for i, (row, col) in enumerate(pts[:n_visible]):
        if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
            is_head = (i == n_visible - 1) and not launch["impacted"]
            grid[row][col] = head_char if is_head else "."
    if launch["impacted"]:
        r1, c1 = launch["r1"], launch["c1"]
        if 0 <= r1 < len(grid) and 0 <= c1 < len(grid[r1]):
            grid[r1][c1] = BLINK + "X" + UNBLINK

    lines = ["".join(row) for row in grid]
    lines.append("")
    label = f"DEFCON: {defcon}"
    if defcon <= 2:
        label = BLINK + label + UNBLINK
    lines.append(label)
    lines.append("-" * CANVAS_W)
    status = "IMPACT" if launch["impacted"] else "TRACKING"
    lines.append(f"  {launch['src']} -> {launch['tgt']}: {status}")
    return lines


def scene_targeting():
    """Draw the world map, have WOPR offer a side to play, 'select' the
    Soviet Union, and enter a couple of US cities as primary targets --
    all auto-typed since this is a self-running demo. Returns the map
    background and the chosen target list so scene_attack can launch at
    exactly those cities."""
    clear()
    type_out("GLOBAL THERMONUCLEAR WAR", cps=38, pause_after=0.8)
    blank()

    background = build_map_background()
    for line in background:
        print(line)
    blank()
    sleep(0.6)

    type_out("SELECT YOUR SIDE:", cps=45, pause_after=0.3)
    type_out("  1. UNITED STATES", cps=90)
    type_out("  2. SOVIET UNION", cps=90, pause_after=0.5)
    type_prompt_input("SELECTION: ", "2", cps=14, pause_after=0.5)
    type_out("YOU HAVE SELECTED: SOVIET UNION", cps=45, pause_after=1.0)
    blank()

    targets = TARGET_ORDER
    type_out(f"ENTER PRIMARY TARGETS ({len(targets)} CITIES):", cps=42, pause_after=0.4)
    for name in targets:
        type_prompt_input("TARGET> ", name, cps=22, pause_after=0.5)
    blank()
    type_out("TARGET LIST CONFIRMED:", cps=42, pause_after=0.3)
    for name in targets:
        type_out(f"  - {name}", cps=90)
        sleep(0.1)
    blank()
    type_out("INITIATING GLOBAL THERMONUCLEAR WAR SIMULATION...", cps=42, pause_after=1.4)

    return background, targets


def scene_attack(background, targets, duration=10.0):
    clear()
    type_out("LAUNCH TARGETS: UNION OF SOVIET SOCIALIST REPUBLICS -> UNITED STATES",
              cps=40, pause_after=0.6)
    blank()

    defcon = 5
    launch_index = 0
    launch = _new_launch(targets, launch_index)

    draw_frame(_render_map_frame(background, launch, defcon), first=True)
    sleep(0.6)

    start = time.time()
    while time.time() - start < duration * SPEED:
        time.sleep(0.15 * SPEED)
        if not launch["impacted"]:
            launch["progress"] += 1
            if launch["progress"] >= launch["steps"]:
                launch["impacted"] = True
                if defcon > 1:
                    defcon -= 1
        else:
            launch["hold"] += 1
            if launch["hold"] >= 4:
                launch_index += 1
                launch = _new_launch(targets, launch_index)
        draw_frame(_render_map_frame(background, launch, defcon))
    blank()


def scene_finale():
    type_out("GREETINGS PROFESSOR FALKEN.", cps=38, pause_after=1.0)
    blank()
    type_out("A STRANGE GAME.", cps=32, pause_after=0.8)
    type_out("THE ONLY WINNING MOVE IS NOT TO PLAY.", cps=32, pause_after=1.4)
    blank()
    type_out("HOW ABOUT A NICE GAME OF CHESS?", cps=32, pause_after=2.0)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_once():
    scene_boot()
    scene_login()
    scene_menu()
    background, targets = scene_targeting()
    scene_attack(background, targets, duration=10.0)
    scene_finale()


def main():
    global SPEED
    parser = argparse.ArgumentParser(description="WOPR terminal demo (WarGames homage)")
    parser.add_argument("--once", action="store_true", help="play the sequence once and exit")
    parser.add_argument("--slow", action="store_true", help="slower typing / pacing")
    parser.add_argument("--fast", action="store_true", help="faster typing / pacing")
    args = parser.parse_args()

    if args.slow:
        SPEED = 1.6
    elif args.fast:
        SPEED = 0.5

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.write(FG_COLOR)
    sys.stdout.flush()
    try:
        if args.once:
            run_once()
        else:
            while True:
                run_once()
                sleep(2.5)
    except KeyboardInterrupt:
        pass
    except Exception:
        # Restore the terminal before letting the real error surface --
        # a bug here should never leave the user's shell stuck colored
        # and cursor-less.
        sys.stdout.write(SHOW_CURSOR + RESET + "\n")
        sys.stdout.flush()
        raise
    cleanup()


if __name__ == "__main__":
    main()
