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
mass_fact_and = [None] * len(rules)  # массив правил из части and
mass_fact_not = [None] * len(rules)  # массив правил из части not

mass_then = []

itog = []  # итоговая база знаний
index_not_one_rang = []  # индексы словарей где ранг != 1

facts = set(facts)


for i, rule in enumerate(rules):  # для правил ранга 1
	counter = 0
	condition = list(rule["if"].keys())[0]
	if condition == "or":
		for ind, fact in enumerate(rule["if"]["or"], start=1):
			if fact in facts:
				counter += 1
			if counter != 0:
				mass_then.append(rule["then"])
				itog.append(rule["then"])
				break
		if counter == 0:
			index_not_one_rang.append(i)
			continue

	if condition == "and":
		fact_and = rule["if"]["and"]
		if fact_and in mass_fact_not:  # обработка взаимоисключений and not
			index = mass_fact_not.index(fact_and)
			if rule["then"] == rules[mass_fact_not[index][-1]]["then"]:
				rules.pop(i)
				rules.pop(mass_fact_not[index][-1])
				mass_then.pop(mass_fact_not[index][-1])
				continue
		for ind, fact in enumerate(fact_and, start=1):
			if fact in facts:
				counter += 1
			if counter != ind:
				index_not_one_rang.append(i)
				break
		if counter == len(fact_and):
			mass_fact_and.append(fact_and.append(i))
			mass_then.append(rule["then"])
			itog.append(rule["then"])
			continue
	if condition == "not":
		fact_not = rule["if"]["not"]
		if fact_not in mass_fact_and:  # обработка взаимоисключений and not
			index = mass_fact_and.index(fact_not)
			if rule["then"] == rules[mass_fact_and[index][-1]]["then"]:
				rules.pop(i)
				rules.pop(mass_fact_and[index][-1])
				mass_then.pop(mass_fact_and[index][-1])
				continue
		for ind, fact in enumerate(rule["if"]["not"], start=1):
			if fact in facts:
				counter += 1
			if counter != ind:
				index_not_one_rang.append(i)
				break
		if counter == 0:
			mass_then.append(rule["then"])
			itog.append(rule["then"])

while len(index_not_one_rang) != 0:  # для правил ранга больше 1
	for i in index_not_one_rang:
		rule = rules[i]
		condition = rule["if"].keys()
		if condition == "or":
			counter = 0
			for ind, fact in enumerate(rule["if"]["or"], start=1):
				if fact in facts:
					counter += 1
					mass_then.append(rule["then"])
					itog.append(rule["then"])
					index_not_one_rang.remove(i)
					break
				elif fact in mass_then:
					counter += 1
					mass_then.append(rule["then"])
					itog.append(rule["then"])
					index_not_one_rang.remove(i)
					break
			if counter == 0:
				index_not_one_rang.append(i)
				continue

		if condition == "and":
			counter = 0
			fact_and = rule["if"]["and"]
			if fact_and in mass_fact_not:  # обработка взаимоисключений and not
				index = mass_fact_not.index(fact_and)
				if rule["then"] == rules[mass_fact_not[index][-1]]["then"]:
					rules.pop(i)
					rules.pop(mass_fact_not[index][-1])
					mass_then.pop(mass_fact_not[index][-1])
					continue
			for ind, fact in enumerate(rule["if"]["and"], start=1):
				if fact in facts:
					counter += 1
				elif fact in mass_then:
					counter += 1
				if counter != ind:
					index_not_one_rang.append(i)
					break
			if counter == len(rule["if"]["and"]):
				mass_then.append(rule["then"])
				itog.append(rule["then"])
				index_not_one_rang.remove(i)

		if condition == "not":
			counter = 0
			fact_not = rule["if"]["not"]
			if fact_not in mass_fact_and:  # обработка взаимоисключений and not
				index = mass_fact_and.index(fact_not)
				if rule["then"] == rules[mass_fact_and[index][-1]]["then"]:
					rules.pop(i)
					rules.pop(mass_fact_and[index][-1])
					mass_then.pop(mass_fact_and[index][-1])
					continue
			for ind, fact in enumerate(rule["if"]["not"], start=1):
				if fact in facts:
					counter += 1
				elif fact in mass_then:
					counter += 1
				if counter != ind:
					index_not_one_rang.append(i)
					break
			if counter == 0:
				mass_then.append(rule["then"])
				itog.append(rule["then"])
				index_not_one_rang.remove(i)

print("validate rules in %f seconds" % (time()-time_start))
# check facts vs rules
time_start = time()

print(itog)
print("%d facts validated vs %d rules in %f seconds" % (M, N, time()-time_start))
