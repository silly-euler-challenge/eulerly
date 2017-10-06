#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Loads and confront the results for different implementations of the euler problems

import imp
import os
import time
import sys
import warnings
import gc
import uuid
from multiprocessing import Process, Queue

# Allow import Eratostene
sys.path.append(sys.path[0] + "/v")

MIN_SOLVE_TIME_MILLIS = 2000

class Clock:
    '''
    A simple clock that returns milliseconds - unfortunately not cpu time (available only in py 3.3)
    The best clock is used for each platform (win32 -> time.clock(), nix -> time.time()).
    (Best is according to "general wisdom of the internet")
    '''
    def __init__(self):
        # chose the best clock depending on OS.
        unix_clock_ms = lambda: int(round(time.time() * 1000))
        win32_clock_ms = lambda: int(round(time.time() * 1000))
        self.__clock = win32_clock_ms if sys.platform == "win32" else unix_clock_ms
        self.__start_time = None

    def start(self):
        self.__start_time = self.__clock()

    def elapsed(self):
        if not self.__start_time:
            return 0
        return self.__clock() - self.__start_time

# this is what we going to execute in the forked process
def f(queue, module_path, task, min_execution_time):
    gc.disable() # garbage collection might affect timings.

    clock = Clock()
    iteration = 0
    result = None
    module_name = str(uuid.uuid4())
    module = imp.load_source(module_name, module_path)

    if not hasattr(module, task):
        queue.put((None, 1, min_execution_time)) # fake results for not-found stuff.

    runnable = getattr(module, task)

    clock.start()
    while True:
        iteration += 1
        result = runnable()
        elapsed = clock.elapsed()
        if (elapsed > min_execution_time):
            break

    queue.put((result, iteration, elapsed))
    gc.enable() # should not be needed, the forked process just dies after this, but for symmetry...

def run_in_child_process(task_name, module_path, min_execution_time=MIN_SOLVE_TIME_MILLIS):
    '''
    Executes task() repeatedly until min_execution_time has passed in a child process, 
    returning the tuple (last_result, iterations, elaspsed_time_millis)
    '''

    # executes task in a child process, and get the result via an IPC mechanism (queue)
    # the forked process will put into the queue, the main process will wait (indefinitely) for the result
    q = Queue()
    p = Process(target=f, args=(q, module_path, task_name, min_execution_time))
    p.daemon = True
    p.start()
    results = q.get() # get the result
    p.join()
    return results

class Raceable():
    def __init__(self, problem_name=None, author=None, description=None, module_path=None, impl_name=None):
        self.module_path = module_path
        self.problem_name = problem_name
        self.author=author
        self.description = description
        self.impl_name = impl_name


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


def to_str_trunc(obj, max_len=40):
    s = str(obj)
    str_len = max_len - 2
    return s[:str_len] + (s[str_len:] and '..')


class RaceableRunResult():
    def __init__(self, raceable=None, result=None):
        self.raceable = raceable
        self.result = result

    def score(self):
        return self.result.score()

    def __str__(self):
        return "[%s :: %s] result [%s] elapsed [%d] iterations [%d] score [%f]" % (self.raceable.author, self.raceable.description, to_str_trunc(self.result.value), self.result.elapsed_millis, self.result.iterations, self.score())


def load_raceables_from_file(filepath):
    '''
    Loads all raceables from a file.
    '''
    raceables = []
    parent_dir = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    with warnings.catch_warnings(): # suppressing warnings about module naming not being consistent... who cares.

        warnings.simplefilter("ignore")
        module_name = basename
        module = imp.load_source(module_name, filepath)
        if hasattr(module, 'race') and 'raceables' in module.race:
            problem_name = module.race.get('problemName', basename)
            author = module.race.get('author', 'unknown')
            print("looking into [%s]" % filepath)
            for desc, impl in module.race['raceables'].iteritems():
                print("found %s's %s" % (author, desc))
                # assumes that impl is a function with a func_name attr (it works for top level defined functions but not for the rest)
                raceables.append(Raceable(problem_name, author, desc, filepath, impl.func_name))

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
            result_value, iterations, elapsed = run_in_child_process(r.impl_name, r.module_path)
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
