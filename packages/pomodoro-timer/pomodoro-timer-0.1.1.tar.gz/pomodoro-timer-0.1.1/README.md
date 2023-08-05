# Pomodoro-Timer - A pomodoro timer for my needs with audio and visual cues informing you when to start / stop working.

A pomodoro timer using [ncurses](https://www.gnu.org/software/ncurses/ncurses-intro.html) for terminal display and [zenity](https://en.wikipedia.org/wiki/Zenity) to open small notification windows on Linux.
Start, stop, resume sessions and get notified by sound or notification window when your work/break block starts.
You can also define and use your own sessions with a small session text format.

![Pomodoro-Timer Demo](examples/pomodoro_timer.gif)

## Getting Started

### Prerequisites
You need `python3` and also `pip` to install simpleaudio.

`pip install simpleaudio`

### Installing

1. Clone or download the repo.

`git clone git@github.com:Laeri/pomodoro-timer.git`

2. Copy the file into your path.

`sudo cp ./pomodoro-timer/pomodoro-timer /usr/bin/`


## Usage
1. Start the application with `pomodoro-timer`.
2. Type `help` and press enter to show all available commands.
3. Run `list`  to show all available sessions.
4. Run  `start <name>` or `start <session_number>` to start a specific session.
   (Replace <name> or <session_number> with the corresponding name or number)

### Session Description 
You can change the provided default sessions and also define your own sessions
by writing a session description file and reading it in. All session files are
stored in '~/.config/pomodoro-timer'. 
Example of a session:
```
session 'Default Long Session' 'This is the description for the default long session'
# this is a comment
# repeat the two grouped block statements three times
3x
block Work 25m
block Break 5m is_break

# then do a normal work block and a longer break
block Work 25m
block 'Long Break' 20m is_break
```

This would create a session where we repeat 25 minutes of work, followed by a 5 minute break three times.
Then we would work again 25 minutes and take a longer break of 20 minutes as recommended.
'is_break' to specify breaks is in this case optional. We can omit it and every second block will
be labelled as a break automatically.

1. Describe the session
`session <name> <session_description>`
2. Optional: The session can auto restart if it is finished (the first block will run
again after finishing the session).
auto_restart
3. Define each work / break block separately. The <time> can be any string in the format 'xh ym zs' where x are the hours, y minutes and z seconds.
`block <block_name> <time>`
4. If you do not provide an 'is_break' declaration at the end, the sessions will be labeled
'work', 'break' consecutively.
`block <block_name> <time> is_break`
5. You can also provide a 'multiplier' on a line before consecutive block specification lines.
   This will mean that we repeat the following lines (no empty lines between) x times:`
```4x
block work
block break
```
This would repeat two blocks (work and break) four times.

Checkout the configuration folder:
~/.config/pomodoro-timer


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file
for details.
Two .wav audio files were used which do have the Attribution 3.0 License.
The sources are specified in the 'sounds' folder.
