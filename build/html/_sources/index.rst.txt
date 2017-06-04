.. Turbot documentation master file, created by
   sphinx-quickstart on Sun Jun  4 23:05:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Turbot's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
============

Turbot is a small python bot done for school that streams music from youtube in a specific discord voice channel.
It relies on a music queue which is filled up by users.

Dependencies : `Discord.py <http://discordpy.readthedocs.io/en/latest/api.html>`_ , `youtube-dl <https://rg3.github.io/youtube-dl/>`_

Basic usage
===========

Help is accessed with the !help command. By default, the invoker is '!' but can be configured by the user in the conf.json file.
When !join is invoked, the bot will join the user's current voice channel.

!queue ***search string*** will add a song in the queue. The first youtube result encountered will be used. The queue can be displayed with !viewqueue and deleted with !emptyqueue.

I won't insult you by explaining the !start, !stop, !pause and !resume commands.

!skip is actually broken and will get fixed pretty soon. But, eh, deadlines.


Documentation
==================

.. automodule:: turbot
    :members:
	
.. autoclass:: Song
    :members:
	:functions: