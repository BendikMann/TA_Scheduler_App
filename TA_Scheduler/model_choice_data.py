class CourseChoices:
    SPRING = 'spr'
    FALL = 'fal'
    WINTERIM = 'win'
    SUMMER = 'sum'

    # TODO Make term names (Spring semester is different then fall semsester)
    TERM_NAMES = [
        (SPRING, 'Spring'),
        (FALL, 'fall'),
        (WINTERIM, 'winterim'),
        (SUMMER, 'summer')
    ]

    YEAR2022 = '2022'
    YEAR2023 = '2023'
    YEAR2024 = '2024'

    TERM_YEAR = [
        (YEAR2022, '2022'),
        (YEAR2023, '2023'),
        (YEAR2024, '2024')
    ]


class SectionChoices:
    LECTURE = 'LEC'
    DISCUSSION = 'DIS'
    LAB = 'LAB'

    SECTION_CHOICES = [
        (LECTURE, 'Lecture'),
        (DISCUSSION, 'Discussion'),
        (LAB, 'Lab')
    ]
