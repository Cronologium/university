package repository;

import model.Student;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class StudentFileDataPersistence extends FileDataPersistence {
    public StudentFileDataPersistence(String file) {
        super(file);
    }

    public void saveStudent(Student student) {
        try {
            BufferedWriter writer;
            writer = new BufferedWriter(new FileWriter(file, true));
            writer.write(student.toString() + "\n");
            writer.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    public List<Student> getStudentsList() throws NumberFormatException,
            IOException {
        BufferedReader reader = new BufferedReader(new FileReader(file));

        List<Student> allStudentsList = new ArrayList<Student>();

        String line = null;

        while ((line = reader.readLine()) != null) {
            String[] lineData = line.split(" ");
            if (lineData.length == 4) {
                Student student = new Student(lineData[0], lineData[1] + lineData[2], Integer.valueOf(lineData[3]));
                allStudentsList.add(student);
            }
        }

        return allStudentsList;
    }
}
