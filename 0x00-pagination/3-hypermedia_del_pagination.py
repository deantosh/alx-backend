#!/usr/bin/env python3
"""
Implement a method named get_page that takes two integer arguments page with
default value 1 and page_size with default value 10.

 - You have to use this CSV file (same as the one presented at the top of the
   project)
 - Use assert to verify that both arguments are integers greater than 0.
 - Use index_range to find the correct indexes to paginate the dataset
   correctly and return the appropriate page of the dataset (i.e. the correct
   list of rows).
 - If the input arguments are out of range for the dataset, an empty list
   should be returned.
"""
import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns the range of indexes corresponding to those particular
       pagination parameters.
    """

    # calculate the start index
    start_index = (page - 1) * page_size

    # calculate the index index
    last_index = start_index + page_size

    return (start_index, last_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Read pages of content from a file
        """
        # validate input
        assert isinstance(page, int) and page > 0, (
            "Page must be an integer and greater than 0"
        )
        assert isinstance(page_size, int) and page_size > 0, (
            "Page size must be an integer and greater than 0"
        )

        # Get a list from the file lines
        dataset = self.dataset()

        # Get start and end index of the lines in list
        start_index, last_index = index_range(page, page_size)

        # Handle out of range error
        if start_index > len(dataset):
            return []

        # slice dataset and return a list of list
        return dataset[start_index:last_index]

    def get_hyper(self, page: int, page_size: int) -> Dict:
        """Paginate using hypermedia
        """
        # Get the values of  keys
        dataset = self.get_page(page, page_size)
        prev_page = page - 1
        next_page = page + 1

        # Calculate the total number of pages
        total_num_pages = math.ceil(len(self.__dataset) / page_size)
        if page > total_num_pages:
            page_size = 0
            next_page = None

        # case: no previous page
        if page - 1 == 0:
            prev_page = None

        return {
            'page_size': page_size,
            'page': page,
            'data': page_data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_num_pages
        }

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Returns dataset with metadata to allow to perform the next query
        """
        # Get sorted dataset
        sorted_dataset = self.indexed_dataset()

        # If index is None, set it to 0
        if index is None:
            index = 0

        # validate index is in range
        assert 0 <= index < len(sorted_dataset), "Index out of range"

        # Get the last index
        next_index = index + page_size

        # Get the selected keys
        selected_keys = [key for key in range(
            index, next_index) if key in sorted_dataset]

        # Retrieve corresponding values
        page_dataset = [sorted_dataset[key] for key in selected_keys]

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': page_dataset
        }