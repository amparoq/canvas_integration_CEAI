from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

class Report(Base):
    __tablename__ = 'report'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    report_pdf = Column(LargeBinary(length=(2**32)-1), nullable=False)  # PDF almacenado en la base de datos
    
    student = relationship('Student', back_populates='reports')
    

class Assignment(Base):
    __tablename__ = 'assignment'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, primary_key=True)
    
    due_date = Column(DateTime)

Student.reports = relationship('Report', order_by=Report.id, back_populates='student')
