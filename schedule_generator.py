import random
import math
import re

# -------------------------
# Tetapan nama subjek
# -------------------------
kategori1_subjects = [
    "Bahasa Melayu", "English", "Chinese", "Science", "Mathematics",
    "Sejarah", "Geografi", "Pendidikan Moral", "Pendidikan Seni Visual",
    "Asas Sains Komputer", "Pendidikan Jasmani dan Kesihatan"
]

subject_options = {
    1: "Bahasa Melayu",
    2: "English",
    3: "Chinese",
    4: "Science",
    5: "Mathematics",
    6: "Sejarah",
    7: "Geografi",
    8: "Account",
    9: "Pendidikan Seni Visual",
    10: "Sains Komputer",
    11: "Pendidikan Moral",
    12: "Pendidikan Islam",
    13: "Additional Mathematics",
    14: "Physics",
    15: "Biologi",
    16: "Chemistry"
}

def _norm(s):
    return re.sub(r'\s+', '', s.strip().lower())

_all_canonical = []
for s in kategori1_subjects:
    if s not in _all_canonical:
        _all_canonical.append(s)
for s in subject_options.values():
    if s not in _all_canonical:
        _all_canonical.append(s)
_norm_to_canon = { _norm(s): s for s in _all_canonical }

def parse_chosen_input(chosen_input):
    if not chosen_input or not chosen_input.strip():
        return []
    s = chosen_input.strip()
    for sep in ['，', '、', ';', '；', '/', '\\', '|', ':']:
        s = s.replace(sep, ',')
    s = re.sub(r',+', ',', s).strip(',')
    if ',' in s:
        tokens = [t.strip() for t in s.split(',') if t.strip()]
    else:
        parts = [p for p in re.split(r'\s+', s) if p]
        if parts and all(re.fullmatch(r'\d+', p) for p in parts):
            tokens = parts
        else:
            tokens = [s]

    chosen, seen = [], set()
    for tok in tokens:
        if tok.isdigit():
            n = int(tok)
            if n in subject_options:
                name = subject_options[n]
                if name not in seen:
                    chosen.append(name); seen.add(name)
            continue
        kn = _norm(tok)
        if kn in _norm_to_canon:
            name = _norm_to_canon[kn]
            if name not in seen:
                chosen.append(name); seen.add(name)
            continue
    return chosen

def generate_weekly_schedule(subjects, difficulties, daily_hours, subjects_per_day):
    if not subjects:
        raise ValueError("Tiada subjek diberikan.")
    minutes_per_day = int(round(float(daily_hours) * 60))
    total_slots = 7 * subjects_per_day
    if total_slots < len(subjects):
        subjects_per_day = math.ceil(len(subjects) / 7)
        total_slots = 7 * subjects_per_day

    days = [[] for _ in range(7)]
    order = subjects.copy()
    random.shuffle(order)
    for subj in order:
        min_len = min(len(d) for d in days)
        for i in range(7):
            if len(days[i]) == min_len and len(days[i]) < subjects_per_day:
                days[i].append(subj)
                break
    for i in range(7):
        while len(days[i]) < subjects_per_day:
            avail = [s for s in subjects if s not in days[i]]
            pool = avail if avail else subjects
            weights = [difficulties.get(s, 1) for s in pool]
            chosen = random.choices(pool, weights=weights, k=1)[0]
            days[i].append(chosen)

    weekly_plan = {}
    for i, day in enumerate(days):
        weights = [difficulties.get(s, 1) for s in day]
        total_w = sum(weights)
        day_minutes = [0]*len(day)
        if total_w <= 0:
            base = minutes_per_day // len(day)
            day_minutes = [base]*len(day)
            rem = minutes_per_day - sum(day_minutes)
            for j in range(rem):
                day_minutes[j % len(day)] += 1
        else:
            for j, s in enumerate(day):
                day_minutes[j] = int(round(minutes_per_day * (difficulties.get(s,1) / total_w)))
            diff = minutes_per_day - sum(day_minutes)
            if diff != 0:
                max_idx = max(range(len(day)), key=lambda j: weights[j])
                day_minutes[max_idx] += diff
        day_agg = {}
        for idx, s in enumerate(day):
            day_agg[s] = day_agg.get(s, 0) + day_minutes[idx]
        formatted = {}
        for s, mins in day_agg.items():
            hours = round(mins / 60, 2)
            formatted[s] = {"minutes": mins, "hours": hours}
        weekly_plan[f"Hari {i+1}"] = formatted
    return weekly_plan
