import datetime

def is_weekend(day):
    return datetime.weekday in [5, 6]

def calculate_work_and_weekend_days(start_date, end_date):
    current_date = start_date
    weekend_days, work_days = 0, 0
    while current_date <= end_date:
        if is_weekend(current_date):
            weekend_days += 1
        else:
            work_days += 1
        current_date += datetime.timedelta(days=1)
    return work_days, weekend_days

def validate_vacation_schedule(existing_schedules, new_schedule):
    for start, end in new_schedule['periods']:
        if start > end:
            raise ValueError(f'Ошибка валидации: Дата начала отпуска {start.strftime('%d.%m.%Y')} позже даты конца отпуска {end.strftime('%d.%m.%Y')}')
    
    sorted_periods = sorted(new_schedule['periods'])
    for i in range(len(new_schedule) - 1):
        start1, end1 = sorted_periods[i]
        start2, end2 = sorted_periods[i+1]
        if start2 <= end1:
            raise ValueError(f'Ошибка валидации: Даты отпуска {start1.strftime('%d.%m.%Y')-end1.strftime('%d.%m.%Y')} и {start2.strftime('%d.%m.%Y')-end2.strftime('%d.%m.%Y')} пересекаются')
    
    total_days = 0
    has_14_days = False

    for start, end in new_schedule['periods']:
        duration = (end - start).days + 1
        total_days += duration

        work_days, weekend_days = calculate_work_and_weekend_days(start, end)
        if weekend_days < 2 or work_days < 1:
            raise ValueError(f'Ошибка валидации: Период отпуска {start.strftime('%d.%m.%Y')-end.strftime('%d.%m.%Y')} должен включать хотя бы 2 выходных дня и 1 рабочий')
        
        if duration == 14:
            has_14_days = True
        
    if total_days < 28:
        raise ValueError('Ошибка валидации: Сумма отпусков должна быть равна 28 дням')
        
    if not has_14_days:
        raise ValueError('Ошибка валидации: В графике отпусков должен быть, по крайне мере, один 14-ти дневный период')
        
    for existing_schedule in existing_schedules:
        if existing_schedule['employee_id'] == new_schedule['employee_id']:
            continue
        
        for existing_start, existing_end in existing_schedule['periods']:
            for new_start, new_end in new_schedule['periods']:
                if max(existing_start, new_start) <= min(existing_end, new_end):
                    raise ValueError(f"Ошибка валидации: Новый график отпусков пересекается с существующим графиком сотрудника {existing_schedule['employee_name']} в период с {max(existing_start, new_start).strftime('%d.%m.%Y')} по {min(existing_end, new_end).strftime('%d.%m.%Y')}.")

    return True