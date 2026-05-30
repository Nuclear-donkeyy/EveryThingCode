from dataclasses import dataclass

@dataclass(frozen=True)
class Course:
    name: str
    minutes: int

courses = [Course("typing", 20), Course("asyncio", 30)]
print(f"total minutes = {sum(course.minutes for course in courses)}")
