package edu.stanford.nlp.pipeline;

import edu.stanford.nlp.io.RuntimeIOException;
import edu.stanford.nlp.util.MetaClass;
import edu.stanford.nlp.util.PropertiesUtils;
import edu.stanford.nlp.util.ReflectionLoading;
import edu.stanford.nlp.util.logging.Redwood;
import org.h2.tools.RunScript;

import java.io.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Collection;
import java.util.Properties;
import java.util.function.BiConsumer;

public class IndonesianStanfordCoreNLP extends StanfordCoreNLP {

    private static final Redwood.RedwoodChannels logger = Redwood.channels(IndonesianStanfordCoreNLP.class);
    private static final String sqlFile = System.getProperty("file.separator") + "database.sql";
    private static final String databaseUrl = "jdbc:h2:mem:corenlp;DB_CLOSE_DELAY=-1;IGNORECASE=TRUE";

    private Properties properties;

    public IndonesianStanfordCoreNLP() throws Exception {
        this((Properties) null);
    }

    /**
     * Construct a basic pipeline. The Properties will be used to determine
     * which annotators to create, and a default AnnotatorPool will be used
     * to create the annotators.
     *
     */
    public IndonesianStanfordCoreNLP(Properties props) throws Exception {
        this(props, null);
        this.properties = props;
    }

    /**
     * Construct a CoreNLP with a custom Annotator Pool.
     */
    public IndonesianStanfordCoreNLP(Properties props, AnnotatorPool annotatorPool) throws ClassNotFoundException, SQLException, IOException {
        super(props, (props == null || PropertiesUtils.getBool(props, "enforceRequirements", true)), annotatorPool);
        this.properties = props;
        Connection connection = createDatabaseConnection();
        connection.close();
    }

    /**
     * Override annotator registration
     * @return
     */
    @Override
    protected AnnotatorImplementations getAnnotatorImplementations() {
        return new IndonesianAnnotatorImplementations();
    }

    /**
     * Process a collection of files.
     *
     * @param base The base input directory to process from.
     * @param files The files to process.
     * @param numThreads The number of threads to annotate on.
     *
     * @throws IOException
     */
    @Override
    public void processFiles(String base, final Collection<File> files, int numThreads) throws IOException {
        AnnotationOutputter.Options options = AnnotationOutputter.getOptions(this);
        StanfordCoreNLP.OutputFormat outputFormat = StanfordCoreNLP.OutputFormat.valueOf(properties.getProperty("outputFormat", DEFAULT_OUTPUT_FORMAT).toUpperCase());
        processFiles(base, files, numThreads, properties, this::annotate, createOutputter(properties, options), outputFormat);
    }


    /**
     * Copied from StanfordCoreNLP.createOutputter
     * overriding CoNLLUOutputter with ExtendedCoNLLUOutputter
     *
     * @param properties The properties file to use.
     * @param outputOptions The means of creating output options
     *
     * @return A consumer that can be passed into the processFiles method.
     */
    protected static BiConsumer<Annotation, OutputStream> createOutputter(Properties properties, AnnotationOutputter.Options outputOptions) {
        final OutputFormat outputFormat =
                OutputFormat.valueOf(properties.getProperty("outputFormat", DEFAULT_OUTPUT_FORMAT).toUpperCase());

        final String serializerClass = properties.getProperty("serializer", GenericAnnotationSerializer.class.getName());
        final String outputSerializerClass = properties.getProperty("outputSerializer", serializerClass);
        final String outputSerializerName = (serializerClass.equals(outputSerializerClass))? "serializer":"outputSerializer";

        return (Annotation annotation, OutputStream fos) -> {
            try {
                switch (outputFormat) {
                    case XML: {
                        AnnotationOutputter outputter = MetaClass.create("edu.stanford.nlp.pipeline.XMLOutputter").createInstance();
                        outputter.print(annotation, fos, outputOptions);
                        break;
                    }
                    case JSON: {
                        new JSONOutputter().print(annotation, fos, outputOptions);
                        break;
                    }
                    case CONLL: {
                        new CoNLLOutputter().print(annotation, fos, outputOptions);
                        break;
                    }
                    case TEXT: {
                        new TextOutputter().print(annotation, fos, outputOptions);
                        break;
                    }
                    case SERIALIZED: {
                        if (outputSerializerClass != null) {
                            AnnotationSerializer outputSerializer = loadSerializer(outputSerializerClass, outputSerializerName, properties);
                            outputSerializer.write(annotation, fos);
                        }
                        break;
                    }
                    case CONLLU:
                        new ExtendedCoNLLUOutputter().print(annotation, fos, outputOptions);
                        break;
                    default:
                        throw new IllegalArgumentException("Unknown output format " + outputFormat);
                }
            } catch (IOException e) {
                throw new RuntimeIOException(e);
            }
        };
    }

    /**
     * Copied from StanfordCoreNLP.loadSerializer
     * @param serializerClass
     * @param name
     * @param properties
     * @return
     */
    private static AnnotationSerializer loadSerializer(String serializerClass, String name, Properties properties) {
        AnnotationSerializer serializer; // initialized below
        try {
            // Try loading with properties
            serializer = ReflectionLoading.loadByReflection(serializerClass, name, properties);
        } catch (ReflectionLoading.ReflectionLoadingException ex) {
            // Try loading with just default constructor
            serializer = ReflectionLoading.loadByReflection(serializerClass);
        }
        return serializer;
    }

    /**
     * Create database connection to H2 in-memory database (for Lemmatizer)
     * @return
     * @throws ClassNotFoundException
     * @throws SQLException
     * @throws IOException
     */
    public static Connection createDatabaseConnection() throws ClassNotFoundException, SQLException, IOException {
        Class.forName("org.h2.Driver");
        Connection connection = DriverManager.getConnection(databaseUrl);
        ResultSet rs = connection.getMetaData().getTables(null, null, "DICTIONARY", null);
        boolean found = rs.next();

        // if table does not exist, load from sql
        if (!found) {
            BufferedReader reader = null;
            InputStream in = null;
            try {
                in = IndonesianStanfordCoreNLP.class.getClass().getResourceAsStream(sqlFile);
                reader = new BufferedReader(new InputStreamReader(in));
                RunScript.execute(connection, reader);
            } finally {
                if (reader != null) {
                    reader.close();
                }
                if (in != null) {
                    in.close();
                }
            }
        }
        return connection;
    }
}
