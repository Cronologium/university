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

    @Test // Test case #1
    public void testAddValidStudent() {
        assertEquals(true, controller.saveStudent(new Student("test1234", "test test", 123)));
    }

    @Test // Test case #2
    public void testAddStudentWithGroupAtInferiorBoundary() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test", 0)));
    }

    @Test // Test case #3
    public void testAddStudentWithGroupAtSuperiorBoundary() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test", 1000)));
    }

    @Test // Test case #4
    public void testAddStudentWithGroupSmallerThanInferiorBoundary() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test", -1)));

    }

    @Test // Test case #5
    public void testAddStudentWithGroupBiggerThanSuperiorBoundary() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test", 1001)));
    }

    @Test // Test case #6
    public void testAddStudentWithGroupNearSuperiorBoundary() {
        assertEquals(true, controller.saveStudent(new Student("test1234", "test test", 999)));
    }

    @Test // Test case #7
    public void testAddStudentWithGroupNearInferiorBoundary() {
        assertEquals(true, controller.saveStudent(new Student("test1234", "test test", 1)));
    }

    @Test // Test case #8
    public void testAddStudentWithRegHavingLessLetters() {
        assertEquals(false, controller.saveStudent(new Student("tes1234", "test test", 123)));
    }

    @Test // Test case #9
    public void testAddStudentWithRegHavingLessDigits() {
        assertEquals(false, controller.saveStudent(new Student("test123", "test test", 123)));
    }

    @Test // Test case #10
    public void testAddStudentWithNameHavingLessWord() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test", 123)));
    }

    @Test // Test case #11
    public void testAddStudentWithNameHavingMoreWords() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test test", 123)));
    }

    @Test // Test case #12
    public void testAddStudentWithNameHavingDigits() {
        assertEquals(false, controller.saveStudent(new Student("test1234", "test test1", 123)));
    }

    @Test // Not really a documented test case, leftover from laboratory work
    public void testAddInvalidStudent() {
        assertEquals(false, controller.saveStudent(new Student("ajahdgasjdhasgda", "asdjaskjdhask", 23874623)));
    }


}
