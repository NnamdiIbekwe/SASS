from sqlalchemy import Enum as SqlEnum
import enum


class AssignmentStatus(str, enum.Enum):
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    GRADED = "Graded"

