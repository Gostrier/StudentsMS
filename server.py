"""Web UI server for the Student Management System.

Uses only the Python standard library, so nothing extra to install.
Run:  python server.py   (then open http://127.0.0.1:8000)
"""
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from grade_system import GradeSystem
from student import Student
from student_manager import StudentManager

BASE_DIR = Path(__file__).resolve().parent
PAGE = BASE_DIR / "index.html"
HOST, PORT = "127.0.0.1", 8000

manager = StudentManager(str(BASE_DIR / "students.json"))
lock = threading.Lock()


def student_json(s):
    data = s.to_dict()
    data["grade"] = GradeSystem.mark_to_grade(s.average_mark)
    return data


def find_or_fail(admission_number):
    s = manager.find_student(admission_number)
    if s is None:
        raise KeyError("Student not found.")
    return s


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet

    def _send(self, status, body, content_type="application/json"):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            raise ValueError("Invalid request data.")

    def _route(self, method):
        url = urlparse(self.path)
        sid = parse_qs(url.query).get("id", [""])[0]
        path = url.path

        if method == "GET" and path == "/":
            return 200, PAGE.read_bytes(), "text/html; charset=utf-8"

        if method == "GET" and path == "/api/students":
            return 200, [student_json(s) for s in manager.all_students()]

        if method == "POST" and path == "/api/students":
            d = self._body()
            s = Student(
                d.get("admission_number", ""), d.get("name", ""),
                d.get("programme", ""), d.get("year_of_study", 1),
                d.get("average_mark", 0),
            )
            manager.add_student(s)
            return 201, student_json(s)

        if method == "PUT" and path == "/api/student":
            s = find_or_fail(sid)
            d = self._body()
            # Validate everything first so a bad value changes nothing
            check = Student(
                s.admission_number, d.get("name", s.name),
                d.get("programme", s.programme),
                d.get("year_of_study", s.year_of_study),
                d.get("average_mark", s.average_mark),
            )
            s.name = check.name
            s.programme = check.programme
            s.year_of_study = check.year_of_study
            s.average_mark = check.average_mark
            manager.save()
            return 200, student_json(s)

        if method == "DELETE" and path == "/api/student":
            manager.remove_student(sid)
            return 200, {"ok": True}

        if method == "POST" and path == "/api/student/registration":
            s = find_or_fail(sid)
            if bool(self._body().get("registered")):
                s.register()
            else:
                s.deregister()
            manager.save()
            return 200, student_json(s)

        if method == "GET" and path == "/api/stats":
            students = manager.all_students()
            registered = sum(1 for s in students if s.registered)
            return 200, {
                "total": len(students),
                "registered": registered,
                "not_registered": len(students) - registered,
                "class_average": manager.class_average(),
            }

        if method == "GET" and path == "/api/grades":
            return 200, GradeSystem.GRADE_POINTS

        if method == "POST" and path == "/api/gpa":
            grades = self._body().get("grades", [])
            if not isinstance(grades, list) or not all(isinstance(g, str) for g in grades):
                raise ValueError("Grades must be a list of letters.")
            return 200, {"gpa": GradeSystem.calculate_gpa(grades)}

        return None

    def _handle(self, method):
        try:
            with lock:
                result = self._route(method)
            if result is None:
                self._send(404, {"error": "Not found."})
            else:
                self._send(*result)
        except (ValueError, TypeError) as e:
            self._send(400, {"error": str(e)})
        except KeyError as e:
            self._send(404, {"error": str(e.args[0])})
        except Exception as e:  # last resort
            self._send(500, {"error": f"Server error: {e}"})

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def do_PUT(self):
        self._handle("PUT")

    def do_DELETE(self):
        self._handle("DELETE")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Student system running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
