import os

import pytest

from src.individual import Student, add_student, find, load_students, save


@pytest.fixture
def test_students():
    """Фикстура для создания списка студентов."""
    return [
        Student("Иванов И.И.", "123", [5, 5, 5, 5, 5]),
        Student("Петров П.П.", "124", [4, 4, 4, 4, 4]),
        Student("Сидоров С.С.", "125", [2, 5, 3, 4, 5]),
    ]


def test_add_student(test_students):
    """Тестируем добавление студента."""
    new_student = Student("Кузнецова А.А.", "126", [5, 5, 5, 5, 5])

    # Добавляем нового студента
    add_student(
        test_students,
        new_student.name,
        new_student.group_number,
        new_student.performance,
    )

    # Проверка, что новый студент был добавлен
    assert len(test_students) == 4
    assert test_students[-1].name == new_student.name
    assert test_students[-1].group_number == new_student.group_number
    assert test_students[-1].performance == new_student.performance


def test_save_students(test_students):
    """Тестируем сохранение студентов в файл."""
    test_file = "test_students.xml"

    # Сохраняем студентов в файл
    save(test_file, test_students)

    # Проверяем, что файл создан
    assert os.path.exists(test_file)

    # Проверяем содержимое файла (парсим XML)
    with open(test_file, "r", encoding="utf-8") as fin:
        content = fin.read()
        assert "<students>" in content  # Проверка тега <students> в файле
        assert "<student>" in content  # Присутствуют ли теги <student>


def test_load_students(test_students):
    """Тестируем загрузку студентов из файла."""
    test_file = "test_students.xml"

    # Сохраняем студентов в файл
    save(test_file, test_students)

    # Загружаем студентов из файла
    loaded_students = load_students(test_file)

    # Проверка, что студенты были загружены правильно
    assert len(loaded_students) == len(test_students)
    for original, loaded in zip(test_students, loaded_students):
        assert original.name == loaded.name
        assert original.group_number == loaded.group_number
        assert original.performance == loaded.performance


def test_find_students_with_failing_grades(test_students):
    """Тестируем поиск студентов с отметкой 2."""
    found_students = find(test_students)

    # Проверка, что студенты с отметкой 2 найдены
    assert len(found_students) == 1
    assert found_students[0].name == "Сидоров С.С."


def test_load_students_invalid_schema():
    """Тестируем обработку ошибок при некорректной схеме XML."""
    # Создаем некорректный файл XML, где данные в performance некорректны
    invalid_data = """
    <students>
        <student>
            <name>Иванов И.И.</name>
            <group_number>123</group_number>
            <performance>5,5,5,abc</performance>
        </student>
        <student>
            <name>Петров П.П.</name>
            <group_number>124</group_number>
            <performance>4,xyz,4,4</performance>
        </student>
    </students>
    """
    test_file = "test_students_invalid.xml"
    with open(test_file, "w", encoding="utf-8") as fout:
        fout.write(invalid_data)

    # Проверка попытки загрузить данные с ошибкой возникнет исключение
    with pytest.raises(ValueError, match="Некорректные данные"):
        load_students(test_file)
