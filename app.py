from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

STUDENT_CSV = 'student.csv'

@app.route('/debug_csv_data')
def debug_csv_data():
    student_list = []
    with open(STUDENT_CSV, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        student_list = list(reader)

    return f"Student Data: {student_list}"

def get_next_id():
    try:
        with open(STUDENT_CSV, "r") as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                last_id = int(reader[-1][0])  # Get last ID from the file
                return last_id + 1
    except:
        return 1
    return 1

def allocate_hostel(gender, nationality):
    if gender == 'Female':
        return 'Hostel A: Indian Girls' if nationality == 'Indian' else 'Hostel B: International Girls'
    elif gender == 'Male':
        return 'Hostel C: International Boys' if nationality == 'International' else 'Hostel D: Indian Boys'
    return 'Not Assigned'

@app.route('/add_students', methods=['POST'])
def add_students():

    student_id = get_next_id()
    gender = request.form['gender']
    nationality = request.form['nationality']
    allocated_hostel = allocate_hostel(gender, nationality)

    data = [
        student_id,
        request.form['name'],
        request.form['gr_no'],
        request.form['age'],
        request.form['local_g_nm'],
        request.form['local_g_ph'],
        gender,
        nationality,
        request.form['contact'],
        request.form['address'],
        request.form['sem'],
        request.form['course'],
        request.form['blood_group'],
        request.form['email'],
        request.form['allergies'],
        allocated_hostel

    ]

    with open(STUDENT_CSV, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

    return redirect(url_for('students'))

@app.route('/students', methods=['GET', 'POST'])
def students():
    query = request.args.get('search', '').lower()
    student_list = []

    with open(STUDENT_CSV, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if query:
                if any(query in str(item).lower() for item in row):
                    student_list.append(row)
            else:
                student_list.append(row)

    return render_template('view_students.html', students=student_list, search=query)


@app.route('/delete/<id>')
def delete_student(id):
    students_list = []
    with open(STUDENT_CSV, "r") as file:
        reader = csv.reader(file)
        students_list = [row for row in reader if row[0] != id]

    with open(STUDENT_CSV, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(students_list)

    return redirect(url_for('students'))

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_student(id):
    students_list = []
    with open(STUDENT_CSV, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        students_list = [row for row in reader]

    student_data = None
    for student in students_list:
        if student[0] == id:
            student_data = student
            break
            
    if request.method == 'POST':
        gender = request.form['gender']
        nationality = request.form['nationality']
        allocated_hostel = allocate_hostel(gender, nationality)  # Ensure hostel assignment

        updated_data = [
            id,
            request.form['name'],
            request.form['gr_no'],
            request.form['age'],
            request.form['guardian'],
            request.form['guardian_phone'],
            gender,
            nationality,
            request.form['contact'],
            request.form['address'],
            request.form['sem'],
            request.form['course'],
            request.form['blood_group'],
            request.form['email'],
            request.form['allergies'],
            allocated_hostel

        ]

        for i, student in enumerate(students_list):
            if student[0] == id:
                students_list[i] = updated_data
                break

        with open(STUDENT_CSV, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(students_list)

        return redirect(url_for('students'))

    return render_template('update.html', student=student_data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)