import heaps


def greedy_scheduler_diff(job_list):
    schedule_heap = heaps.Minheap()
    # Push all jobs with their priority onto the scheduler heap
    # Priority here: job weight - job length (encoded as length-weight on a
    # minimum heap)
    for job in job_list:
        # Subtract a bit of job weight to handle ties
        schedule_heap.push((job[1]-job[0] - .0001 * job[0], job[0], job[1]))
    # Initialize completion time and completion cost
    completion_time = 0
    cost = 0
    # Complete jobs in decreasing priority (that is, popped ascendingly from the
    # minimum heap) and compute their completion times and costs.
    while len(schedule_heap) > 0:
        next_job = schedule_heap.pop()
        completion_time += next_job[2]
        cost += completion_time * next_job[1]
    # Return total completion cost
    return int(cost)


def greedy_scheduler_ratio(job_list):
    schedule_heap = heaps.Minheap()
    # Push all jobs with their priority onto the scheduler heap
    # Priority here: job weight / job length (encoded as length/weight on a
    # minimum heap)
    for job in job_list:
        schedule_heap.push((job[1]/job[0], job[0], job[1]))
    # Initialize completion time and completion cost
    completion_time = 0
    cost = 0
    # Complete jobs in decreasing priority (that is, popped ascendingly from the
    # minimum heap) and compute their completion times and costs.
    while len(schedule_heap) > 0:
        next_job = schedule_heap.pop()
        completion_time += next_job[2]
        cost += completion_time * next_job[1]
    # Return total completion cost
    return int(cost)


test_files = ['jobs_test1.txt', 'jobs_test2.txt']
hw_file = ['jobs_hw.txt']

for filename in hw_file:
    with open(filename, 'r') as f:
        rows = f.read().split('\n')
        jobs = []
        # Omit first row, which contains number of jobs
        for row in rows[1:]:
            row = row.split(' ')
            row = map(float, row)
            jobs.append(row)
        print
        print 'Reading complete.'
        print
        print 'Difference:', greedy_scheduler_diff(jobs)
        print '     Ratio:', greedy_scheduler_ratio(jobs)