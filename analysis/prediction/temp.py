import pickle

with open('analysis/prediction/preds', 'rb') as f:
    temp = pickle.load(f)
    for i in range(10):
        print(temp[i])
