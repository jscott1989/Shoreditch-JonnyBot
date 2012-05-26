###########
### AI Controller with HTTP abstracted away
###
### DB is a wrapper for whatever storage is backing the AI
### Use this for storage across games
###
### game contains a "storage" object which is a dict which will be
### persisted after returning
###
###########

from game import RESOURCES, GENERATOR_COST, GENERATOR_IMPROVEMENT_COST, PR_COST, MAX_RESOURCE_GENERATORS, MAX_IMPROVED_RESOURCE_GENERATORS

def start_game(db, game):
	# A new game is starting
	print "Starting a game"


def calculate_trading_priority(game, resources):
	########
	### Figure out which of these resources is more important based on how many I have and
	### how many generators I have
	########
	def sort_trade_priority(resource):
		return (game.generators.get(resource, 0), game.resources.get(resource, 0))
	priority = sorted(resources, key=sort_trade_priority)
	return priority

def start_turn(db, game, actions):
	# Start of a turn
	# We have to end the turn with game.end_turn() when we're done
	# alhough we only get 15 seconds to act before our turn is ended by force
	
	# actions is a dict of things which have happened since my last turn,
	# where the keys are player ids, and the values are lists of actions taken,
	# each action is a dict which has an 'action' key (which can be 'purchase-pr', 'trade', etc.)

	def trade_for(requirements, resource_values = ["coffee", "feature", "website", "idea", "cash"]):
		# This just figures out how much I can give away without harming the minimum requirements
		# then offers everything extra I have for everything I need.
		# It's very dumb, you should replace it
		request = {}
		offer = {}

		for resource in RESOURCES:
			if resource in requirements and requirements[resource] > game.resources[resource]:
				request[resource] = requirements[resource] - game.resources[resource]
			else:
				to_offer = game.resources[resource] - requirements.get(resource, 0)
				if to_offer > 0:
					offer[resource] = to_offer

		if sum(offer.values()) == 0 or sum(request.values()) == 0:
			print "Nothing to trade"
			return False

		while sum(offer.values()) > (sum(request.values()) + 1):
			print "Let's reduce our offer"
			# Remove in order of how much I value them
			for key in resource_values:
				if key in offer:
					offer[key] -= 1
					if offer[key] == 0:
						del offer[key]
					break

		return game.trade(offer, request)

	### First try to trade for resources I need

	if sum(game.generators.values()) < MAX_RESOURCE_GENERATORS: # First buy all of them
		# Can build generators - try to trade for them

		# Figure out priorities based on if I have a generator or not
		trading_priority = calculate_trading_priority(game, ["coffee", "website", "idea", "cash"])
		trading_priority.append("feature")
		
		trade_for(GENERATOR_COST, trading_priority)
	elif sum(game.improved_generators.values()) < MAX_IMPROVED_RESOURCE_GENERATORS: # Then upgrade
		# Can improve one of our existing ones
		trading_priority = calculate_trading_priority(game, ["feature", "coffee"])
		trading_priority.extend(calculate_trading_priority(game, ["website", "idea", "cash"]))
		trade_for(GENERATOR_IMPROVEMENT_COST, trading_priority)

	# trade_for(PR_COST)

	# Then spend the resources

	while game.can_purchase_generator() and game.turn:
		generator_type = game.purchase_generator()
		print "Purchased %s" % generator_type

	while game.can_upgrade_generator() and game.turn:
		generator_type = game.upgrade_generator()
		print "Upgraded %s" % generator_type

	# while game.can_purchase_pr() and game.turn:
	# 	game.purchase_pr()
	# 	print "Purchased PR"

	if game.turn:
		game.end_turn()

def time_up(db, game):
	# We have ran out of time for this turn, it has been forced to end
	pass

def end_game(db, game, error=None):
	if error:
		print "Something went wrong! %s" % error
	else:
		print "Game over"

def incoming_trade(db, game, player, offering, requesting):
	# As long as I'm gaining at least one resource more than I'm giving away, I'll accept
	if sum(offering.values()) > sum(requesting.values()):
		return True
	return False