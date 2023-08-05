from .temporal import Temporal


class TemporalInstants(Temporal):
    """
    Abstract class for representing temporal values of instant set or
    sequence duration.
    """
    __slots__ = ['_instantList']

    @property
    def getValues(self):
        """
        List of distinct values taken by the temporal value.
        """
        return list(dict.fromkeys([inst._value for inst in self._instantList]))

    @property
    def startValue(self):
        """
        Start value.
        """
        return self._instantList[0]._value

    @property
    def endValue(self):
        """
        End value.
        """
        return self._instantList[-1]._value

    @property
    def minValue(self):
        """
        Minimum value.
        """
        return min(inst._value for inst in self._instantList)

    @property
    def maxValue(self):
        """
        Maximum value.
        """
        return max(inst._value for inst in self._instantList)

    @property
    def numInstants(self):
        """
        Number of instants.
        """
        return len(self._instantList)

    @property
    def startInstant(self):
        """
        Start instant.
        """
        return self._instantList[0]

    @property
    def endInstant(self):
        """
        End instant.
        """
        return self._instantList[-1]

    def instantN(self, n):
        """
        N-th instant.
        """
        # 1-based
        if 1 <= n <= len(self._instantList):
            return self._instantList[n - 1]
        else:
            raise Exception("ERROR: Out of range")

    @property
    def instants(self):
        """
        List of instants.
        """
        return self._instantList

    @property
    def numTimestamps(self):
        """
        Number of timestamps.
        """
        return len(self._instantList)

    @property
    def startTimestamp(self):
        """
        Start timestamp.
        """
        return self._instantList[0]._time

    @property
    def endTimestamp(self):
        """
        End timestamp.
        """
        return self._instantList[-1]._time

    def timestampN(self, n):
        """
        N-th timestamp.
        """
        # 1-based
        if 1 <= n <= len(self._instantList):
            return self._instantList[n - 1]._time
        else:
            raise Exception("ERROR: Out of range")

    @property
    def timestamps(self):
        """
        List of timestamps.
        """
        return [instant._time for instant in self._instantList]

    def shift(self, timedelta):
        """
        Shift the temporal value by a time interval.
        """
        for inst in self._instantList:
            inst._time += timedelta
        return self

    def __str__(self):
        return "{}".format(', '.join('{}'.format(instant.__str__().replace("'", ""))
            for instant in self._instantList))
