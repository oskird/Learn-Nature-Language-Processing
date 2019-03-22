A = [1,3,4,6,7,9,12]
B = [1,2,3,5,7,8,10,12]

idx1 = 0 # 指针1
idx2 = 0 # 指针2
ans = [] # 匹配到的索引集合
while True:
    if A[idx1]==B[idx2]: # 当出现相同索引时，储存该索引，并使两个指针都前进一步
        ans.append(A[idx1])
        idx1+=1
        idx2+=1
    else:                # 当索引不同时，小的一方指针前进一步
        if A[idx1] < B[idx2]:
            idx1+=1
        else:
            idx2+=1
    if (idx1==len(A)) or (idx1==len(A)): break # 指针超过数组长度时，跳出循环
print(ans)