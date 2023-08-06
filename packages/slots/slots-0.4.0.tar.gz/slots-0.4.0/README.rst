slots
=====
*A multi-armed bandit library for Python*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

slots is intended to be a basic, very easy-to-use multi-armed bandit library for Python.

:Author: `Roy Keyes <https://roycoding.github.io>`_ - roy.coding@gmail


:License: MIT


Introduction
~~~~~~~~~~~~
slots is a Python library designed to allow the user to explore and use simple multi-armed bandit (MAB) strategies. The basic concept behind the multi-armed bandit problem is that you are faced with *n* choices (e.g. slot machines, medicines, or UI/UX designs), each of which results in a "win" with some unknown probability. Multi-armed bandit strategies are designed to let you quickly determine which choice will yield the highest result over time, while reducing the number of tests (or arm pulls) needed to make this determination. Typically, MAB strategies attempt to strike a balance between "exploration", testing different arms in order to find the best, and "exploitation", using the best known choice. There are many variation of this problem, see `here <https://en.wikipedia.org/wiki/Multi-armed_bandit>`_ for more background.

slots provides a hopefully simple API to allow you to explore, test, and use these strategies. See the `development site <https://github.com/roycoding/slots>`_ for usage and API details.
