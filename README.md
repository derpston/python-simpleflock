python-simpleflock
==================

Python module for very simple flock-based file locking.

Features
--------
* Uses Python's ```with``` syntax.
* Doesn't complain if the lock file already exists but is stale.
* Cleans up the lock file after itself.
* Supports a timeout.

Example
-------
```python
import simpleflock

with simpleflock.SimpleFlock("/tmp/foolock"):
   # Do something.
   pass

# Raises an IOError in 3 seconds if unable to acquire the lock.
with simpleflock.SimpleFlock("/tmp/foolock", timeout = 3):
   # Do something.
   pass
```

BUGS
----
Unknown.

Contributing
------------
Contributions welcome!
