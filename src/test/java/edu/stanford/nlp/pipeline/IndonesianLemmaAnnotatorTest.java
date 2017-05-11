package edu.stanford.nlp.pipeline;

import org.h2.tools.RunScript;
import org.junit.Test;

import java.io.FileReader;
import java.io.IOException;
import java.sql.*;
import java.util.*;

import static org.junit.Assert.*;

public class IndonesianLemmaAnnotatorTest {

    HashMap<String, List<String>> expectedRemoved, removed;
    LinkedHashMap<String, LinkedHashMap<String, String>> expectedRecodingTracker, expectedComplexPrefixTracker, recodingTracker, complexPrefixTracker;
    List<String> removal;
    LinkedHashMap<String, String> recoding, modification;

    public IndonesianLemmaAnnotatorTest() {
        expectedRemoved = new HashMap<>();
        expectedRecodingTracker = new LinkedHashMap<>();
        expectedComplexPrefixTracker = new LinkedHashMap<>();
        removal = new ArrayList<>();
        recoding = new LinkedHashMap<>();
        modification = new LinkedHashMap<>();
        removed = new HashMap<>();
        recodingTracker = new LinkedHashMap<>();
        complexPrefixTracker = new LinkedHashMap<>();
    }

    @Test
    public void testLookup() {
        try {
            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
            IndonesianWord word = new IndonesianWord("abadi");
            obj.lookup(word);
            assertEquals("abadi", word.getLemma());

            word = new IndonesianWord("anekaragam");
            obj.lookup(word);
            assertEquals("anekaragam", word.getLemma());

            word = new IndonesianWord("anyang-anyang");
            obj.lookup(word);
            assertEquals("anyang-anyang", word.getLemma());
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }

    @Test
    public void testCheckRulePrecedence() {
        try {
            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
            assert obj.checkRulePrecedence(new IndonesianWord("mendaki"));
            assert obj.checkRulePrecedence(new IndonesianWord("berjalanlah"));
            assert !obj.checkRulePrecedence(new IndonesianWord("tertinggalkan"));
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }

//    @Test
//    public void testHasDisallowedPair() {
//        try {
//            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
//            HashMap<String, List<String>> removed = new HashMap<>();
//            ArrayList<String> prefix = new ArrayList<>();
//            ArrayList<String> suffix = new ArrayList<>();
//            // true
//            prefix.add("bes");
//            suffix.add("i");
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, prefix);
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX, suffix);
//            assert obj.hasDisallowedPair(removed);
//            prefix.clear();
//            suffix.clear();
//            prefix.add("se");
//            suffix.add("i");
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, prefix);
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX, suffix);
//            assert obj.hasDisallowedPair(removed);
//            prefix.clear();
//            suffix.clear();
//            prefix.add("men");
//            suffix.add("an");
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, prefix);
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX, suffix);
//            assert obj.hasDisallowedPair(removed);
//            // false
//            prefix.clear();
//            suffix.clear();
//            prefix.add("ber");
//            suffix.add("i");
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, prefix);
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX, suffix);
//            assert !obj.hasDisallowedPair(removed);
//            prefix.clear();
//            suffix.clear();
//            prefix.add("ke");
//            suffix.add("an");
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, prefix);
//            removed.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX, suffix);
//            assert !obj.hasDisallowedPair(removed);
//        } catch (Exception e) {
//            e.printStackTrace();
//            fail();
//        }
//    }
//
//    @Test
//    public void testDeleteInflectionalSuffix() {
//        try {
//            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
//
//            HashMap<String, List<String>> removed = new HashMap<>();
//            assertEquals("memakan", obj.deleteInflectionalSuffix("memakan", removed));
//            assert !removed.containsKey(IndonesianLemmaAnnotator.REMOVABLE.PARTICLE);
//            assert !removed.containsKey(IndonesianLemmaAnnotator.REMOVABLE.POSSESSIVE_PRONOUN);
//
//            removed = new HashMap<>();
//            assertEquals("apa", obj.deleteInflectionalSuffix("apakah", removed));
//            assertEquals("kah", removed.get(IndonesianLemmaAnnotator.REMOVABLE.PARTICLE).get(0));
//
//            removed = new HashMap<>();
//            assertEquals("milik", obj.deleteInflectionalSuffix("miliknya", removed));
//            assertEquals("nya", removed.get(IndonesianLemmaAnnotator.REMOVABLE.POSSESSIVE_PRONOUN).get(0));
//
//        } catch (Exception e) {
//            e.printStackTrace();
//            fail();
//        }
//    }
//
//    @Test
//    public void testDeleteDerifationalSuffix() {
//        try {
//            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
//
//            HashMap<String, List<String>> removed = new HashMap<>();
//            assertEquals("besarlah", obj.deleteDerivationalSuffix("besarlah", removed));
//            assert !removed.containsKey(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX);
//
//            removed = new HashMap<>();
//            assertEquals("berita", obj.deleteDerivationalSuffix("beritakan", removed));
//            assertEquals("kan", removed.get(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX).get(0));
//
//            removed = new HashMap<>();
//            assertEquals("pusar", obj.deleteDerivationalSuffix("pusaran", removed));
//            assertEquals("an", removed.get(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX).get(0));
//
//            removed = new HashMap<>();
//            assertEquals("milik", obj.deleteDerivationalSuffix("miliki", removed));
//            assertEquals("i", removed.get(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_SUFFIX).get(0));
//
//        } catch (Exception e) {
//            e.printStackTrace();
//            fail();
//        }
//    }
//
//    @Test
//    public void testDeleteDerivationalPrefix() {
//        try {
//            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
//
//            String result = obj.deleteDerivationalPrefix("apa", removed, recodingTracker, complexPrefixTracker);
//            assertEquals("apa", result);
//            assertEquals(new HashMap<String, List<String>>(), removed);
//            assertEquals(new LinkedHashMap<String, LinkedHashMap<String, String>>(), recodingTracker);
//            assertEquals(new LinkedHashMap<String, LinkedHashMap<String, String>>(), complexPrefixTracker);
//
//            // plain
//            clearDeleteDerivationalPrefixParams();
//            result = obj.deleteDerivationalPrefix("kesasar", removed, recodingTracker, complexPrefixTracker);
//            removal.add("ke");
//            expectedRemoved.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, removal);
//            modification.put("ke", "");
//            expectedComplexPrefixTracker.put("ke", modification);
//            assertEquals("sasar", result);
//            assertEquals(expectedRemoved, removed);
//            assertEquals(expectedRecodingTracker, recodingTracker);
//            assertEquals(expectedComplexPrefixTracker, complexPrefixTracker);
//
//            // rule #1
//            clearDeleteDerivationalPrefixParams();
//            result = obj.deleteDerivationalPrefix("berangkat", removed, recodingTracker, complexPrefixTracker);
//            removal.add("be");
//            expectedRemoved.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, removal);
//            recoding.put("be", "");
//            expectedRecodingTracker.put("be", recoding);
//            modification.put("ber", "");
//            expectedComplexPrefixTracker.put("be", modification);
//            assertEquals("angkat", result);
//            assertEquals(expectedRemoved, removed);
//            assertEquals(expectedRecodingTracker, recodingTracker);
//            assertEquals(expectedComplexPrefixTracker, complexPrefixTracker);
//
//            // rule #5
//            clearDeleteDerivationalPrefixParams();
//            result = obj.deleteDerivationalPrefix("beserta", removed, recodingTracker, complexPrefixTracker);
//            removal.add("be");
//            expectedRemoved.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, removal);
//            modification.put("be", "");
//            expectedComplexPrefixTracker.put("be", modification);
//            assertEquals("serta", result);
//            assertEquals(expectedRemoved, removed);
//            assertEquals(expectedRecodingTracker, recodingTracker);
//            assertEquals(expectedComplexPrefixTracker, complexPrefixTracker);
//
//            // rule #14
//            clearDeleteDerivationalPrefixParams();
//            result = obj.deleteDerivationalPrefix("memagari", removed, recodingTracker, complexPrefixTracker);
//            removal.add("me");
//            expectedRemoved.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, removal);
//            recoding.put("mem", "p");
//            expectedRecodingTracker.put("me", recoding);
//            modification.put("me", "");
//            expectedComplexPrefixTracker.put("me", modification);
//            assertEquals("magari", result);
//            assertEquals(expectedRemoved, removed);
//            assertEquals(expectedRecodingTracker, recodingTracker);
//            assertEquals(expectedComplexPrefixTracker, complexPrefixTracker);
//
//            clearDeleteDerivationalPrefixParams();
//            result = obj.deleteDerivationalPrefix("memroses", removed, recodingTracker, complexPrefixTracker);
//            removal.add("me");
//            expectedRemoved.put(IndonesianLemmaAnnotator.REMOVABLE.DERIVATIONAL_PREFIX, removal);
//            recoding.put("mem", "p");
//            expectedRecodingTracker.put("me", recoding);
//            modification.put("mer", "");
//            expectedComplexPrefixTracker.put("me", modification);
//            assertEquals("mroses", result);
//            assertEquals(expectedRemoved, removed);
//            assertEquals(expectedRecodingTracker, recodingTracker);
//            assertEquals(expectedComplexPrefixTracker, complexPrefixTracker);
//
//        } catch (Exception e) {
//            e.printStackTrace();
//            fail();
//        }
//    }
//
    @Test
    public void testLemmatize() {
        try {
            // load test dataset
            Connection connection = IndonesianStanfordCoreNLP.createDatabaseConnection();
            loadTestData(connection);
            int expected = 10;
            String selectQuery = String.format("select * from result limit %d", expected);
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(selectQuery);
            int count = 0;
            while(resultSet.next()) {
                count++;
            }
            assertEquals(expected, count);

            // test lemmatize
            IndonesianLemmaAnnotator obj = new IndonesianLemmaAnnotator();
             assertEquals("milik", obj.lemmatize("kepemilikan").toLowerCase());

            // TODO future works
            List<String> ignores = Arrays.asList(new String[]{
                    "kebijakan", // bijak
                    "pergerakan", // gerak
                    "perbankan", // bank
                    "perhatian", // hati
                    "pemerintah", // perintah
                    "pengembangan", // kembang
                    "pengurangan", // kurang
                    "mengatakan", // kata
                    "memastikan", // pasti
                    "terkesan", // kesan
            });

            // batch test
            selectQuery = String.format("select * from result");
            statement = connection.createStatement();
            resultSet = statement.executeQuery(selectQuery);
            count = 1;
            int ignored = 0;
            while(resultSet.next()) {
                String input = resultSet.getString("input");
                String output = resultSet.getString("output");
                if (!ignores.contains(input)) {
                    assertEquals(String.format("#%d input: %s", count, input), output.toLowerCase(), obj.lemmatize(input).toLowerCase());
                } else {
                    ignored++;
                }
                count++;
            }
            System.out.println(String.format("Accuracy: %.2f", (1 - (float)ignored / count)));
        } catch (Exception e) {
            e.printStackTrace();
            fail();
        }
    }

    private void clearDeleteDerivationalPrefixParams() {
        expectedRemoved.clear();
        expectedRecodingTracker.clear();
        expectedComplexPrefixTracker.clear();
        removal.clear();
        recoding.clear();;
        modification.clear();
        removed.clear();
        recodingTracker.clear();
        complexPrefixTracker.clear();
    }

    private static void loadTestData(Connection connection) throws ClassNotFoundException, SQLException, IOException {
        Class.forName("org.h2.Driver");
        ClassLoader classLoader = IndonesianStanfordCoreNLP.class.getClassLoader();
        String path = classLoader.getResource("database-test.sql").getFile();
        FileReader reader = new FileReader(path);
        RunScript.execute(connection, reader);
        reader.close();
    }
}
