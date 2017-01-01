
import os
import logging
import tempfile

################################################################################
# logging module missing functionality
################################################################################

class BufferingHandler(logging.Handler):
    """
  A handler class which buffers logging records in memory. Whenever each
  record is added to the buffer, a check is made to see if the buffer should
  be flushed. If it should, then flush() is expected to do what's needed.
    """
    def __init__(self, capacity):
        """
        Initialize the handler with the buffer size.
        """
        logging.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = []

    def shouldFlush(self, record):
        """
        Should the handler flush its buffer?

        Returns true if the buffer is up to capacity. This method can be
        overridden to implement custom flushing strategies.
        """
        return (len(self.buffer) >= self.capacity)

    def emit(self, record):
        """
        Emit a record.

        Append the record. If shouldFlush() tells us to, call flush() to process
        the buffer.
        """
        self.buffer.append(record)
        if self.shouldFlush(record):
            self.flush()

    def flush(self):
        """
        Override to implement custom flushing behaviour.

        This version just zaps the buffer to empty.
        """
        self.buffer = []

    def close(self):
        """
        Close the handler.

        This version just flushes and chains to the parent class' close().
        """
        self.flush()
        logging.Handler.close(self)

class MemoryHandler(BufferingHandler):
    """
    A handler class which buffers logging records in memory, periodically
    flushing them to a target handler. Flushing occurs whenever the buffer
    is full, or when an event of a certain severity or greater is seen.
    """
    def __init__(self, capacity, flushLevel=logging.ERROR, target=None):
        """
        Initialize the handler with the buffer size, the level at which
        flushing should occur and an optional target.

        Note that without a target being set either here or via setTarget(),
        a MemoryHandler is no use to anyone!
        """
        BufferingHandler.__init__(self, capacity)
        self.flushLevel = flushLevel
        self.target = target

    def shouldFlush(self, record):
        """
        Check for buffer full or a record at the flushLevel or higher.
        """
        return (len(self.buffer) >= self.capacity) or \
                (record.levelno >= self.flushLevel)

    def setTarget(self, target):
        """
        Set the target handler for this handler.
        """
        self.target = target

    def flush(self):
        """
        For a MemoryHandler, flushing means just sending the buffered
        records to the target, if there is one. Override if you want
        different behaviour.
        """
        if self.target:
            for record in self.buffer:
                self.target.handle(record)
            self.buffer = []

    def close(self):
        """
        Flush, set the target to None and lose the buffer.
        """
        self.flush()
        self.target = None
        BufferingHandler.close(self)

################################################################################
# Investment logging functionality
################################################################################

LOG_FORMAT = '[ %(levelname)-5s ] %(asctime)-15s: %(message)s'

class LogfileHandler(MemoryHandler):
    def shouldFlush(self, record):
        return False

    @property
    def baseFilename(self):
        return self.target.baseFilename

    def toFile(self):
        with open(self.baseFilename, 'w') as f:
            for record in self.buffer:
                f.write(record.getMessage() + '\n')
        self.buffer = []

    def close(self):
        self.target.acquire()
        self.target.flush()
        self.target.close()
        os.remove(self.baseFilename)

def initialize_log(app_name):
    setattr(logging, 'logfile_name', app_name)

    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    formatter = logging.Formatter(fmt=LOG_FORMAT)

    (temp_handle, temp_path) = tempfile.mkstemp(suffix='.log', prefix='investments_app_')
    file_handler = logging.FileHandler(temp_path, delay=True)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.info("Log file created at: %s" % temp_path)

    logfile_handler = LogfileHandler(1024*10, logging.DEBUG, file_handler)
    logfile_handler.setFormatter(formatter)

    log = logging.getLogger()
    log.addHandler(logfile_handler)

def write_log_to_file():
    log = logging.getLogger()
    logfile_handler = log.handlers[-1]

    logging.info('Writing log to file: %s' % logfile_handler.baseFilename)
    logfile_handler.toFile()