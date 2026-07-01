# Proto 15-Hour Clock

A simple Python terminal clock that displays the current time using a custom **15-hour AM/PM clock** instead of the standard 24-hour format.

## How It Works

* Converts a standard 24-hour day into a **30-hour clock**.
* Each custom hour lasts **48 standard minutes**.
* Displays the time in `HH:MM:SS AM/PM` format.
* Updates every second in the terminal.

### Example

```text
proto Clock → 08:25:41 AM
```

## Requirements

* Python 3
* Makefile

## Run

```bash
make run
```

Press **Ctrl +C** to stop the clock.