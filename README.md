# Custom Boot Page

Custom Boot Page is a terminal-based startup screen, the kind of thing meant to run automatically when a shell opens or a machine boots, combining a randomized ASCII art splash with a live system status readout. It leans more toward personalization and terminal aesthetics than toward firmware or browser tooling, everything here runs as a plain Python script targeting a console.

On launch, it picks one of several large ASCII art pieces at random and prints it in color using `colorama`, followed by a stylized "OMEN" header. From there it pulls together a small dashboard: current CPU and RAM utilization and free disk space via `psutil`, the current time, live weather for a configured city via the OpenWeatherMap API, and a random inspirational quote pulled from a public quotes API, all rendered with a lightweight typewriter text effect for a bit of terminal flair.

A background thread listens for a single keypress (`s`) using `msvcrt`, letting you skip the typewriter animation and print instantly if you don't want to wait, a small but practical touch for something that's meant to run every time you open a terminal.

Because it depends on `msvcrt`, this script is Windows-specific as written. Porting it to Linux or macOS would mean swapping the skip-listener implementation for something built on `termios`/`tty` or a cross-platform library like `keyboard`, since `msvcrt` has no equivalent on those platforms.

Features:
- Randomized ASCII art splash screen on every run
- Live system stats: CPU usage, RAM usage, free disk space
- Live weather lookup via the OpenWeatherMap API
- Random daily quote via the ZenQuotes API, with a graceful fallback if the request fails
- Typewriter-style text rendering with a keypress-based skip function
- Color output via `colorama`

Tech:
- Python 3
- `psutil`
- `requests`
- `colorama`
- `msvcrt` (standard library, Windows only)

Configuration: set your city and OpenWeatherMap API key in the `CITY` and `API_KEY` constants near the top of the script. Treat the API key as a secret; if this repo is public, move it to an environment variable or a local, gitignored config file rather than hardcoding it.

Usage: install dependencies with `pip install psutil requests colorama`, then run the file. For it to act as an actual boot/startup page, point your terminal profile or a startup script at it, for example a shortcut in the Windows Startup folder or a custom PowerShell profile hook.

Note: the API key in the current source is a real, live key. It should be rotated and removed from version control history before this repo is made public.
