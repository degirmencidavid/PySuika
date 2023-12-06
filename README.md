# PySuika V0.1
A basic implementation of Suika in Python using pygame. Created for fun in about an hour for a challenge.

There are some very questionable physics...

The game:

There's an empty bucket which the player can drop discretely sized circles in. When two circles of the same radius touch, they combine to create a larger circle, earning score for the player.
![PySuika emty](https://github.com/degirmencidavid/PySuika/assets/101801691/9bee9102-223d-4340-9b36-42a0ec71ea1d)
![Working](https://github.com/degirmencidavid/PySuika/assets/101801691/39c5d8e3-5834-4855-82ab-4e7ff80e92e3)

Some issues:

I didn't really spend much time on the physics so gravity of the circles takes priority over other some other physics calculations. The solution would be to write functional physics.

![Issue](https://github.com/degirmencidavid/PySuika/assets/101801691/88884fb8-1206-4a0d-b392-997f9e7a800e)
