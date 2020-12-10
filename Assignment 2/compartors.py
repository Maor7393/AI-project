def max_adversarial_comparator(best_value_tup, new_state_tup):
	best_value = best_value_tup[0] - best_value_tup[1]
	new_value = new_state_tup[0] - new_state_tup[1]
	return best_value_tup if best_value > new_value else new_state_tup


def max_semi_cooperative_comparator(best_value_tup, new_state_tup):
	if best_value_tup[0] < new_state_tup[0]:
		return new_state_tup
	if best_value_tup[0] == new_state_tup[0]:
		if best_value_tup[1] < new_state_tup[1]:
			return new_state_tup
	return best_value_tup


def min_adversarial_comparator(best_value_tup, new_state_tup):
	best_value = best_value_tup[1] - best_value_tup[0]
	new_value = new_state_tup[1] - new_state_tup[0]
	return best_value_tup if best_value > new_value else new_state_tup


def min_semi_cooperative_comparator(best_value_tup, new_state_tup):
	if best_value_tup[1] < new_state_tup[1]:
		return new_state_tup
	if best_value_tup[1] == new_state_tup[1]:
		if best_value_tup[0] < new_state_tup[0]:
			return new_state_tup
	return best_value_tup


def fully_cooperative_comparator(best_value_tup, new_state_tup):
	best_value = best_value_tup[0] + best_value_tup[1]
	new_value = new_state_tup[0] + new_state_tup[1]
	return new_state_tup if best_value < new_value else best_value_tup

