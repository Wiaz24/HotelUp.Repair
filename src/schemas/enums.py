from enum import Enum

class RepairType(str, Enum):
    damage = "damage"
    malfunction = "malfunction"
    undefined = "undefined"
    not_detected = "not_detected"
    
class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"