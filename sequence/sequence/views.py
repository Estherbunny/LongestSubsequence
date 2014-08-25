from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import urllib
import time

""" API call to obtain the longest increasing subsequence from an input string of integers """
"""   The following functions are used:                                                    """
"""   longest : processes the API call, cleans data, calls function implementing the       """ 
"""                     algorithm, formats the output and returns the result in JSON       """
"""   print_answers : takes the output of the algorithm (list of indexes) and finds the    """
"""                     corresponding values in the input. also outputs the indexes        """
"""                     themselves, and runtime, if verbose is true                        """
"""   longest_increasing : first attempt at implementing the algorithm. Functional, but    """
"""                     takes O(n^2) time. No longer used.                                 """
"""   smartest_longest_increasing : the algorithm, which takes O(nlogn) time to find the   """
"""                     longest increasing subsequence                                     """

@csrf_exempt
def longest(request):
    response_data = {}

    # (1) get POST data for the input number string (num_array) and the verbose flag

    # first make sure the request is a POST
    if request.method!="POST":
        response_data['error'] = "Only method 'POST' is allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # then make sure request body has data
    try:
        json_data = json.loads(request.body)
    except:
        response_data['error'] = 'Request data not properly formatted'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # get the two parts of JSON data, "num_array" number inputs, and (optional) verbose flag
    num_array = json_data.get('num_array','')
    verbose = json_data.get('verbose',0)

    # return an error if "num_array", is not found
    if not num_array:
        response_data['error'] = "'num_array' not specified"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # process "num_array" data. remove any trailing or leading spaces or commas. separate at the comma
    num_array = num_array.strip().strip(',').strip()
    num_vals_stripped = num_array.split(',')

    if len(num_vals_stripped)>1000:
        response_data['error'] = "Input numbers are limited to 1,000 values"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # check that all "num_array" elements have integer values, and convert to integers if they do
    num_vals = []
    try:
        num_vals = [int(elem.strip()) for elem in num_vals_stripped]
    except:
        response_data['error'] = "Input numbers do not contain valid values"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    if [1 for elem in num_vals if not isinstance(elem,int)]:
        response_data['error'] = "Input numbers should only contain integer values (-9223372036854775808 to 9223372036854775807)"
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # (2) Call function for Longest Increasing Sequence
    if verbose:
        start = time.time()
    linked_answer,linked_answer_start = smartest_longest_increasing(num_vals)
    if verbose:
        end = time.time()

    # Convert the array of indexes ("linked_answer") to output number string ("out_vals")
    #   if verbose, output the indexes of numbers that were part of longest subsequence ("out_indexes") 
    out_vals,out_indexes = print_answers(num_vals,linked_answer,linked_answer_start,verbose)

    # (3) Format the output values and indexes, and return as JSON
    response_data['out'] = ','.join(["%s" % out_val for out_val in out_vals])
    if verbose:
        response_data['indexes'] = ','.join(["%s" % out_idx for out_idx in out_indexes])
        response_data['time'] = "%s" % (end - start)

    return HttpResponse(json.dumps(response_data), content_type="application/json")




""" Takes the indexes from our algorithm ("linked_answer") and finds the  """
"""    corresponding value in our list, so that we return a list of       """
"""    increasing numbers (out_vals). If print_indexes is true, print the """
"""    indexes as well                                                    """
def print_answers(list1,linked_answer,linked_answer_start,print_indexes=False):
    next_link = linked_answer_start
    out_vals = []
    if print_indexes:
        out_indexes = [linked_answer_start,]
    else:
        out_indexes = []

    while next_link != -1:
        out_vals.append(list1[next_link])
        next_link = linked_answer[next_link]
        if print_indexes and next_link != -1:
            out_indexes.append(next_link)

    return reversed(out_vals),reversed(out_indexes)




