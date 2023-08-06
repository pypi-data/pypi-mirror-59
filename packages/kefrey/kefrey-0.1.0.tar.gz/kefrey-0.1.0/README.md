# Kefrey

*A tool to track system-wide keypress frequencies*

If a laptop key breaks, it's useful to be able to know which keys are
least used across all your tasks. This way, you can swap the least used
key for the one that broke. This script tracks this data with a keylogger
(don't worry, it only stores distribution data).


## Install

```bash
pip3 install --user kefrey
```

## Setup Tracking

```bash
kefrey-install
systemctl enable kefrey
systemctl start kefrey
```

Now, a file `~/.kefrey.json` will contain keypress distribution info,
tracked in the background, started at startup.
