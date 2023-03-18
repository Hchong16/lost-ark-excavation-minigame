# Lost Ark Excavation Minigame Tool
Automation tool to automate the excavation lifeskill minigame. 

This tool does **not** interfere with any game code or network packets. 

Instead, the tool takes region-bounded screenshots and perform image recognition on them to determine what actions to take.

Your mileage may vary.

# Setup
**This tool only works when Lost Ark is running on 1080p + Fullscreen.**

Pre-requisite is to have Python 3.11.0+ installed using the installation [here](https://www.python.org/downloads/).

Once completed, run the following commands in the terminal below:
1. Setup a python virtual environment by running : ```python -m venv venv```
2. Activate the virtual environment: ```./venv/Scripts/activate```
3. Install python dependencies: ```pip3 install -r requirements.txt```

You can now run the tool by running: ```python minigame.py```

To quit the tool, press the `=` key or `CTRL + C` in the terminal.

# WARNING
This is not endorsed by Smilegate or AGS. Usage of this tool isn't defined by Smilegate or AGS. No personal identifiable data is saved.