""" This is the long way to find subsequence of increasing integers O(n^2)  """
"""    (we did not end up using this, but it was our first answer)          """
""" Loop through the input "list1", and determine if the longest increasing """
"""    subsequence can be updated based on previously values in the list    """
def longest_increasing(list1):

    N = len(list1)
    # all numbers in list will have a longest subsequence of at least 1 (themselves)   
    longest = [1]*N

    # linked_answer will be a pointer to previous integer in this subsequence
    # linked_answer_start is where one would begin following linked_answer to 
    #    trace back and find the optimal subsequence 
    linked_answer= [-1]*N
    linked_answer_start = 0

    # L is the current longest subsequence length
    L = 1

    # iterate through the input(list1), and for every data point i,
    #    for the previous values in list1, see if we have found a data point that
    #    is both increasing from some value j previously seen, and for which
    #    a longer subsequence is possible when we form a subsequence with that j
    for i in range(1,N):
        j = i
        while j >= 0:
            if ((longest[j] + 1) > longest[i]) and (list1[j] < list1[i]):
                longest[i] = longest[j] + 1
                linked_answer[i] = j
            j -= 1

        # keep track of the longest subsequence thus far
        #    and the index  to start tracing back to discover the subsequence
        if longest[i] > L:
            L = longest[i]
            linked_answer_start = i

    return (linked_answer,linked_answer_start)




"""       The Algorithm for Longest Increasing Subsequence                    """
""" Loop through the input "list1", and determine if the longest increasing   """
"""    subsequence can be updated based on previously values in the list      """
""" Rather than explicitly checking every previous value as in the O(n^2)     """
"""    solution, use a list S which tracks the best solution thus far.        """
""" S is a list which tracks the best subsequence as we iterate               """
"""    i = 1 to N (length of input "list1"). Specifically, an entry in S is   """ 
""" S[length of subseq.] = index of final integer in optimal subseq. in list1 """
""" It follows that list1[S[i-1]] < list1[S[i]], since if there did exist a   """
"""    a list[S[i]] that was less than list1[S[i-1]], then one would have had """
"""    to have updated list1[S[i-1]] with the index of whatever integer came  """
"""    before in the subsequence leading up to list[S[i]]                     """ 
""" We use the array "linked_answer", of size N, to point to the previous     """
"""    integer in list1 that forms the best subsequence at any point i        """
""" The value of linked_answer for point i can be updated at the moment       """
"""    S is updated for the new value of list[i].                             """

def smartest_longest_increasing(list1):

    N = len(list1)

    # linked_answer will be a pointer to previous integer in this subsequence
    # linked_answer_start is where one would begin following linked_answer to 
    #    trace back and find the optimal subsequence 
    linked_answer= [-1]*N
    linked_answer_start = 0

    # L is the current longest subsequence length
    L = 1

    # S is an array of index values for the optimal subsequences
    # S[length of subseq.] = index of final integer in optimal subseq. in list1
    S = [-1]*N
    S[0] = 0

    for i in range(1,N):

        if list1[i] == list1[i-1]:
            # a repeated value won't alter the final solution 
            pass
        else:

            # find the place where list[i] would be "inserted" into the "list" formed
            #    by [list1[elem] for elem in S[:L]]. The insertion point
            #    for repeated values will be to the left of other values.
            #    If the insertion point is at the end of S, then a new
            #    "longest length" has been found

            # Originally done with bisect, but this
            # wastefully performs list1[elem] for every elem in S
            #     import bisect
            #     S_place = bisect.bisect_left([list1[elem] for elem in S[:L]],list1[i])

            # Efficient Binary Insertion, where a repeated value is inserted to 
            #     the left of the other identical values. Note that we are not going to
            #     actually insert a value (unless we find a new longest-length). 
            lo = 0
            hi = L
            while lo < hi:
                mid = (lo+hi)/2
                if list1[S[mid]] < list1[i]: 
                    lo = mid+1
                else: 
                    hi = mid
            S_place = lo

            # S_place is index of list1[i] within the "list" [list1[elem] for elem in S[:L]]
            # linked_answer is an index to the previous index in a subsequence
            # Since the value stored in S is an index into list[i], to find
            #    the previous (optimal) index in a subsequence, get the value for
            #    the previous S, which is S[S_place-1]
            linked_answer[i] = S[S_place-1]  

            # If S_place represents a new longest-length (by having an insertion point
            #    at the end of S[:L]), then add it to S and increase the longest length, L
            if S_place > (L-1):
                S[S_place] = i
                L += 1
                linked_answer_start = i

            # otherwise if the input value corresponding to the index S[S_place] is 
            #    greater than the new value (list1[i]) that mapped to S_place, update
            #    S[S_place] because it should always be optimal
            elif list1[S[S_place]] > list1[i]:
                S[S_place] = i

    return (linked_answer,linked_answer_start)

