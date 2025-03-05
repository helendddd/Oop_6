#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import xml.etree.ElementTree as ET

# Конфигурация логгера
logging.basicConfig(
    filename="students_program.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Student:
    """Класс для представления студента."""

    def __init__(self, name, group_number, performance):
        self.name = name
        self.group_number = group_number
        self.performance = performance

    def to_dict(self):
        """Конвертировать объект Student в словарь."""
        return {
            "name": self.name,
            "group_number": self.group_number,
            "performance": self.performance,
        }

    @staticmethod
    def from_dict(data):
        """Создать объект Student из словаря."""
        return Student(
            name=data["name"],
            group_number=data["group_number"],
            performance=data["performance"],
        )

    def to_xml(self):
        """Конвертировать объект Student в XML элемент."""
        student_element = ET.Element("student")
        name_element = ET.SubElement(student_element, "name")
        name_element.text = self.name
        group_element = ET.SubElement(student_element, "group_number")
        group_element.text = self.group_number
        performance_element = ET.SubElement(student_element, "performance")
        performance_element.text = ",".join(map(str, self.performance))
        return student_element

    @staticmethod
    def from_xml(student_element):
        """Создать объект Student из XML элемента."""
        name = student_element.find("name").text
        group_number = student_element.find("group_number").text  # Это строка
        performance_text = student_element.find("performance").text

        # Преобразуем строки в список чисел
        try:
            performance = list(map(int, performance_text.split(",")))
        except ValueError:
            raise ValueError("Некорректные данные успеваемости")

        return Student(name, group_number, performance)


def add_student(students, name, group_number, performance):
    """Функция для добавления нового ученика в список."""
    try:
        student = Student(name, group_number, performance)
        students.append(student)
        logging.info(f"Добавлен новый студент: {name}, Группа: {group_number}")
    except Exception as e:
        logging.error(f"Ошибка при добавлении студента: {e}")
        raise
    return students


def list_students(students):
    """Функция для вывода списка студентов."""
    try:
        if students:
            line = "+-{}-+-{}-+-{}-+-{}-+".format(
                "-" * 4, "-" * 30, "-" * 20, "-" * 20
            )
            print(line)

            print(
                "| {:^4} | {:^30} | {:^20} | {:^20} |".format(
                    "No", "Фамилия и инициалы", "Номер группы", "Успеваемость"
                )
            )

            print(line)

            for idx, student in enumerate(students, 1):
                print(
                    "| {:>4} | {:<30} | {:<20} | {:>20} |".format(
                        idx,
                        student.name,
                        student.group_number,
                        ", ".join(map(str, student.performance)),
                    )
                )
            print(line)
        else:
            print("Список студентов пуст.")
    except Exception as e:
        logging.error(f"Ошибка при выводе списка студентов: {e}")
        raise


def find(students):
    """Функция для поиска студентов с отметкой 2."""
    try:
        found = [student for student in students if 2 in student.performance]
        return found
    except Exception as e:
        logging.error(f"Ошибка при поиске студентов: {e}")
        raise


def save(file_name, students):
    """Сохранить всех студентов в XML файл."""
    try:
        root = ET.Element("students")
        for student in students:
            root.append(student.to_xml())

        tree = ET.ElementTree(root)
        tree.write(file_name, encoding="utf-8", xml_declaration=True)
        logging.info(f"Данные студентов сохранены в файл: {file_name}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в файл: {e}")
        raise


def load_students(file_name):
    """Загрузить всех студентов из XML файла."""
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()

        if root.tag != "students":
            raise ValueError("Неверный корневой элемент XML")

        students = []
        for student_element in root.findall("student"):
            try:
                student = Student.from_xml(student_element)
                students.append(student)
            except ValueError as e:
                logging.error(f"Ошибка в данных студента: {e}")
                raise ValueError(f"Ошибка в данных студента: {e}")

        logging.info(f"Данные успешно загружены из файла: {file_name}")
        return students
    except Exception as e:
        logging.error(f"Ошибка при загрузке данных из файла: {e}")
        raise
