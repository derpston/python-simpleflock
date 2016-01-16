from __future__ import print_function
import time
import os
import fcntl
import errno

class SimpleFlock:
   """Provides the simplest possible interface to flock-based file locking. Intended for use with the `with` syntax. It will create/truncate/delete the lock file as necessary."""

   def __init__(self, path, timeout = None):
      self._path = path
      self._timeout = timeout
      self._fd = None

   def __enter__(self):
      self._fd = os.open(self._path, os.O_CREAT)
      start_lock_search = time.time()
      while True:
         try:
            fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Lock acquired!
            return
         except (OSError, IOError) as ex:
            if ex.errno != errno.EAGAIN: # Resource temporarily unavailable
               raise
            elif self._timeout is not None and time.time() > (start_lock_search + self._timeout):
               # Exceeded the user-specified timeout.
               raise
         
         # TODO It would be nice to avoid an arbitrary sleep here, but spinning
         # without a delay is also undesirable.
         time.sleep(0.1)

   def __exit__(self, *args):
      fcntl.flock(self._fd, fcntl.LOCK_UN)
      os.close(self._fd)
      self._fd = None

      # Try to remove the lock file, but don't try too hard because it is
      # unnecessary. This is mostly to help the user see whether a lock
      # exists by examining the filesystem.
      try:
         os.unlink(self._path)
      except:
         pass

if __name__ == "__main__":
   print("Acquiring lock...")
   with SimpleFlock("locktest", 2):
      print("Lock acquired.")
      time.sleep(3)
   print("Lock released.")



