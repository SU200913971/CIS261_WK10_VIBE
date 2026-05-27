#!/usr/bin/env python3
"""
Student Grade Calculator

Features:
- Manage student records with three test scores
- Calculate average and letter grade
- Display formatted table and class statistics
- Search students by name (case-insensitive)
- Save/load pipe-delimited file `student_grades.txt`
- Use ESC at the main menu to exit

Data structure: Student class (Option B)
"""
import os
import sys
from typing import List, Optional, Tuple


FILEPATH = "student_grades.txt"


class Student:
    def __init__(self, name: str, sid: str, test1: float, test2: float, test3: float):
        self.name = name
        self.id = sid
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)

    @property
    def average(self) -> float:
        return round((self.test1 + self.test2 + self.test3) / 3.0, 2)

    @property
    def grade(self) -> str:
        avg = self.average
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def to_pipe(self) -> str:
        return f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"

    @staticmethod
    def from_pipe(line: str):
        parts = line.strip().split("|")
        if len(parts) < 7:
            raise ValueError("Invalid record format")
        name, sid, t1, t2, t3, avg, grade = parts[:7]
        return Student(name=name, sid=sid, test1=float(t1), test2=float(t2), test3=float(t3))


def load_records(filepath: str = FILEPATH) -> List[Student]:
    students: List[Student] = []
    if not os.path.exists(filepath):
        return students
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    s = Student.from_pipe(line)
                    students.append(s)
                except Exception:
                    # skip malformed lines
                    continue
    except Exception as e:
        print(f"Error loading file: {e}")
    return students


def save_records(students: List[Student], filepath: str = FILEPATH) -> None:
    try:
        with open(filepath, "w") as f:
            for s in students:
                f.write(s.to_pipe())
    except Exception as e:
        print(f"Error saving file: {e}")


def add_student_interactive(students: List[Student]) -> None:
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty")
        return
    sid = input("Enter student ID: ").strip()
    if not sid:
        print("ID cannot be empty")
        return
    try:
        t1 = float(input("Test 1 score: ").strip())
        t2 = float(input("Test 2 score: ").strip())
        t3 = float(input("Test 3 score: ").strip())
    except ValueError:
        print("Invalid score entered. Scores must be numbers.")
        return
    students.append(Student(name=name, sid=sid, test1=t1, test2=t2, test3=t3))
    print(f"Student {name} added.")


def display_students_table(students: List[Student]) -> None:
    if not students:
        print("No students to display.")
        return
    widths = (20, 10, 8, 8, 8, 9, 6)
    header = ("Name", "ID", "Test1", "Test2", "Test3", "Average", "Grade")
    fmt = "".join(f"{{:<{w}}} " for w in widths)
    print(fmt.format(*header))
    print("-" * (sum(widths) + len(widths)))
    for s in students:
        print(fmt.format(
            s.name[:widths[0]-1], s.id[:widths[1]-1],
            f"{s.test1:.2f}", f"{s.test2:.2f}", f"{s.test3:.2f}",
            f"{s.average:.2f}", s.grade
        ))


def class_statistics(students: List[Student]) -> Optional[Tuple[float, float, float]]:
    if not students:
        return None
    avgs = [s.average for s in students]
    highest = max(avgs)
    lowest = min(avgs)
    class_avg = round(sum(avgs) / len(avgs), 2)
    return highest, lowest, class_avg


def search_by_name(students: List[Student], query: str) -> List[Student]:
    q = query.strip().lower()
    return [s for s in students if q in s.name.lower()]


def read_single_key() -> str:
    """Read a single character from stdin without requiring Enter. Returns the char or empty string on failure."""
    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
    except Exception:
        # Fallback: ask user to type and press Enter
        try:
            v = input().strip()
            return v[0] if v else ""
        except Exception:
            return ""


def main():
    print("Student Grade Calculator (press ESC at menu to exit)")
    students = load_records()
    while True:
        print("\nMenu:")
        print("1) Add new student record")
        print("2) Display all students")
        print("3) Class statistics")
        print("4) Search student by name")
        print("5) Save records")
        print("Press ESC to exit")
        print("Choose an option (1-5):", end=" ", flush=True)
        ch = read_single_key()
        if ch == "\x1b":
            print("\nExiting and saving records...")
            save_records(students)
            break
        print(ch)
        if ch == "1":
            add_student_interactive(students)
        elif ch == "2":
            display_students_table(students)
        elif ch == "3":
            stats = class_statistics(students)
            if not stats:
                print("No students available for statistics.")
            else:
                high, low, avg = stats
                print(f"Highest average: {high:.2f}")
                print(f"Lowest average: {low:.2f}")
                print(f"Class average: {avg:.2f}")
        elif ch == "4":
            query = input("Enter name to search: ").strip()
            results = search_by_name(students, query)
            if not results:
                print("No matching students found.")
            else:
                display_students_table(results)
        elif ch == "5":
            save_records(students)
            print("Records saved.")
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
