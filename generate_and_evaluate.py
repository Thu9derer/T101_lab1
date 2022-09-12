from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

		log_oper = choice(log_oper_choice)  # not means and-not (neither)
		if n_max < 2:
			n_max = 2
		n_items = randint(2, n_max)
		items = []
		for i in range(0, n_items):
			items.append(randint(1, code_max))
		rule = {
				'if': {
					log_oper:	 items
				},
				'then': code_max+j
		}
		rules.append(rule)
	shuffle(rules)
	return rules


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

		log_oper = choice(log_oper_choice)  # not means and-not (neither)
		if n_max < 2:
			n_max = 2
		n_items = randint(2, n_max)
		items = []
		for i in range(0, n_items):
			items.append(i + j)
		rule = {
				'if': {
					log_oper: items
				},
				'then': i+j+1
				}
		rules.append(rule)
	shuffle(rules)
	return rules


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = generate_stairway_rules(code_max, n_max, n_generate-1, log_oper_choice)
	log_oper = choice(log_oper_choice)  # not means and-not (neither)
	if n_max < 2:
		n_max = 2
	n_items = randint(2, n_max)
	items = []
	for i in range(0, n_items):
		items.append(code_max-i)
	rule = {
			'if': {
				log_oper: items
			},
			'then': 0
			}
	rules.append(rule)
	shuffle(rules)
	return rules


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and","or","not"]):
	rules = []
	for j in range(0, n_generate):

		log_oper = choice(log_oper_choice)  # not means and-not (neither)
		if n_max < 2:
			n_max = 2
		n_items = randint(2, n_max)
		items = []
		for i in range(0, n_items):
			items.append(randint(1, code_max))
		rule = {
				'if':{
					log_oper: items
				},
				'then': randint(1, code_max)
				}
		rules.append(rule)
	shuffle(rules)
	return rules


def generate_seq_facts(M):
	facts = list(range(0, M))
	shuffle(facts)
	return facts


def generate_rand_facts(code_max, M):
	facts = []
	for i in range(0, M):
		facts.append(randint(0, code_max))
	return facts


# samples:
print(generate_simple_rules(100, 4, 10))
print(generate_random_rules(100, 4, 10))
print(generate_stairway_rules(100, 4, 10, ["or"]))
print(generate_ring_rules(100, 4, 10, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time()-time_start))
print(facts)

# load and validate rules
mass_fact_or = []
mass_fact_and = []
mass_fact_not = []
for rule in rules:
	rul_and = rule['if'].get('and')
	if rul_and is not None:
		if mass_fact_and.count(rul_and) != 0:
			rules.pop(mass_fact_and.index(rul_and))
			continue
		mass_fact_and.append(rul_and)

	rul_not = rule['if'].get('not')
	if rul_not is not None:
		if mass_fact_not.count(rul_not) != 0:

			rules.pop(mass_fact_not.index(rul_not))
			continue
		mass_fact_not.append(rul_not)

	rul_or = rule['if'].get('or')
	if rul_or is not None:
		if mass_fact_or.count(rul_or) != 0:
			rules.pop(mass_fact_or.index(rul_or))
			continue
		mass_fact_and.append(rul_or)


# check facts vs rules
time_start = time()
itog = []
for rule in rules:
	fact_and = rule['if'].get('and')
	if fact_and is not None:
		counter = 0
		for fact in fact_and:
			if fact in facts:
				counter += 1
		if counter == len(fact_and):
			itog.append(rule['then'])

	fact_or = rule['if'].get('or')
	if fact_or is not None:
		for fact in fact_or:
			if fact in facts:
				itog.append(rule['then'])
				break

	fact_not = rule['if'].get('not')
	if fact_not is not None:
		counter = 0
		for fact in fact_not:
			if fact in facts:
				counter += 1
		if counter == 0:
			itog.append(rule['then'])
print(itog)
print("%d facts validated vs %d rules in %f seconds" % (M, N, time()-time_start))
