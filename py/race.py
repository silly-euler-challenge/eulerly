#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Loads and confront the results for different implementations of the euler problems

import imp
import os
import time

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

def load_and_perform_solve(author_dir, filename):
    '''
    Loads a python module from the author dir, assuming it contains a function name solve without args.
    Calls solve() over and over until MIN_SOLVE_TIME_MILLIS are passed.
    Returns a result object.
    '''
    basename = os.path.basename(filename)
    solver = imp.load_source("%s_%s" % (author_dir, basename), os.path.join(author_dir, filename))

    task = lambda: solver.solve()
    result, iterations, elapsed = execute_task_repeatedly(task)

    return Result(author=author_dir, problem_name=basename, result=result, elapsed_millis=elapsed, iterations=iterations)


class Result():
    def __init__(self, author=None, problem_name=None, result=None, elapsed_millis=0, iterations=1):
        self.author = author
        self.problem_name = problem_name
        self.result = result
        self.elapsed_millis = elapsed_millis
        self.iterations = iterations

    def score(self):
        '''
        Score is the number of iterations for unit of time.
        '''
        return float(self.iterations) / float(self.elapsed_millis)

    def __str__(self):
        return "[%s@%s] result [%s] elapsed [%d] iterations [%d] score [%f]" % (self.author, self.problem_name, str(self.result), self.elapsed_millis, self.iterations, self.score())

def enumerate_w_first(items):
    for i, item in enumerate(items):
        yield i == 0, item

def compare_solutions():
    # look for all *.py files in dirs /v and /m. Take only the ones that appear in both dirs.
    authors_dirs = ['m', 'v']
    problems = map(lambda dir: set(filter(lambda x: x.endswith('.py'), os.listdir(dir))), authors_dirs)
    problems = reduce(lambda p1, p2: p1 & p2, problems)

    print('found [%d] problems implementations to compare...' % len(problems))

    for problem in problems:
        print("-----------------------------------------------------")
        print(problem)
        print("-----------------------------------------------------")
        results = []
        for author in authors_dirs:
            print("... running %s by %s" % (problem, author))
            results.append(load_and_perform_solve(author, problem))

        # faster (i.e. higher iterations/elapsed time) wins.
        sorted_results = sorted(results, key=lambda x: x.score(), reverse=True)
        for winner, result in enumerate_w_first(sorted_results):
            if winner:
                print("%s wins!" % result.author)
            print(str(result))    

if __name__ == "__main__":
    compare_solutions()
