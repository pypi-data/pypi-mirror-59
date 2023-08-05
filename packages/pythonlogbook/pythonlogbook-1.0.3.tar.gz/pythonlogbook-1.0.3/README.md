# Python Logbook
This program enables it's users to instantly make a logbook entry from the terminal. The program instantly creates folders that correspond to the date that each entry was published. Each file is named as date_time. If you want to see all logs at once, you can do such with combineLogs.py, which will concatenate all logs into one long logbook.

## Getting Started
Installing logbook is super simple on debian-based operating systems.
```
sudo add-apt-repository ppa:lukew3/logbook
sudo apt update
sudo apt install logbook
```

## Alternate install method
The python logbook was designed to be as convenient as possible. If you do it right, you should be able to simply run `logbook` into the terminal and create a log entry.

### Setting up directory
As of right now, the only way to change the folder where the logs are stored is by editing the variable originalPath so that line 11 of logbook.py says `originalPath = r"folderLocation"`.

Once you set this up, you should be able to run the program through the terminal by running `python logbook.py` while in the folder that the file is in.

### Setting up alias
To set up a custom command for running logbook.py from your home directory you have to edit the bash_aliases file. To do this, run `nano .bash_aliases` in your terminal. Once you are in the editor you must write the alias command to allow you to type in logbook anytime you want to write a log. Type this in the first line: `alias logbook="cd <spaceholder>; python logbook.py"`, and place the directions to the folder that contains logbook.py where the <spaceholder> is. Once you do this, press ctrl+x, y, enter. If all is successful, you should be able to create a new log entry by simply typing `logbook` into terminal whenever you want.

## Built with
* Python

## Author

* **Luke Weiler** - [lukew3](https://github.com/lukew3)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
