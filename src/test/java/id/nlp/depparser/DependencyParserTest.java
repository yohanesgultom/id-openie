package id.nlp.depparser;

import org.junit.Test;

import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;

public class DependencyParserTest {

    @Test
    public void parseTextTest() {
        try {
            String actual = new DependencyParser().parse("Sembungan adalah sebuah desa yang terletak di kecamatan Kejajar , kabupaten Wonosobo , Jawa Tengah , Indonesia .");
            System.out.println(actual);
            assertNotNull(actual);
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }

    @Test
    public void parseFileTest() {
        try {
            String[] files = new String[]{ System.getProperty("file.separator") + "plain.txt" };
            List<File> fileList = new ArrayList<>();
            URL url = null;
            for (String file:files) {
                url = getClass().getResource(file);
                fileList.add(new File(url.getFile()));
            }

            // get dir from last file
            String dir = url.getPath().substring(0, url.getPath().lastIndexOf(System.getProperty("file.separator")));
            new DependencyParser().parse(fileList, dir);

            // check if output file created
            for (String file:files) {
                assertNotNull(getClass().getResource(file + ".conllu"));
            }
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }
}
