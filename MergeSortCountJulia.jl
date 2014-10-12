function merge_count(A, B)
   merged = Int64[]
   inv_count = 0
   while ((length(A) > 0) || (length(B) > 0))
       if length(A) == 0
           append!(merged, B)
           B = []
       elseif length(B) == 0
           append!(merged, A)
           A = []
       else
           if A[1] <= B[1]
               push!(merged, shift!(A))
           else
               push!(merged, shift!(B))
               inv_count += length(A)
           end
       end
   end
   return (merged, inv_count)
end

function merge_sort_count(Lst)
    if length(Lst) == 0 || length(Lst) == 1
        return (Lst, 0)
    else
        center = floor(length(Lst) / 2)
        first_half = Lst[1:center]
        second_half = Lst[(center+1):]

        (first_sorted, first_count) = merge_sort_count(first_half)
        (second_sorted, second_count) = merge_sort_count(second_half)

        sorted, split_count = merge_count(first_sorted, second_sorted)
    end
    return (sorted, first_count + second_count + split_count)
end

function count_inversions(Lst)
    (sorted, count) = merge_sort_count(Lst)
    return count
end

# Some test cases
A = [1, 4, 2] # 1
B = [3, 5, 6] # 0
C = [37, 7, 2, 14, 35, 47, 10, 24, 44, 17, 34, 11, 16, 48, 1, 39, 6, 33, 43, 26,
     40, 4, 28, 5, 38, 41, 42, 12, 13, 21, 29, 18, 3, 19, 0, 32, 46, 27, 31, 25,
     15, 36, 20, 8, 9, 49, 22, 23, 30, 45] # 590
D = [1, 6, 3, 2, 4, 5] # 5
E = [9, 12, 3, 1, 6, 8, 2, 5, 14, 13, 11, 7, 10, 4, 0] # 56

f = open("IntegerArray.txt")
a = readlines(f) #.strip('\r\n')
intArray = Int64[]
for line in a
    chomp(line)
    push!(intArray, parseint(Int64, line))
end

#print(count_inversions(intArray))
print(@elapsed count_inversions(intArray))
