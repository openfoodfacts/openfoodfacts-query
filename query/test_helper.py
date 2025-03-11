from typing import Any, List
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
        

# class Cursor:
#     def __init__(self, data: List[Any]):
#         self.data = data
#         self.index = -1

#     async def next(self):
#         self.index += 1
#         return self.data[self.index] if self.index < len(self.data) else None

#     async def close(self):
#         pass
