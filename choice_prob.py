import numpy as np
def softmax(f):
    f -= np.max(f)
    return np.exp(f) / np.sum(np.exp(f))

def getChoiceProb(branchInfo, visitNumInfo, visitNumOfParent, temp, p):
    alpha_Hb = (visitNumInfo+0.000000000001)/(visitNumOfParent + 0.000000001)
    alpha_Hb = np.min(np.concatenate((alpha_Hb[np.newaxis,...],
                                      np.ones(alpha_Hb.shape)[np.newaxis,...])), axis=0)
    beta_Hb = (visitNumInfo+0.000000000001)/(branchInfo + 0.000000001)
    beta_Hb = np.min(np.concatenate((beta_Hb[np.newaxis,...],
                                      np.ones(beta_Hb.shape)[np.newaxis,...])), axis=0)
    if np.random.uniform() >= p:
        logits = -1*np.log(beta_Hb)
    else:
        logits = -1*np.log(alpha_Hb)
    prob = softmax(logits/temp)
    return prob