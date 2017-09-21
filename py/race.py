#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Loads and confront the results for different implementations of the euler problems

import imp
import os
import time
import sys
import warnings

MIN_SOLVE_TIME_MILLIS = 1000

def current_time_millis():
    return int(round(time.time() * 1000))

def execute_task_repeatedly(task, min_execution_time=MIN_SOLVE_TIME_MILLIS):
    '''
    Executes task() repeatedly until min_execution_time has passed.
    return the tuple (last_result, iterations, elaspsed_time_millis)
    '''
    iteration = 0
    start_time = current_time_millis()
    result = None
    while True:
        iteration += 1
        result = task()
        elapsed = current_time_millis() - start_time;
        if (elapsed > MIN_SOLVE_TIME_MILLIS):
            break
    return result, iteration, elapsed


class Raceable():
    def __init__(self, problem_name=None, author=None, description=None, implementation=None):
        self.problem_name = problem_name
        self.author=author
        self.description = description
        self.implementation = implementation

class RaceableResult():
    def __init__(self, value=None, elapsed_millis=0, iterations=1):
        self.value = value
        self.elapsed_millis = elapsed_millis
        self.iterations = iterations

    def score(self):
        '''
        Score is the number of iterations for unit of time.
        '''
        return float(self.iterations) / float(self.elapsed_millis)


class RaceableRunResult():
    def __init__(self, raceable=None, result=None):
        self.raceable = raceable
        self.result = result

    def score(self):
        return self.result.score()

    def __str__(self):
        return "[%s :: %s] result [%s] elapsed [%d] iterations [%d] score [%f]" % (self.raceable.author, self.raceable.description, str(self.result.value), self.result.elapsed_millis, self.result.iterations, self.score())


def load_raceables_from_file(filepath):
    '''
    Loads all raceables from a file.
    '''
    raceables = []
    parent_dir = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    with warnings.catch_warnings(): # suppressing warnings about module naming not being consistent... who cares.

        warnings.simplefilter("ignore")
        module = imp.load_source("%s_%s" % (parent_dir, basename), filepath)
        if hasattr(module, 'race') and 'raceables' in module.race:
            problem_name = module.race.get('problemName', basename)
            author = module.race.get('author', 'unknown')
            print("looking into [%s]" % filepath)
            for desc, impl in module.race['raceables'].iteritems():
                print("found %s's %s" % (author, desc))
                raceables.append(Raceable(problem_name, author, desc, impl))

    return raceables



def scan_raceables(filter_text=''):
    '''
    Load all raceables from all files matching a filter.
    '''
    raceables = []
    current_file_path = os.path.realpath(__file__)
    base_dir  = os.path.dirname(current_file_path) # the dir where this script resides.
    for dirpath, dirnames, filenames in os.walk(base_dir):
        filenames = filter(lambda f: f != current_file_path, filenames) # exluce this very same script
        filenames = filter(lambda f: f.endswith('.py'), filenames)
        filenames = filter(lambda f: filter_text in f, filenames)
        filepaths = map(lambda f: os.path.join(dirpath, f), filenames)
        for f in filepaths:
            items = load_raceables_from_file(f)
            raceables.extend(items)

    # group by problem name
    raceables_by_problem = {}
    for r in raceables:
        v = raceables_by_problem.get(r.problem_name, [])
        v.append(r)
        raceables_by_problem[r.problem_name] = v

    return raceables_by_problem


def run_race(focus_problem=None):
    raceables_by_problem = scan_raceables()
    problem_names = raceables_by_problem.keys()

    if (focus_problem): # concentrate on a single problem.
        print("Focusing on problem [%s]" % (focus_problem))
        problem_names = filter(lambda x: x == focus_problem, problem_names)

    print('found [%d] problems' % (len(problem_names)))

    for problem in problem_names:
        print("-----------------------------------------------------")
        print(" Running solutions for problem [%s]" % problem)
        print("-----------------------------------------------------")
        raceables = raceables_by_problem[problem]
        results = []
        for r in raceables:
            print("... running %s's %s" % (r.author, r.description))
            result_value, iterations, elapsed = execute_task_repeatedly(r.implementation)
            res = RaceableResult(result_value, elapsed, iterations)
            results.append(RaceableRunResult(raceable=r, result=res))

        # sort on score desc.
        # faster (i.e. higher #iterations/elapsed) wins.
        sorted_results = sorted(results, key=lambda x: x.score(), reverse=True)
        for i, item in enumerate(sorted_results):
            print("#%d - %s" % (i + 1, str(item)))


if __name__ == "__main__":
    # filter on a particular problem.
    focus_problem = None
    if len(sys.argv) > 1:
        focus_problem = sys.argv[1]

    run_race(focus_problem)
