from sklearn.metrics import accuracy_score
from itertools import permutations

def acc_score(groups, pred_groups):
    score_res = 0
    yhat_mod = []
    for ind_pred in permutations('012', 3):
        ind_pred = [int(i) for i in list(ind_pred)]
        corresp_groups = dict(zip([0,1,2], list(ind_pred)))
        pred_groups_mod = [corresp_groups[g] for g in pred_groups]
        score = accuracy_score(groups, pred_groups_mod)
        if score > score_res:
            score_res = score
            yhat_mod = pred_groups_mod

    return score_res, yhat_mod
