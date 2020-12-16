#!/usr/bin/env python3
def main(input_list, n):
    turns_spoken = {}  # Maps a number to a list of turns on which it was previously spoken
    most_recent = None

    turn = 1
    while turn <= n:
        if len(input_list) > 0:
            # Work our way through the list of given numbers first
            next_number = input_list[0]
            input_list = input_list[1:]
        else:
            # Once we're done with the input list, we consider the most recently spoken number.
            # If it's the first time it has been spoken, we say 0. If it has been spoken before,
            # we say the number of turns it has been since it was last spoken.
            if most_recent is None:
                print('Got to the end of the input list without setting most_recent!')
                return

            # There's no reason most_recent WOULDN'T be in num_times_spoken...
            # after all, it was the last one spoken. Nevertheless, we check.
            if most_recent in turns_spoken and len(turns_spoken[most_recent]) == 1:
                next_number = 0
            else:
                previous_turns = turns_spoken[most_recent][-2:]
                next_number = previous_turns[1] - previous_turns[0]

        # Now that we know what the next number should be, 'speak' it by adding/updating
        # it to last_turn_spoken and num_times_spoken and setting the most recent
        most_recent = next_number
        if most_recent not in turns_spoken:
            turns_spoken[most_recent] = [turn]
        else:
            turns_spoken[most_recent].append(turn)

        turn = turn + 1

    print('The {0}th number spoken is {1}'.format(n, most_recent))


if __name__ == '__main__':
    real_input = [6, 4, 12, 1, 20, 0, 16]
    test_input1 = [0, 3, 6]
    test_input2 = [3, 2, 1]
    main(real_input, 30000000)
