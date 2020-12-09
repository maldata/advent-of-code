#!/usr/bin/env python3
def main():
    with open('./input.txt', 'r') as f:
        all_lines = f.readlines()

    sequence = [int(i.strip()) for i in all_lines]
    invalid_value = 14360655

    for idx in range(len(sequence)):
        sum_of_subsequent = sequence[idx]
        offset = 0
        while sum_of_subsequent < invalid_value:
            offset = offset + 1
            sum_of_subsequent = sum_of_subsequent + sequence[idx + offset]

        if sum_of_subsequent == invalid_value:
            print('Index {0} and the next {1} values sum to {2}'.format(idx, offset, sum_of_subsequent))
            break

    subsequence = sequence[idx:idx+offset+1]
    sum_of_subseq_min_max = min(subsequence) + max(subsequence)
    print('The sum of the min and max of the subsequence is {0}'.format(sum_of_subseq_min_max))


if __name__ == '__main__':
    main()
