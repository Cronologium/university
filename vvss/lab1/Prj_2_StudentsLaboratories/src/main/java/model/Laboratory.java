package model;

import java.util.Date;

public class Laboratory {
    // Ambiguous names : laboratoryNumber and problem laboratoryNumber
    private int laboratoryNumber;
    private Date date;
    private int problemNumber;
    private float grade = 1;
    private String studentRegNumber;

    public Laboratory(int laboratoryNumber, Date date, int problemNumber,
                      String studentRegNumber) {
        this.laboratoryNumber = laboratoryNumber;
        this.date = date;
        this.problemNumber = problemNumber;
        this.studentRegNumber = studentRegNumber;
    }

    public Laboratory(int laboratoryNumber, Date date, int problemNumber, Float grade,
                      String studentRegNumber) {
        this.laboratoryNumber = laboratoryNumber;
        this.date = date;
        this.problemNumber = problemNumber;
        this.grade = grade;
        this.studentRegNumber = studentRegNumber;
    }

    public int getLaboratoryNumber() {
        return laboratoryNumber;
    }

    public void setLaboratoryNumber(int laboratoryNumber) {
        this.laboratoryNumber = laboratoryNumber;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public int getProblemNumber() {
        return problemNumber;
    }

    public void setProblemNumber(int problemNumber) {
        this.problemNumber = problemNumber;
    }

    public float getGrade() {
        return grade;
    }

    public void setGrade(float grade) {
        this.grade = grade;
    }

    public String getStudentRegNumber() {
        return studentRegNumber;
    }

    public void setStudentRegNumber(String studentRegNumber) {
        this.studentRegNumber = studentRegNumber;
    }

    @Override
    public String toString() {
        int month = date.getMonth() + 1;
        int year = date.getYear() + 1900;
        return laboratoryNumber + " " + date.getDate() + "/" + month + "/" + year + " "
                + problemNumber + " " + grade + " " + studentRegNumber;
    }

} 