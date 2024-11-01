from .line import Line

# Points table to map a grade to a point value.
POINTS_TABLE = {
    '1': 1.0,
    '2': 1.05,
    '3': 1.1,
    '4': 1.15,
    '5': 1.2,
    'Hyv.': 1.1,
    'HT': 1.1,
    'TT': 1.05,
    'ET': 1.2
}


def pointer_until_startswith(pointer, s):
    """
    Move the pointer forward until it reaches a line that starts with the given string.
    :param pointer: The current pointer.
    :param s: string to search for
    :return: The pointer after moving forward.
    """
    while not pointer.value.startswith(s):
        pointer = pointer.next_line
    return pointer


def irrelevant_matches(s: str):
    """
    Check if the line is irrelevant based on several checks.
    :param s: the line as a string
    :return: boolean
    """
    return (s.startswith('Suorituksen nimi ja koodi') or
            s.startswith('Ei suorituksia') or
            s.startswith('Opintokokonaisuudet') or
            s.startswith('Opintojaksot') or
            ' PERUSOPINNOT ' in s or
            ' KANDIOHJELMA' in s or
            'PATOLOGIA (ELK-122)' in s or
            'MATEMATIIKAN, FYSIIKAN JA KEMIAN OPETTAJAN' in s or
            'JULKISOIKEUS (ON-J2000)' in s or
            'OIKEUSNOTAARIN KOULUTUSOHJELMA' in s or
            'TIETOJENKÄSITTELYTIETEEN KOULUTUSOHJELMA (ALEMPI)' in s or
            'USKONTOTIEDE II, OPINTOKOKONAISUUS' in s or
            len(s) < 14 or
            len(s.strip().split('   ')) < 5)


def skip_irrelevant_lines(pointer: Line):
    """
    Moves the pointer forward until it reaches a relevant line.
    :param pointer: The current pointer.
    :return: The same pointer after moving forward.
    """
    while irrelevant_matches(pointer.value):
        if pointer.value.startswith("Kaikki opintojaksot yhteensä"):
            return pointer
        pointer = pointer.next_line
    return pointer


def split_potential_course_line(s):
    """
    Split a line into parts that are separated by three spaces.
    This results an array of parts forming a potential course line.
    :param s: A string that may contain a course line.
    :return: list of strings
    """
    parts = s.split('   ')
    parts = [item.strip() for item in parts if len(item.strip()) > 0]
    return parts


def check_indents(pointer):
    """
    Check if the next line is a continuation of the current course.
    :param pointer: Pointer to the current line.
    """
    leading_spaces = len(pointer.value) - len(pointer.value.lstrip(' '))
    next_pointer = pointer.next_line.next_line
    while irrelevant_matches(next_pointer.value):
        if next_pointer.value.startswith('Kaikki opintojaksot yhteensä'):
            return pointer
        next_pointer = next_pointer.next_line

    next_leading_spaces = len(next_pointer.value) - len(next_pointer.value.lstrip(' '))

    if next_leading_spaces - leading_spaces == 3:
        return next_pointer

    return pointer


class Document:
    """
    A class for parsing a document containing student information and course information.
    """

    def __init__(self, content):
        self.credits = 0
        self.courses = []
        self.points = 0
        self.first_names = ""
        self.last_name = ""
        self.student_number = ""
        self.birth_time = ""
        self.total_credits_check = 0

        if len(content) < 2:
            return

        self.first_line = Line(content[0])

        current_line = self.first_line

        for i in range(1, len(content)):
            old_line = current_line
            current_line.next_line = Line(content[i])
            current_line = current_line.next_line
            current_line.prev_line = old_line

    def parse_basics(self, pointer: Line):
        """
        Parse the student basic information from the document.
        :param pointer: Pointer to the first line of the document.
        """
        pointer = pointer_until_startswith(pointer, 'Etunimet')
        self.first_names = " ".join(pointer.value.split(" ")[1:]).strip()

        pointer = pointer_until_startswith(pointer, 'Sukunimi')
        self.last_name = " ".join(pointer.value.split(" ")[1:]).strip()

        pointer = pointer_until_startswith(pointer, 'Opiskelijanumero')
        self.student_number = " ".join(pointer.value.split(" ")[1:]).strip()

        pointer = pointer_until_startswith(pointer, 'Syntymäaika')
        self.birth_time = " ".join(pointer.value.split(" ")[1:]).strip()
        return pointer.next_line

    def add_course(self, arr):
        """
        Add a course to the courses list. Does nothing if the line is not in a valid format.
        :param arr: An array of the following format:
            [name, credits, grade, date] or [name, credits, language, grade, date]
        """
        if len(arr) == 4:
            self.courses.append({
                "name": arr[0],
                "credits": float(arr[1][:-3]),
                "grade": arr[2],
                "date": arr[3]
            })
        else:
            self.courses.append({
                "name": arr[0],
                "credits": float(arr[1][:-3]),
                "language": arr[2],
                "grade": arr[3],
                "date": arr[4]
            })

    def parse_courses(self, pointer: Line):
        """
        Parse the document from the point where the courses start.
        :param pointer: Pointer to a document line after the basics part.
        """
        pointer = pointer_until_startswith(pointer, 'Suorituksen nimi ja koodi')
        while True:
            pointer = skip_irrelevant_lines(pointer)
            if pointer.value.startswith("Kaikki opintojaksot yhteensä"):
                self.total_credits_check = float(pointer.value.split(' ')[3])
                return

            pointer = check_indents(pointer)

            cells = split_potential_course_line(pointer.value)
            self.add_course(cells)

            pointer = pointer.next_line

    def parse(self):
        """
        Parse tge document, put the courses in a list and calculate the total credits and points.
        """
        pointer = self.parse_basics(self.first_line)
        self.parse_courses(pointer)

        for course in self.courses:
            self.credits += course['credits']
            self.points += course['credits'] * POINTS_TABLE[course['grade']]

        return

    def get_csv(self):
        """
        Write the parsed data to a csv file.
        :param output_directory:  Output directory path
        """
        first_names = self.first_names.replace(' ', '_')
        filename = f'{self.last_name}_{first_names}.csv'

        content = ""

        content += '"kurssi","opintopisteet","kieli","arvosana","pvm","arvostelupisteet"\n'
        for c in self.courses:
            name = c['name']
            creds = c['credits']
            language = c['language'] if 'language' in c else ''
            if language == '\ufb01':
                language = 'fi'
            grade = c['grade']
            date = c['date']
            content += f'"{name}","{creds}","{language}","{grade}","{date}","{(creds * POINTS_TABLE[grade])}"\n'

        content += f'\n"Opintopisteitä yhteensä","{self.total_credits_check}","Parserin laskemat opintopisteet","{self.credits}","Arvostelupisteet", "{self.points}"'
        return filename, content
