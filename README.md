# Bürgeramt appointment experiment

Checks Berlin.de for free Anmeldung appointments every X minutes, then analyses the results.

Later, I built a [Python version that serves the results via websockets](https://github.com/nicbou/burgeramt-appointments-websockets). It powers my [Bürgeramt appointment finder](https://allaboutberlin.com/appointments).

## How to use

Run `get-page.sh` periodically. Turn the resulting pages into machine-readable data with `results-parser.py`.

...or save yourself the trouble and use `results.csv` or `results.json`.

* [Experiment results](https://nicolasbouliane.com/blog/berlin-buergeramt-experiment)
* [How to find a Bürgeramt appointment in Berlin](https://allaboutberlin.com/guides/berlin-burgeramt-appointment)
* [How to register your address in Berlin](https://allaboutberlin.com/guides/anmeldung-in-english-berlin)

## Licence

This project is released in the public domain. Do whatever you want. I take no responsibility for it.

## Mentions

This project was mentioned by [RBB24](https://www.rbb24.de/panorama/beitrag/2021/10/termin-buergeramt-berlin-software-tipp.html) and [Tagesspiegel](https://checkpoint.tagesspiegel.de/newsletter/58AQnV8j65ZFm10qj3Cii6).
