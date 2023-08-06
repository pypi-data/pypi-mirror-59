# PyFiFinder

<p>PyFinder is a basic tool to search for archives passing their formats</p>

## How to use?

create PyFiFinder object by passing path to directorie and passing one list that containg all formats to search

```python
from PyFiFinder import PyFinder

# Create new pyfinder object
finder = PyFinder('path/to/search', ['mp3', 'mp4', 'mkv'])

# Start the search
finder.start()

# Save results

finder.save()

```

Author: M4rk<br/>
License: MIT
