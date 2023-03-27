# Lost Ark Excavation Minigame Tool
Automation tool to automate the excavation lifeskill minigame. 

This tool does **not** interfere with any game code or network packets. 

Instead, the tool takes region-bounded screenshots and perform image recognition on them to determine what actions to take.

Your mileage may vary.

# User Setup
**This tool only works when Lost Ark is running on 1080p + Fullscreen + 80% HUD size. You must configure offset values to work with your PC.**

Before starting the exectuable, four values may need to be changed in the `config.ini`:

`starting_delay_seconds` is the time before the program starts tapping the targets. Typically, longer delay will allow the program to "settle" and hit targets more accurately.

When we locate the arrow, the program will find the starting position of the arrow on the x-axis. The `arrow_middle_offset` will adjust the defined middle point of the arrow.
```
              ^                   ^
             ^ ^      ---->      ^ ^ 
            ^---^               ^---^
            |                     |  
           (x)              (x + offset)
```

When we locate the three targets, the program will locate the middle of each target and use the `target_range_left_offset` and `target_range_right_offset` to define the starting and ending range for each target. If the middle of the arrow (`arrow_middle_offset`) is within any of these ranges, the program will press spacebar. 

**It is prefered that these target offets should be the same. If the program is biased towards one side over the other the arrow offset should be adjusted and not the range**.

```
        target 1     target 2        target 3
     ___________________________________________
    |    |   |        |   |           |   |     |
    |____|___|________|_ _|___________|___|_____|

           |            |               |
        <----->      <----->         <----->
        |  |  |      |  |  |         |  |  |  
       +l  m  +r    +l  m  +r       +l  m  +r
       
Legend:
l = left offset
r = right offset
```

These offsets are to account for delays between the program and the game. A 0 offset means there are no latency at all. If the program hits the spacebar too late, shifting the arrow middle (increasing `arrow_middle_offset`) and/or expanding the target ranges will alleviate the latency.

To run the program, simply use the `minigame.exe`. To quit the tool, press the `=` key or `CTRL + C` in the terminal.

Restarting the program is required for changes made in the configuration file to take effect.

# Development Setup
Pre-requisite is to have Python 3.11.0+ installed using the installation [here](https://www.python.org/downloads/).

Once completed, run the following commands in the terminal below:
1. Setup a python virtual environment by running : ```python -m venv venv```
2. Activate the virtual environment: ```./venv/Scripts/activate```
3. Install python dependencies: ```pip3 install -r requirements.txt```

You can now run the tool by running: ```python minigame.py```

If you choose to run based on the executable, use the `minigame.exe` file, which will immediately start up the program.

However, any changes made outside of the configuration file will require the user to regenerate the `.exe` by running:
```pyinstaller --onefile minigame.py```. Once generated, move the one file from the `dist` directory to the root.

To quit the tool, press the `=` key or `CTRL + C` in the terminal.

# Result
A minigame shovel with 2 difficulty reduction has yielded the following results:  
Of 80 out of 85 games, all 3 targets were hit. For the remaining 5, a minimum of 2 targets were hit.

Users may need to configure offset values on the target ranges and the middle point on the game arrow to reach similar results.

# WARNING
This is not endorsed by Smilegate or AGS. Usage of this tool isn't defined by Smilegate or AGS. No personal identifiable data is saved.
