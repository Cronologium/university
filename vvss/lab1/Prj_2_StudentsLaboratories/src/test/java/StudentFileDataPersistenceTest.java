import controller.LaboratoriesController;
import model.Student;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class StudentFileDataPersistenceTest {

    private LaboratoriesController controller;

    @Before
    public void setUp() {
        controller = new LaboratoriesController("test_file.txt", null);
    }

    @Test
    public void testAddValidStudent() {
        assertEquals(true, controller.saveStudent(new Student("test2021", "Test Test", 456)));
    }

    @Test
    public void testAddInvalidStudent() {
        assertEquals(false, controller.saveStudent(new Student("ajahdgasjdhasgda", "asdjaskjdhask", 23874623)));
    }
}
