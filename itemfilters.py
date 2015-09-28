###############################################
### COMP 598 : Project #1                   ###
### ---------------------					###
### Authors:                                ###
###  + Nicolas Angelard-Gontier - 260532513 ###
###  + Genevieve Fried - #########          ###
###  + Charlie Bloomfield - 260520615       ###
###############################################

#necessary attributes to consider an item as a valid story
storyAttributes = [
	'type',
	'id',
	'by',
	'title',
	'url',
	'score',
	'time',
	'descendants'
]

def stories(items):
	"""
	@param list of hacker-news items
	@return list of hacker-news valid stories

	Validity is determined by testing the item for containing a set of features.
	"""
	return [story for story in items if all(map(lambda attribute: attribute in story, storyAttributes))]