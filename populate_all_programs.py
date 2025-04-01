from run import app, db
from models import Program, Course, ProgramCourse
from sqlalchemy import text
import traceback

def add_program_with_courses(program_name, degree_type, description, courses_data):
    """Helper function to add a program and its courses"""
    # Check if program already exists
    program = Program.query.filter_by(name=program_name, degree_type=degree_type).first()
    
    if not program:
        # Create program if it doesn't exist
        program = Program(
            name=program_name,
            degree_type=degree_type,
            description=description
        )
        # Add program to database
        db.session.add(program)
        db.session.flush()  # Get program ID before committing
    else:
        print(f"Program {program_name} ({degree_type}) already exists, checking for courses...")
        # Check if program has courses
        course_count = ProgramCourse.query.filter_by(program_id=program.id).count()
        if course_count > 0:
            print(f"Program {program_name} ({degree_type}) already has {course_count} courses. Skipping.")
            return program
    
    # Create courses
    all_courses = []
    for semester, courses in courses_data.items():
        for i, course_title in enumerate(courses):
            course_code = f"{program_name[:2].upper()}{degree_type[0]}{semester}{i+1:02d}"
            # Check if course already exists
            existing_course = Course.query.filter_by(code=course_code, title=course_title).first()
            if existing_course:
                all_courses.append(existing_course)
            else:
                course = Course(
                    code=course_code,
                    title=course_title,
                    semester=semester,
                    credits=3 if course_title != "Project" else 6
                )
                all_courses.append(course)
                db.session.add(course)
    
    db.session.flush()
    
    # Associate courses with program
    for course in all_courses:
        # Check if association already exists
        existing_assoc = ProgramCourse.query.filter_by(
            program_id=program.id, 
            course_id=course.id
        ).first()
        
        if not existing_assoc:
            program_course = ProgramCourse(
                program_id=program.id,
                course_id=course.id,
                semester=course.semester
            )
            db.session.add(program_course)
            print(f"Added course {course.title} to program {program_name} ({degree_type})")
    
    return program

