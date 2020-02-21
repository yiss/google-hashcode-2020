import os
from dataclasses import dataclass
from typing import List


@dataclass
class Book:
    id: int
    score: int


@dataclass(init=False)
class Library:
    id: int
    nb_books: int
    signup_time: int
    books_per_days: int
    books: List[Book]
    lib_score: int = 0

    def total_time(self) -> float:
        return self.signup_time + (len(self.books) / self.books_per_days)

    def weight(self):
        return self.lib_score / self.total_time()


@dataclass(init=False)
class Problem:
    nb_books: int
    nb_libs: int
    max_days: int
    libs: List[Library]


def solve(filename):
    print(f'solving {filename}')
    problem = read_input_file(filename)
    problem.libs.sort(key=lambda l: l.weight(), reverse=True)
    lib_sending: List[Library] = []
    i = 0
    days = problem.max_days
    while days >= 0 and i < len(problem.libs):
        if days - problem.libs[i].signup_time >= 0:
            lib_sending.append(problem.libs[i])
            days -= problem.libs[i].signup_time
        i += 1
    print(f'size : {len(lib_sending)}')
    write_output_file(filename, lib_sending)


def get_input_filenames() -> List[str]:
    input_files: List[str] = []
    for file in os.listdir('./input'):
        if file.endswith('.txt'):
            input_files.append(file)
    for filename in input_files:
        solve(filename)
    return input_files


def read_input_file(filename) -> Problem:
    problem = Problem()
    with open(f'./input/{filename}') as file:
        line = file.readline().split(' ')
        problem.nb_books = int(line[0])
        problem.nb_libs = int(line[1])
        problem.max_days = int(line[2])
        problem.libs = []
        line = file.readline().split(' ')
        books = [Book(i, int(line[i])) for i in range(len(line))]
        for i in range(problem.nb_libs):
            lib = Library()
            line = file.readline().split(' ')
            lib.id = i
            lib.nb_books = int(line[0])
            lib.signup_time = int(line[1])
            lib.books_per_days = int(line[2])
            line = file.readline().split(' ')
            lib.books = []
            for j in range(lib.nb_books):
                b = books[int(line[j])]
                lib.books.append(b)
                lib.lib_score += b.score
            # lib.books.sort(key=lambda bo: bo.score, reverse=True)
            problem.libs.append(lib)

    return problem


def write_output_file(filename: str, libs: List[Library]) -> None:
    file = open(f'./output/{filename}', 'w')
    file.write(f'{len(libs)}\n')
    for lib in libs:
        file.write(f'{lib.id} {lib.nb_books}\n')
        file.write(' '.join(map(lambda b: str(b.id), lib.books)))
        file.write('\n')


# def write_output_files(content, filename)

if __name__ == '__main__':
    # a = [5, 8, 9, 1, 2, 3]
    # a.sort(reverse=True)
    # print(a)
    get_input_filenames()
