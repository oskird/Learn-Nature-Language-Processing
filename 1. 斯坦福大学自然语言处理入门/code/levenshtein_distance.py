# levenshtein distance solution with dynamic programming
import numpy as np
def levenshtein_distance(source, target, keep_matrix=True):
    # 计算字符长度、创建零矩阵
    height = len(source) + 1
    width = len(target) + 1
    matrix = np.zeros((height,width))
    # 初始化
    for i in range(width):
        matrix[0][i] = i
    for j in range(height):
        matrix[j][0] = j
    # 计算每个位置的最小值
    for i in range(1, height):
        for j in range(1, width):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 2
            a = matrix[i - 1][j] + 1
            b = matrix[i][j - 1] + 1
            c = matrix[i - 1][j - 1] + cost
            matrix[i][j] = min(a, b, c)
    # 输出
    if keep_matrix == True: return int(matrix[-1][-1]), matrix
    else:     
        return int(matrix[-1][-1])
# test 1
levenshtein_distance('sum','sune')
# test 2
levenshtein_distance('intention','execution')