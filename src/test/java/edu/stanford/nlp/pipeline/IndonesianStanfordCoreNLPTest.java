package edu.stanford.nlp.pipeline;

import org.junit.Test;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.fail;

public class IndonesianStanfordCoreNLPTest {

    @Test
    public void testCreateDatabaseConnection() {
        Connection connection = null;
        try {
            connection = IndonesianStanfordCoreNLP.createDatabaseConnection();
            // test select
            int expected = 10;
            String selectQuery = String.format("select * from dictionary limit %d", expected);
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(selectQuery);
            int count = 0;
            while(resultSet.next()) {
                System.out.println(String.format("%s\t%s", resultSet.getString("lemma"), resultSet.getString("pos")));
                count++;
            }
            connection.close();
            assertEquals(expected, count);
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }

    @Test
    public void testDatabasePersistency() {
        String dummyTableName = "DUMMY";
        try {
            // create dummy table
            Connection connection = IndonesianStanfordCoreNLP.createDatabaseConnection();
            Statement stmt = connection.createStatement();
            String sql = String.format("create table %s (id int not null, primary key (id))", dummyTableName);
            System.out.println(sql);
            stmt.executeUpdate(sql);
            stmt.close();
            connection.close();

            // reconnect & validate dummy table exists
            connection = IndonesianStanfordCoreNLP.createDatabaseConnection();
            ResultSet rs = connection.getMetaData().getTables(null, null, dummyTableName, null);
            assertEquals(true, rs.next());
            connection.close();
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }
}
