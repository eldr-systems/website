---
title: What PSM actually negotiates, and why your battery estimate is wrong
date: 2026-09-18
summary: The T3412 and T3324 timers your device asks for are a request, not a setting. The network decides. Here is how to find out what you actually got.
description: NB-IoT and LTE-M devices request PSM timers; the network grants them. Firmware that logs the request rather than the grant produces battery estimates built on a number that was never true.
---

## The request is not the answer

A device asking for a 24-hour TAU period and a 2-second active timer will often be
granted something else entirely. The attach request carries the values your firmware
asked for. The accept carries what the network decided to give you.

Firmware that logs the request and not the accept produces a battery estimate built on
a number that was never true. Read the granted T3412 and T3324 back after attach, and
log those.

Operators differ, and the same operator differs by region and by roaming agreement. A
device that behaves on a domestic SIM can behave differently on the roaming SIM you
ship with.

## Where the current actually goes

On a device transmitting a small payload hourly, the transmit burst is rarely the
problem. It is brief, it is obvious, and it is the thing everyone measures first.

The recurring costs are usually elsewhere:

- The active timer window after each exchange, where the modem stays reachable doing nothing
- A wake-up path nobody measured — a sensor held in a higher power mode than intended
- A regulator that never reaches its own low-power state because something keeps a rail loaded
- Retries after a failed attach, which can cost more than a week of successful reporting

A power profiler across one full duty cycle settles this in an afternoon. A datasheet
calculation does not.

## What to measure before quoting a battery life

- One complete duty cycle, from wake through transmit to the next wake
- Current during the active window after the exchange, not only during transmit
- Sleep current with every peripheral in the state your firmware believes it is in
- The same measurement on a real network, not only against a base-station simulator

Numbers from a lab bench and numbers from a real operator's network differ. The
difference is usually in the timers, and it is usually in the direction that costs you
battery life rather than saves it.
