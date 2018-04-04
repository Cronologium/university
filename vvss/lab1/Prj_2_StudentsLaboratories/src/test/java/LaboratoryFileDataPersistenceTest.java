import controller.LaboratoriesController;
import model.Laboratory;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;

import static org.junit.Assert.assertEquals;

public class LaboratoryFileDataPersistenceTest {
    private LaboratoriesController controller;
    private SimpleDateFormat format;


    @Before
    public void setUp() {
        controller = new LaboratoriesController(null, "lab_test_file.txt");
        format = new SimpleDateFormat("dd/MM/yyyy");
    }

    @Test
    public void testInvalidLaboratoryNumber() throws ParseException, IOException {
        assertEquals(false, controller.saveLaboratory(new Laboratory(-1, format.parse("25/04/2018"), 2, "test1234")));
    }

    @Test
    public void testValidLaboratory() throws ParseException, IOException {
        assertEquals(true, controller.saveLaboratory(new Laboratory(1,format.parse("25/04/2018"), 3, "test1234")));
    }

}
