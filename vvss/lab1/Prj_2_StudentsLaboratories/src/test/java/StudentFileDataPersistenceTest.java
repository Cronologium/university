import controller.LaboratoriesController;
import model.Student;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class StudentFileDataPersistenceTest {

    private LaboratoriesController controller;

    @BeforeEach
    void setUp() {
        controller = new LaboratoriesController("test_file.txt", null);
    }

    @Test
    void testAddValidStudent() {
        assertEquals(true, controller.saveStudent(new Student("test2021", "Test Test", 456)));
    }

    @Test
    void testAddInvalidStudent() {
        assertEquals(false, controller.saveStudent(new Student("ajahdgasjdhasgda", "asdjaskjdhask", 23874623)));
    }
}
