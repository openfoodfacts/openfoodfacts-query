from typing import Any, List
from unittest.mock import Mock
from uuid import uuid4


def random_code():
    return str(uuid4())


async def mock_cursor(data):
    for item in data:
        yield item
        
async def error_cursor(message):
    for index in range(1):
        # Need to include a yield so that an async iterator is created
        if False:
            yield index
        raise Exception(message)
        

def patch_context_manager(mock: Mock, *cursors):
    """ Patching a context manager isn't very intuitive so use this simple helper function to do it """
    # We pop from the end so need to reverse the list
    cursor_list = list(reversed(cursors))
    def next_cursor():
        nonlocal cursor_list
        return cursor_list.pop() if cursor_list else mock_cursor([])
    mock.return_value.__aenter__.side_effect = next_cursor

# class Cursor:
#     def __init__(self, data: List[Any]):
#         self.data = data
#         self.index = -1

#     async def next(self):
#         self.index += 1
#         return self.data[self.index] if self.index < len(self.data) else None

#     async def close(self):
#         pass