def populate_all_programs():
    with app.app_context():
        try:
            # We won't skip population entirely based on program count anymore
            # Instead, we'll check each program individually in add_program_with_courses
            
            # 1. Project Management
            pm_diploma = add_program_with_courses(
                "Project Management",
                "Diploma",
                "Program for project management fundamentals",
                {
                    1: [
                        "Fundamentals of Project Management",
                        "Data Analysis",
                        "Planning and Scheduling",
                        "Organization Structure and Communication",
                        "Decision Making"
                    ],
                    2: [
                        "Budgeting and Cost",
                        "Crises and Risk Management",
                        "Project Control",
                        "Total Quality Management",
                        "Project"
                    ]
                }
            )
            
            pm_master = add_program_with_courses(
                "Project Management",
                "Master",
                "Advanced project management concepts and techniques",
                {
                    1: [
                        "Principles and Methodologies of Scientific Research",
                        "Feasibility Studies of Projects",
                        "Selected Topics in Project Management"
                    ],
                    2: [
                        "Cost-Benefit Analysis and Project Evaluation",
                        "Project Management in Practice",
                        "Project Management Software",
                        "Project"
                    ]
                }
            )
            
            pm_phd = add_program_with_courses(
                "Project Management",
                "PhD",
                "Doctoral studies in project management",
                {
                    1: [
                        "Managing Organizational Behavior",
                        "Strategic Human Resource",
                        "Assessment of Development Projects"
                    ],
                    2: [
                        "Value Analysis for Engineering Project",
                        "Management of Multiple Projects",
                        "Directed Individual Reading (Advanced Topics)"
                    ]
                }
            )
            
            # 2. Operations Research and Decision Support
            ords_diploma = add_program_with_courses(
                "Operations Research and Decision Support",
                "Diploma",
                "Program for operations research and decision support fundamentals",
                {
                    1: [
                        "Operations Research Models and its Applications",
                        "Decision Support Systems",
                        "Business Statistical Analysis",
                        "Project Management and Networks",
                        "Inventory Management"
                    ],
                    2: [
                        "Operations Management",
                        "Modeling and Simulation",
                        "Quality Control",
                        "Operations Research Software",
                        "Project"
                    ]
                }
            )
            
            ords_master = add_program_with_courses(
                "Operations Research and Decision Support",
                "Master",
                "Advanced operations research and decision support concepts",
                {
                    1: [
                        "Principles and Methodologies of Scientific Research",
                        "Advanced Topics in Decision Making",
                        "Forecasting"
                    ],
                    2: [
                        "Scheduling",
                        "Supply Chain Management",
                        "Advanced Operations Research Software",
                        "Project"
                    ]
                }
            )
            
            ords_phd = add_program_with_courses(
                "Operations Research and Decision Support",
                "PhD",
                "Doctoral studies in operations research and decision support",
                {
                    1: [
                        "Advanced Topics in Decision Support Systems",
                        "Multi-criteria Decision Making",
                        "Probabilistic Models"
                    ],
                    2: [
                        "Game Theory Applications",
                        "Advanced Topics in Operations Research",
                        "Directed Individual Readings (Advanced Topics)"
                    ]
                }
            )
            
            # 3. Supply Chain and Operations Management
            scom_diploma = add_program_with_courses(
                "Supply Chain and Operations Management",
                "Diploma",
                "Program for supply chain and operations management fundamentals",
                {
                    1: [
                        "Project Management: Tools & Techniques",
                        "Quantitative Analysis Tools in Decision Making",
                        "Operations Management",
                        "Operations Management Software",
                        "Supply Chain Management"
                    ],
                    2: [
                        "Business Statistical Analysis",
                        "Information Systems in Supply Chain",
                        "Production Management",
                        "Quality Management",
                        "Project"
                    ]
                }
            )
            
            # Add all the remaining programs following the same pattern
            # 4. Web Design
            wd_diploma = add_program_with_courses(
                "Web Design",
                "Diploma",
                "Program for web design fundamentals",
                {
                    1: [
                        "Introduction to Computer Science",
                        "SQL Server Database",
                        "HTML 5 and CSS 3",
                        "Photoshop for Web Design",
                        "ASP.NET, JavaScript and jQuery"
                    ],
                    2: [
                        "PHP Web Programming",
                        "Bootstrap for Responsive Web Design",
                        "SEO Web Development",
                        "Object Oriented Programming",
                        "Project"
                    ]
                }
            )
            
            # 5. Software Engineering
            se_diploma = add_program_with_courses(
                "Software Engineering",
                "Diploma",
                "Program for software engineering fundamentals",
                {
                    1: [
                        "Computer Systems Principles and Programming",
                        "Relational Database Systems",
                        "The Software Development Process",
                        "The User Interface Design",
                        "Object-Oriented Software Development using UML"
                    ],
                    2: [
                        "Software Project Management",
                        "Web Design and Architecture",
                        "Agile Software Development",
                        "Programming in the Large",
                        "Project"
                    ]
                }
            )
            
            se_master = add_program_with_courses(
                "Software Engineering",
                "Master",
                "Advanced software engineering concepts and methodologies",
                {
                    1: [
                        "Principles and Methodologies of Scientific Research",
                        "Software Quality Assurance",
                        "Advanced Topics in Database"
                    ],
                    2: [
                        "Advanced Topics in Information Systems",
                        "Information Security",
                        "Advanced Agile Software Development",
                        "Project"
                    ]
                }
            )
            
            se_phd = add_program_with_courses(
                "Software Engineering",
                "PhD",
                "Doctoral studies in software engineering",
                {
                    1: [
                        "Selected Topics in Software Engineering",
                        "Selected Topics in Information Systems",
                        "Selected Topics in Information Technology"
                    ],
                    2: [
                        "Data Warehousing",
                        "Developing E-commerce Solutions",
                        "Directed Individual Readings (Advanced Topics)"
                    ]
                }
            )
            
            # Commit all changes to the database
            db.session.commit()
            print("Successfully populated all programs and courses!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error populating database: {str(e)}")
            traceback.print_exc()

if __name__ == '__main__':
    populate_all_programs()
