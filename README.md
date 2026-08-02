# Server Monitoring with ESP8266 & MQTT

A lightweight IoT monitoring project that collects real-time system metrics (CPU, memory, disk usage, and uptime) using Python and publishes them over MQTT. An ESP8266 running MicroPython subscribes to the data and displays the metrics on a 16×2 I2C LCD in real time.

## Running the Monitoring Service

Start the monitoring script in the background using `nohup`:

```bash
nohup python3 system.py > monitor.log 2>&1 &
```

### What this command does

* `nohup` – Keeps the program running even after you close the terminal.
* `python3 system.py` – Starts the monitoring service.
* `> monitor.log` – Redirects standard output to `monitor.log`.
* `2>&1` – Redirects error output to the same log file.
* `&` – Runs the process in the background.

### Check if the service is running

```bash
ps aux | grep system.py
```

or

```bash
pgrep -af system.py
```

### View the log

```bash
tail -f monitor.log
```

### Stop the service

```bash
pkill -f system.py
```

or

```bash
kill <PID>
```

Replace `<PID>` with the process ID returned by `ps` or `pgrep`.


