from pylogix import PLC
import os


port     = 5432,
host     = "RHKEN702",
database = "P01GES",
user     = "uwipuser",
password = "P@ss1m1@n"


commSeq= PLC()
commSeq.IPAddress= "10.212.49.130"
commSeq.ProcessorSlot = 1