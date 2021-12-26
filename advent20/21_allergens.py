from collections import deque
from copy import deepcopy, copy
from heapq import heappush, heappop

from Util import from_file, test


class Rule:
    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return Rule(self.ingredients.copy(), self.allergens.copy())

    def __str__(self):
        return "%s (contains %s)" % (" ".join(self.ingredients), ", ".join(self.allergens))


class Ing:
    def __init__(self, name):
        self.__name = name
        self.__allergen = None
        self.__not_allergen = set()

    def name(self):
        return self.__name

    def allergen(self):
        return self.__allergen

    def possible(self, allergen):
        return allergen != self.__allergen and allergen not in self.__not_allergen

    def try_set_allergen(self, allergen):
        if allergen in self.__not_allergen:
            return False

        self.__allergen = allergen
        return True

    def try_add_not_allergen(self, not_allergen):
        if not_allergen is None:
            return True

        if not_allergen == self.__allergen:
            return False

        self.__not_allergen.add(not_allergen)
        return True

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        other = Ing(self.__name)
        other.__allergen = self.__allergen
        other.__not_allergen = self.__not_allergen.copy()

        return other

    def __str__(self):
        allergen_str = self.__allergen if self.__allergen else "???"
        # not_allergen_str = ", ".join(self.__not_allergen) if self.__not_allergen else "???"

        # return "%s: %s, not %s" % (self.__name, allergen_str, not_allergen_str)
        return "%s: %s" % (self.__name, allergen_str)

    def __hash__(self):
        return hash(self.name())

    def __eq__(self, other):
        return self.name() == other.name()


class State:
    def __init__(self, ing, other_ings, allergen, allergen_left, history=()):
        self.ing = ing
        self.other_ings = other_ings
        self.allergen = allergen
        self.history = history
        self.allergen_left = allergen_left

    def name(self):
        def ing_to_str(ing):
            return "%s-%s" % (ing.name(), ing.allergen())

        all = [ing_to_str(self.ing)]
        all.extend(map(ing_to_str, self.other_ings))

        return ", ".join(sorted(all))

    def __lt__(self, other):
        self_len = len(self.allergen_left)
        other_len = len(other.allergen_left)
        if self_len == other_len:
            return len(self.history) < len(other.history)

        return self_len < other_len


def parse_input(lines):
    rules = []
    all_ingredients = set()
    all_allergies = set()

    for line in lines:
        line = line.strip()

        ingredients, allergens = line.split(' (contains ')
        ingredients = ingredients.split(" ")
        allergens = allergens[:-1].split(", ")

        rules.append(Rule(set(ingredients), allergens))
        all_ingredients.update(map(Ing, ingredients))
        all_allergies.update(allergens)

    return rules, all_ingredients, all_allergies


def update_others(state, allergen):
    for other in state.other_ings:
        is_other_ok = other.try_add_not_allergen(allergen)

        if not is_other_ok:
            return False

    return True


def build_possible_allergens(ingredient, rules):
    allergens = { None }
    for rule in rules:
        if ingredient.name() not in rule.ingredients:
            continue

        for allergen in rule.allergens:
            if ingredient.possible(allergen):
                allergens.add(allergen)

    return allergens


def validate_rules(rules, ingredient, allergen):
    if allergen is None:
        return True

    for rule in rules:
        if allergen in rule.allergens:
            if ingredient.name() not in rule.ingredients:
                return False

    return True


def solve(rules, all_ingredients, all_allergies):
    all_ingredients = list(sorted(all_ingredients, key=lambda ing: ing.name()))
    queue = []
    all_allergies = list(all_allergies)

    for _ in range(len(all_ingredients) - len(all_allergies)):
        all_allergies.append(None)

    for allergen in build_possible_allergens(all_ingredients[0], rules):
        heappush(queue, State(copy(all_ingredients[0]), deepcopy(all_ingredients[1:]), allergen, copy(all_allergies)))

    while len(queue) > 0:
        state = heappop(queue)

        ingredient = state.ing
        allergen = state.allergen

        if not validate_rules(rules, ingredient, allergen):
            continue

        if not ingredient.try_set_allergen(allergen):
            continue

        if allergen not in state.allergen_left:
            continue

        next_allergen_left = copy(state.allergen_left)
        next_allergen_left.remove(allergen)

        next_history = state.history + (ingredient,)

        if len(state.other_ings) == 0:
            safe = list(map(lambda ing: ing.name(), filter(lambda ing: ing.allergen() is None, next_history)))

            # print_sorted(filter(lambda ing: ing.allergen() is not None, next_history))
            return count_occurances(safe, rules)

        next_allergens = build_possible_allergens(state.other_ings[0], rules)

        for allergen in next_allergens:
            next_state = State(copy(state.other_ings[0]), deepcopy(state.other_ings[1:]), allergen, next_allergen_left, next_history)

            heappush(queue, next_state)


def count_occurances(safe, rules):
    count = 0
    for safe_ing in safe:
        for rule in rules:
            if safe_ing in rule.ingredients:
                count += 1

    return count


def print_sorted(ingredients):
    print(",".join(map(lambda ing: ing.name(), sorted(ingredients, key=lambda ing: ing.allergen()))))


def run_lines(lines):
    rules, all_ingredients, all_allergies = parse_input(lines)
    return solve(rules, all_ingredients, all_allergies)


def run():
    return run_lines(from_file("inputs/21_allergens"))


if __name__ == '__main__':
    test_input = ["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)\n", "trh fvjkl sbzzf mxmxvkd (contains dairy)\n", "sqjhc fvjkl (contains soy)\n", "sqjhc mxmxvkd sbzzf (contains fish)\n"]

    test(5, run_lines(test_input))
    print(run())
