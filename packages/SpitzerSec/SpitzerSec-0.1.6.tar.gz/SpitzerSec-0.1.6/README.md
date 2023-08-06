# Spitzer

Spitzer is a *Day Zero Scanner* for a pentest. The idea of the scanner is to chart the network and find all open ports with possible outdated services. Spitzer does **not** exploit anything, it merely scans for possible exploits and errors. This tool was developed during an internship at [HackDefense](https://hackdefense.com/) in 2019.

## Getting Started

Spitzer was developed on [Kali 2019.3](https://www.kali.org/downloads/) with [Python 3.7.3](https://www.python.org/downloads/). Spitzer makes use of a lot of pre-installed tools on kali, so I recommend to only use this on kali. If you want to use another Linux-dist, [here is a list of the tools](https://github.com/riqky/spitzer/wiki/tools).

## Installing

Clone the project and install it:

```bash
git clone https://github.com/Riqky/Spitzer
cd Spitzer
./install.sh
```

and then start the script to get the interactive shell:

```bash
spitzer
```

## Usage

From the interactive shell you can run a range of commands. Here is the output of the help command:

```spitzer
> help

Documented commands (type help <topic>):
========================================
EOF  exit  exploit  help  options  quit  run  scan  set  shell
```

- **run**

this runs both the exploit and the scan command.

- **exit**

Exits the application gracefully

- **exploit**

Runs all the exploit modules in `data.json`. These modules do not actually exploit, I'm just bad at naming. You can easily add an module to this command, see: [Adding Module](#adding-module)

- **help**

displays the help for all commands. To get more information about the command, use `help <command>`. `?` can also be used

- **options**

Shows all the options for running the scans and exploits.

- **quit**

Same as `exit`

- **scan**

Runs the scan modules. The module first executes `masscan` multiple 3 times (amount can be set in `info`). Then it runs `nmap` with the options `-sV -nP` and the given options from `info`.

- **set**

Is used the set the options from `info`. Usage `set <key> <value>`

- **shell**

Can be used to run shell commands in the working directory with `shell <command>` or `!<command>`. <!--**WARNING!** This runs the command completely unsanitized in the shell. Therefor this command could be used to gain [privilege escalation](https://en.wikipedia.org/wiki/Privilege_escalation) on a non-Kali system.-->

- **EOF**

Quits the pogram. This is executed when you press `CRTL+D`.

## Adding Module

The 'exploit' modules are loaded in at run-time, meaning that you can easily add another exploit to the script.
First you need to create a new python file with an unique name in the folder `Spitzer/exploiters`. This script must contain the following method:

```python
def exploit(host, nmap, port):
```

Where `host` host is the hostname or IP-address of the target, `nmap` is a dict with the results of the nmap-scan (see [python-nmap](https://pypi.org/project/python-nmap/) for more information) and `port` is the port where the running service is found.

Within the function you can run test the service for vulnerabilities. You can use the `result` script to export the results to a file after testing.

Then, you'll need to add the script to `data.json`. This file contains all the ports and corresponding modules. In `data.json` add a new entry in `ports`:

```json
"<service-name>":["<module-name>", "<nmap-script>"]
```

Example:

```json
"http":["websploit"]
"ftp":["ftp", "ftp-anon"]
```

## Used tools

The follwing tools are currently used by Spitzer, non-Kali tools are installed by `setup.sh`. The rest you'll need to install manualy if you want to use Spitzer outside of Kali.

- Nmap
- Masscan
- ftp
- smbmap
- searchsploit

Not in Kali, and thus installed by `setup.sh`:

- Gobuster
- securityheaders</span>.py <!--span is a weird trick to prevent them being hyperlinks-->
- aquatone
- testssl</span>.sh

## Acknowledgements

- HackDefense for giving me the room and help to create this script.
