package ui;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

//import com.sun.org.apache.xpath.internal.operations.Bool;
import controller.LaboratoriesController;
import model.Laboratory;
import model.Student;
import validator.Validator;

public class LaboratoriesUI {
	private LaboratoriesController controller;

    public LaboratoriesUI(){
    }

    public void run(){
        System.out.println("Starting");

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        this.controller = new LaboratoriesController("students.txt", "laboratories.txt");

        while(true) {
            System.out.println(" 1) Add student \n" +
                    " 2) Add Laboratory \n" +
                    " 3) Add grade \n" +
                    " 4) Get passing students \n" +
                    " 5) Exit");
            try {
                String line = br.readLine().trim();
                if (line.equals("1")) {
                    String registrationNumber, name;
                    int group;
                    System.out.print("Registration number: ");
                    registrationNumber = br.readLine();
                    System.out.print("Name: ");
                    name = br.readLine();
                    try {
                        System.out.print("Group number: ");
                        String groupString = br.readLine();
                        group = Integer.parseInt(groupString);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid group - not a number");
                        continue;
                    }

                    Student student = new Student(registrationNumber, name, group);
                    Boolean success = controller.saveStudent(student);
                    if (!success) {
                        System.out.println("Invalid student");
                    }
                } else if (line.equals("2")) {
                    int number, problemNumber;
                    String date, studentRegNumber;

                    try {
                        System.out.println("Lab number: ");
                        String labNumberString = br.readLine();
                        System.out.println("Problem number: ");
                        String labProblemNumberString = br.readLine();
                        number = Integer.parseInt(labNumberString);
                        problemNumber = Integer.parseInt(labProblemNumberString);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid input");
                        continue;
                    }

                    System.out.println("Date (dd/mm/yyy)");
                    date = br.readLine();
                    System.out.println("Student reg number");
                    studentRegNumber = br.readLine();
                    Laboratory lab;
                    SimpleDateFormat format = new SimpleDateFormat("dd/MM/yyyy");
                    try {
                        lab = new Laboratory(number, format.parse(date), problemNumber, studentRegNumber);
                        Boolean success = controller.saveLaboratory(lab);
                        if (!success) {
                            System.out.println("Cannot save laboratory");
                        }
                    } catch (ParseException e) {
                        System.out.println("Invalid input");
                    }

                } else if (line.equals("3")) {
                    String registrationNumber, labNumber;
                    float grade;
                    System.out.println("Reg number: ");
                    registrationNumber = br.readLine();
                    System.out.println("Lab number: ");
                    labNumber = br.readLine();
                    try {
                        System.out.println("Grade: ");
                        String gradeString = br.readLine();
                        grade = Float.parseFloat(gradeString);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid grade");
                        continue;
                    }
                    try {
                        Boolean success = controller.addGrade(registrationNumber, labNumber, grade);
                        if (!success) {
                            System.out.println("Cannot save grade");
                        }
                    } catch (NumberFormatException | IOException | ParseException e) {
                        System.out.println("Cannot save grade");
                    }

                } else if (line.equals("4")) {
                    try {
                        List<Student> passingStudents = controller.passedStudents();
                        System.out.println("Passing students: ");
                        for (Student student : passingStudents) {
                            System.out.println("\t - " + student.toString());
                        }
                    } catch (ParseException e) {
                        System.out.println("Could not get passing students");
                    }
                } else if (line.equals("5")) {
                    break;
                } else {
                    System.out.println("Invalid option");
                }
            } catch (IOException exception) {
                System.out.println("An error occured while reading from command line: " + exception.getMessage());
            }
        }
    }
} 