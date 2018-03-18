package repository;

import model.Laboratory;

import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LaboratoryFileDataPersistence extends FileDataPersistence{
    public LaboratoryFileDataPersistence(String file) {
        super(file);
    }

    // No check if laboratory is unique
    public void saveLaboratory(Laboratory laboratory) throws IOException, ParseException {
        Map<String, List<Laboratory>> assignedLaboratories = this.getLaboratoryMap();
        for (Laboratory laboratoryInList : assignedLaboratories.get(laboratory.getStudentRegNumber())) {
            if (laboratory.getProblemNumber() == laboratoryInList.getProblemNumber() && laboratory.getLaboratoryNumber() == laboratoryInList.getLaboratoryNumber()) {
                return;
            }
        }
        BufferedWriter writer;
        try {
            writer = new BufferedWriter(new FileWriter(file, true));
            writer.write(laboratory.toString() + "\n");
            writer.close();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    // Ambiguous what field of "Student" should be passed
    public void addGrade(String studentRegNumber, String labNumber, float grade)
            throws IOException, NumberFormatException, ParseException {
        File fileA = new File(file);
        File fileB = new File("temp");

        BufferedReader reader = new BufferedReader(new FileReader(fileA));
        BufferedWriter writer = new BufferedWriter(new FileWriter(fileB));

        String line;

        while ((line = reader.readLine()) != null) {
            String[] lineData = line.split(" ");
            String fileLabNumber = lineData[0];
            String fileStudentNumber = lineData[4];
            SimpleDateFormat format = new SimpleDateFormat("dd/MM/yyyy");
            if (fileLabNumber.equals(labNumber) && fileStudentNumber.equals(studentRegNumber)) {
                Laboratory laboratory = new Laboratory(
                        Integer.valueOf(lineData[0]), format.parse(lineData[1]),
                        Integer.valueOf(lineData[2]), lineData[4]);
                laboratory.setGrade(grade);
                writer.write(laboratory.toString() + "\n");
            } else {
                writer.write(line + "\n");
            }
        }
        writer.close();
        reader.close();

        fileA.delete();
        fileB.renameTo(fileA);
    }

    public Map<String, List<Laboratory>> getLaboratoryMap()
            throws NumberFormatException, IOException, ParseException {
        BufferedReader reader = new BufferedReader(new FileReader(file));

        Map<String, List<Laboratory>> laboratoryMap = new HashMap<String, List<Laboratory>>();

        String line;

        while ((line = reader.readLine()) != null) {
            String[] lineData = line.split(" ");
            SimpleDateFormat format = new SimpleDateFormat("dd/MM/yyyy");
            Laboratory laboratory = new Laboratory(Integer.valueOf(lineData[0]),
                    format.parse(lineData[1]), Integer.valueOf(lineData[2]), Float.valueOf(lineData[3]),
                    lineData[4]);
            if (laboratoryMap.get(laboratory.getStudentRegNumber()) == null) {
                List<Laboratory> laboratoryList = new ArrayList<Laboratory>();
                laboratoryList.add(laboratory);
                laboratoryMap.put(laboratory.getStudentRegNumber(),
                        laboratoryList);
            } else {
                laboratoryMap.get(laboratory.getStudentRegNumber()).add(
                        laboratory);
            }
        }
        return laboratoryMap;
    }
}
