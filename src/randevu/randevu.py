"""
The official Python implementation of the RANDEVU algorithm

More information is available on [GITHUB](https://github.com/TypicalHog/randevu-py)

Example:
```python
from datetime import datetime, timezone
from randevu import rdv, rdvt

object = "THE_SIMPSONS"
date = datetime.now(timezone.utc)
rdv_value = rdv(object, date)
rdvt_value = rdvt(0, object, date)

print(f"Object {object} has RDV{rdv_value} today with RDVT0 at {rdvt_value}")
```
"""

from blake3 import blake3
from datetime import datetime, timezone

def create_key(date: datetime, rank: int=None) -> bytearray:
    """
    Returns the 32-byte KEY `bytearray` created from a given DATE (UTC) `datetime` and an optional RANK `int | None`
    
    :param date: DATE
    :type date: datetime
    :param rank: RANK (optional)
    :type rank: int or None
    :return: KEY
    :rtype: bytearray
    """
    if date.tzinfo != timezone.utc:
        raise ValueError("Date must be in UTC timezone (tzinfo=timezone.utc)")
    
    key = bytearray(32)
    
    # Convert the date into a string, ISO 8601 formatted (YYYY-MM-DD)
    key_str = date.strftime('%Y-%m-%d')
    
    # If a rank is provided, write it into the key_str after the date, separated by an '_'
    if rank != None:
        key_str += '_' + str(rank)
    
    # Write the key_str into the key
    key[:len(key_str)] = key_str.encode()
    
    return key

def rdv(object: str, date: datetime) -> int:
    """
    Returns the RDV value `int` for an OBJECT `str` on a specific DATE (UTC) `datetime`

    **RDV = number of leading zero bits in blake3::keyed_hash(key: DATE, data: OBJECT)**
    
    :param object: OBJECT
    :type object: str
    :param date: DATE
    :type date: datetime
    :return: RDV
    :rtype: int
    """
    hash = blake3(object.encode(), key=create_key(date)).digest()

    # Count the number of leading zero bits in the hash
    rdv_value = 0
    for byte in hash:
        if byte == 0:
            rdv_value += 8
        else:
            rdv_value += bin(byte)[2:].zfill(8).find('1')
            break

    return rdv_value

def rdvt(rank: int, object: str, date: datetime) -> datetime:
    """
    Returns the RDVT time (UTC) `datetime` of a given RANK `int` for an OBJECT `str` on a specific DATE (UTC) `datetime`
    
    :param rank: RANK
    :type rank: int
    :param object: OBJECT
    :type object: str
    :param date: DATE
    :type date: datetime
    :return: RDVT
    :rtype: datetime
    """
    hash = blake3(object.encode(), key=create_key(date, rank)).digest()

    # Calculate the time using bits from the hash
    total = 0.0
    increment = 12.0 * 60.0 * 60.0 * 1_000_000.0 # 12h in microseconds
    for i, byte in enumerate(hash):
        for j in reversed(range(8)):
            bit = (byte >> j) & 1
            if bit == 1:
                total += increment
            increment /= 2.0
        # Stop once increments become too small to affect the total
        if i > 3 and (2.0 * increment) < (1.0 - total % 1):
            break
    
    # Construct the RDVT time from total
    seconds, microseconds = divmod(int(total), 10**6)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    rdvt_time = datetime(
        year=date.year,
        month=date.month,
        day=date.day,
        hour=hours,
        minute=minutes,
        second=seconds,
        microsecond=microseconds,
        tzinfo=timezone.utc
    )
    
    return rdvt_time
