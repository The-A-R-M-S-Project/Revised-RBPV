from __future__ import print_function

import io
import sys

from ortools.sat.python import cp_model


class RoomsPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, allocations, lectures, lecture_attendants, lecture_students, rooms_names, rooms_capacity, days,
                 timestamps, shift_requests, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._allocations = allocations
        self._lecture = lectures
        self._lectures = lecture_attendants
        self._students = lecture_students
        self._rooms = rooms_names
        self._capacity = rooms_capacity
        self._days = days
        self._requests = shift_requests
        self._timestamps = timestamps
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print('Solution %i' % self._solution_count)
            for d in range(self._days):
                print('&Day %i' % d)
                data = []
                raze = []
                for p in range(self._timestamps):
                    l = 0
                    while l < len(self._lectures):
                        if self.Value(self._allocations[(l, d, p)]) == 1:
                            if self._requests[l][d][p] == 1:
                                print('&  %s is at timestamp %i [Requested]&' % (self._lectures[l], p))
                                data.append(self._lectures[l])
                            else:
                                print('&  %s is at timestamp %i [Not Requested]&' % (self._lectures[l], p))
                                data.append(self._lectures[l])
                        l += 1

                    # Allocate lectures assigned to a timestamp to rooms based on capacity
                    # Adds number of lecture students at a given timestamp to raze array from lectures' dict
                    for q in data:
                        raze.append(self._lecture[q])
                    allocations = {}

                    # Enumerates room capacities and raze's lectures' student numbers
                    # Assigns capacity to lectures' student numbers based on index and adds pair to dict
                    for i, j in enumerate(self._capacity):
                        for l, m in enumerate(raze):
                            if i == l:
                                allocations.update({j: m})
                        else:
                            pass
                    # create list of capacities and lectures in dict
                    room = list(allocations.keys())
                    capacity = list(allocations.values())
                    capacity.sort(reverse=True)

                    stuff = []
                    cool = []

                    # for each capacity obtain corresponding room name in capacity list
                    for r in room:
                        stuff.append(self._rooms[room.index(r)])

                    for w in capacity:
                        res = dict((v, k) for k, v in self._lecture.items())
                        cool.append(res[w])

                    room_allocations = dict(zip(stuff, cool))
                    print('& ', room_allocations)
                    data.clear()
                    raze.clear()
                    print()
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


