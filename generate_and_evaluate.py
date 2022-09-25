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
N = 10000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time()-time_start))

# load and validate rules
# массивы для поиска взаимоислючающих
mass_fact_and = []  # массив правил из части and
mass_fact_not = []  # массив правил из части not

mass_then = []

itog = []  # итоговая база знаний
index_not_one_rang = []  # индексы словарей где ранг != 1

ranges = [None] * len(rules)
facts = set(facts)
rang = 1

for i, rule in enumerate(rules):  # для правил ранга 1
	counter = 0
	condition = rule["if"].keys()
	if condition == "or":
		for ind, fact in enumerate(rule["if"]["or"], start=1):
			if fact in facts:
				counter += 1
			if counter != 0:
				mass_then.append(rule["then"])
				ranges[i] = rang
				itog.append(rule["then"])
				continue
			if counter != ind:
				index_not_one_rang.append(i)
				continue

	if condition == "and":
		for ind, fact in enumerate(rule["if"]["and"], start=1):
			if fact in facts:
				counter += 1
			if counter != ind:
				index_not_one_rang.append(i)
				continue
		if counter == len(rule["if"]["and"]):
			mass_then.append(rule["then"])
			ranges[i] = rule
			itog.append(rule["then"])

	if condition == "not":
		for ind, fact in enumerate(rule["if"]["not"], start=1):
			if fact in facts:
				counter += 1
			if counter != ind:
				index_not_one_rang.append(i)
				continue
		if counter == len(rule["if"]["or"]):
			mass_then.append(rule["then"])
			ranges[i] = rule
			itog.append(rule["then"])
rang += 1
if len(mass_then) != len(rules):  # для правил ранга больше 1
	for i in index_not_one_rang:
		rule = rules[i]
		counter = 0
		condition = rule["if"].keys()
		if condition == "or":
			for ind, fact in enumerate(rule["if"]["or"], start=1):
				if fact in facts:
					counter += 1
				elif fact in mass_then:
					counter += 1
				if counter != ind:
					index_not_one_rang.append(i)
					continue
			if counter == len(rule["if"]["or"]):
				mass_then.append(rule["then"])
				ranges[i] = rang
				itog.append(rule["then"])
				index_not_one_rang.remove(i)

		if condition == "and":
			for ind, fact in enumerate(rule["if"]["and"], start=1):
				if fact in facts:
					counter += 1
				elif fact in mass_then:
					counter += 1
				if counter != ind:
					index_not_one_rang.append(i)
					continue
			if counter == len(rule["if"]["and"]):
				mass_then.append(rule["then"])
				ranges[i] = rule
				itog.append(rule["then"])
				index_not_one_rang.remove(i)

		if condition == "not":
			for ind, fact in enumerate(rule["if"]["not"], start=1):
				if fact in facts:
					counter += 1
				elif fact in mass_then:
					counter += 1
				if counter != ind:
					index_not_one_rang.append(i)
					continue
			if counter == 0:
				mass_then.append(rule["then"])
				ranges[i] = rule
				itog.append(rule["then"])
				index_not_one_rang.remove(i)
	rang += 1
print("validate rules in %f seconds" % (time()-time_start))
# check facts vs rules
time_start = time()

for rule in rules:
	fact_and = rule['if'].get('and')
	if fact_and is not None:
		counter = 0
		for fact in fact_and:
			if fact in facts:
				counter += 1
			else:
				break
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
				break
		if counter == 0:
			itog.append(rule['then'])

print(itog)
print("%d facts validated vs %d rules in %f seconds" % (M, N, time()-time_start))
