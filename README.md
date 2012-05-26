Shoreditch JonnyBot
=====================

Based on Shoreditch-SampleAI - This was written by someone involved in the competition so will not be entered. It was just created to ensure that it is possible to consistently beat SampleAI :)

Changes from SampleAI:

* Don't offer more than +1 on any trade, as the SampleAI will always accept this (though this would probably be a weakness against other bots)
* Ignore PR as it's not needed to beat SampleAI (though again, against other bots that +2 customers could be useful)
* Separate building into 2 phases, 1: build as many generators as possible (to get varied resources), 2: upgrade them. Set trading priorities based on which phase we're in.
* Adjust priorities based on how many resources I currently have and what generator types I have.
* Only accept trades when they offer something I need without taking something I need (for the current production phase).

Feel free to take some "inspiration" from the changes I've made. But please don't fork this as a base for your AI. Please use SampleAI for that.