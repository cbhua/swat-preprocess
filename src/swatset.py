import numpy as np
from torch.utils.data import Dataset


class SwatDataset(Dataset):
    ''' Dataset class generator on SWaT dataset.
    
    Args:
        - path: <str> preprocessed dataset numpy file path
        - feature_idx: <list<int>> choose features you want to use by index
        - start_idx: <int> choose period you want to use by index
        - end_idx: <int> choose period you want to use by index
        - windows_size: <int> history length you want to use
        - sliding: <int> history window moving step
    '''

    def __init__(self, path,
                 feature_idx: list,
                 start_idx: int, 
                 end_idx: int, 
                 windows_size: int,
                 sliding:int=1):
        data = np.load(path, allow_pickle=True).take(feature_idx, axis=1)[start_idx:end_idx]
        self.data = data
        self.windows_size = windows_size
        self.sliding = sliding

    def __len__(self):
        return int((self.data.shape[0] - self.windows_size) / self.sliding) - 1

    def __getitem__(self, index):
        '''
        Returns:
            input: <np.array> [num_feature, windows_size]
            output: <np.array> [num_feature]
        '''
        start = index * self.sliding
        end = index * self.sliding + self.windows_size
        return self.data[start:end, :], self.data[end + 1, :]


if __name__ == '__main__':
    dataset = SwatDataset('../data/swat-2015-data.npy', [1, 2, 3], 800, 900, 10, 1)
    print(dataset.__len__())
    input, output = dataset.__getitem__(0)
    print(input.shape)
    print(output.shape)
    