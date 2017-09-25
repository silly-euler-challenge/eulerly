#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Loads and confront the results for different implementations of the euler problems

import imp
import os
import time
import sys
import warnings
import gc
from multiprocessing import Process, Queue

MIN_SOLVE_TIME_MILLIS = 2000

class Clock:
    '''
    A simple clock that returns milliseconds - unfortunately not cpu time (available only in py 3.3)
    '''
    def __init__(self):
        # chose the best clock depending on OS.
        unix_clock_ms = lambda: int(round(time.time() * 1000))
        win32_clock_ms = lambda: int(round(time.clock() * 1000))
        self.__clock = win32_clock_ms if sys.platform == "win32" else unix_clock_ms
        self.__start_time = None

    def start(self):
        self.__start_time = self.__clock()

    def elapsed(self):
        if not self.__start_time:
            return 0
        return self.__clock() - self.__start_time


def execute_in_child_process(task, min_execution_time=MIN_SOLVE_TIME_MILLIS):
    '''
    Executes task() repeatedly until min_execution_time has passed in a child process, 
    returning the tuple (last_result, iterations, elaspsed_time_millis)
    '''

    # executes task in a child process, and get the result via an IPC mechanism (queue)
    # the forked process will put into the queue.
    q = Queue()

    # this is what we going to execute in the forked process
    def f(queue, task):
        gc.disable() # garbage collection might affect timings.
        clock = Clock()
        iteration = 0
        result = None
        clock.start()
        while True:
            iteration += 1
            result = task()
            elapsed = clock.elapsed()
            if (elapsed > min_execution_time):
                break
        q.put((result, iteration, elapsed))
        gc.enable() # should not be needed, the forked process just dies after this, but for symmetry...


    p = Process(target=f, args=(q, task))
    p.start()
    results =  q.get() # get the result
    p.join()
    return results

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


def enumerate_w_ties(results, tie_threshold=0.02):
    '''
    Generator for RaceableRunResult that will yield runs that are tied in first place.
    If no run is tied at the top score, the generator will not yield anything.
    We consider a draw 
    '''
    if results:
        sorted_results = results
        if len(results) > 1:
            sorted_results = sorted(results, key=lambda x: x.score(), reverse=True)
            highest_score = sorted_results[0].score()
            is_tied_at_top = lambda score: (1 - (second_highest_score / highest_score)) < tie_threshold
            second_highest_score = sorted_results[1].score()
            has_tie = is_tied_at_top(second_highest_score)
        else:
            has_tie = False
            
        for i, result in enumerate(sorted_results):
            if i < 2:
                yield i, result, has_tie
            else:
                yield i, result, is_tied_at_top(result.score)
        

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
            result_value, iterations, elapsed = execute_in_child_process(r.implementation)
            res = RaceableResult(result_value, elapsed, iterations)
            results.append(RaceableRunResult(raceable=r, result=res))

        for i, item, is_tied_at_top in enumerate_w_ties(results):
            if (is_tied_at_top):
                print("#1 (tied) - %s" % (str(item)))
            else:
                print("#%d - %s" % (i + 1, str(item)))
            

if __name__ == "__main__":
    # filter on a particular problem.
    focus_problem = None
    if len(sys.argv) > 1:
        focus_problem = sys.argv[1]

    run_race(focus_problem)