def main():
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    # Data.
    group_a = {'AGR2101': 210, 'CIV3101': 215, 'CMP1101': 220, 'LLD2101': 225, 'YTR4101': 230, 'AXR5101': 235,
               'GRE2103': 240, 'BEE2107': 245, 'POD3106': 250, 'ZIP6201': 255}
    group_b = {'AGR3101': 115, 'CIV3103': 120, 'CMP1105': 125, 'LLD2106': 130, 'YTR5102': 135, 'AXR2109': 140,
               'GRE3205': 145, 'BEE6108': 150, 'POD7103': 200, 'ZIP1106': 205}
    group_c = {'VIB3304': 95, 'NUR6204': 100, 'ECO3201': 105, 'LUG4101': 110}
    group_d = {'RES2101': 65, 'ENT2202': 70, 'SUN1101': 75, 'OOP3209': 80, 'HUN4501': 85, 'JIK1202': 90}
    group_e = {'QUU4104': 50, 'QOO4201': 55, 'QII9201': 60}

    lectures = {**group_a, **group_b, **group_c, **group_d, **group_e}
    lecture_attendants = list(lectures.keys())
    lecture_students = list(lectures.values())

    num_lectures = len(lectures)

    rooms = {'M3': 300, 'M2': 200, 'M1': 100}
    rooms_names = list(rooms.keys())
    rooms_capacity = list(rooms.values())

    days = 7
    timestamps = 7

    all_days = range(days)
    all_timestamps = range(timestamps)
    all_lectures = range(num_lectures)

    # shift requests: Each row consists of 7 sets corresponding to the 7 days
    #                 Each set contains 7 boolean variables, corresponding to the 7 time stamps
    #                 Lastly, 33 rows for each lecture to make a specific request
    # Requests are not above constraints and are only implemented after.

    shift_requests = [[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
                      [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]]

    # Create the model
    model = cp_model.CpModel()

    # Creating shift variables
    # allocations[(l, d, p)]: lecture 'l' is on day 'd' at time 'p'
    allocations = {}
    for l in all_lectures:
        for d in all_days:
            for p in all_timestamps:
                allocations[l, d, p] = model.NewBoolVar('allocations_l%i d%i p%i' % (l, d, p))

    # Only 3 lectures are ongoing at any given timestamp [related to number of rooms at facility]
    for d in all_days:
        for p in all_timestamps:
            model.Add(sum(allocations[(l, d, p)] for l in all_lectures) == 3)

            # Any lecture only happens once on a given day
    for l in all_lectures:
        for d in all_days:
            model.Add(sum(allocations[(l, d, p)] for p in all_timestamps) <= 1)

    # Lectures in group c cannot be on a weekend [Saturday and Sunday]
    for d in all_days[5:7]:
        for p in all_timestamps:
            model.Add(sum(allocations[(l, d, p)] for l in
                          all_lectures[len({**group_a, **group_b}): len({**group_a, **group_b, **group_c})]) == 0)

    # Lectures in group d can only be in the afternoon
    for l in all_lectures[len({**group_a, **group_b, **group_c}): len({**group_a, **group_b, **group_c, **group_d})]:
        for d in all_days:
            model.Add(sum(allocations[(l, d, p)] for p in all_timestamps[0:3]) == 0)

    # Lectures in group e can only be in the morning
    for l in all_lectures[len({**group_a, **group_b, **group_c, **group_d}): len(
            {**group_a, **group_b, **group_c, **group_d, **group_e})]:
        for d in all_days:
            model.Add(sum(allocations[(l, d, p)] for p in all_timestamps[4:6]) == 0)

    # Lectures in group e cannot occur on Monday and Tuesday
    for d in all_days[0:3]:
        for p in all_timestamps:
            model.Add(sum(allocations[(l, d, p)] for l in all_lectures[
                                                          len({**group_a, **group_b, **group_c, **group_d}): len(
                                                              {**group_a, **group_b, **group_c, **group_d,
                                                               **group_e})]) == 0)

    # Split the constraint, one to provide days the other for timestamps but same lectures
    # for example a lecture can only be in the morning AND never on weekends

    # dealing with extra lectures. max lectures per week
    min_timestamps_per_lecture = (21 * days) // num_lectures
    max_timestamps_per_lecture = min_timestamps_per_lecture + 1

    for l in all_lectures:
        num_timestamps_worked = sum(allocations[(l, d, p)] for d in all_days for p in all_timestamps)
        model.Add(min_timestamps_per_lecture <= num_timestamps_worked)
        model.Add(num_timestamps_worked <= max_timestamps_per_lecture)

    # try to ensure as many requests  as possible are catered for, constraints observed

    model.Maximize(
        sum(shift_requests[l][d][p] * allocations[(l, d, p)] for l in all_lectures
            for d in all_days for p in all_timestamps))

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    # Display the first two solutions.
    a_few_solutions = range(1)
    solution_printer = RoomsPartialSolutionPrinter(allocations, lectures, lecture_attendants, lecture_students,
                                                   rooms_names, rooms_capacity, days, timestamps, shift_requests,
                                                   a_few_solutions)
    # solver.SearchForAllSolutions(model, solution_printer)
    solver.SolveWithSolutionCallback(model, solution_printer)

    # Statistics.
    print()
    print('Statistics')
    print('     Number of shifts requests met = %i' % solver.ObjectiveValue(),
          '(out of', num_lectures * min_timestamps_per_lecture, ')')
    print('     Wall time       : %f s' % solver.WallTime())
    print('     Number of conflicts = %i' % solver.NumConflicts())
    print('     Number of branches = %i' % solver.NumBranches())
    print('     Number of booleans = %i' % solver.NumBooleans())

    output = new_stdout.getvalue()
    return output


if __name__ == '__main__':
    main()
