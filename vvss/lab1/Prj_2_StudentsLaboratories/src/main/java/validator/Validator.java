package validator;

import model.Laboratory;
import model.Student;

import java.util.Date;

public class Validator {

    private static final String STUDENT_REG_NUMBER_REGEX = "[a-zA-Z]{4}[\\d]{4}";
    private static final String STUDENT_NAME_REGEX = "[a-zA-Z]+[\\s][a-zA-Z]+";

    public static boolean validateStudent(Student student) {
        if(!student.getRegNumber().matches(STUDENT_REG_NUMBER_REGEX)){
            return false;
        }
        if (!student.getName().matches(STUDENT_NAME_REGEX)) {
            return false;
        }
        if(student.getGroup() >= 1000 || student.getGroup() <= 0){
            return false;
        }
        return true;
    }

    public static boolean validateLaboratory(Laboratory laboratory) {
        if(laboratory.getLaboratoryNumber() < 1) {
            return false;
        }
        if(laboratory.getProblemNumber() > 10 || laboratory.getProblemNumber() < 1) {
            return false;
        }
        if(!laboratory.getStudentRegNumber().matches(STUDENT_REG_NUMBER_REGEX)) {
            return false;
        }
        Date date = new Date();
        if(date.after(laboratory.getDate())) {
            return false;
        }
        return true;
    }

    public static boolean validateGrade(float grade) {
        if(grade >= 1 && grade <= 10) {
            return true;
        }
        return false;
    }
} 