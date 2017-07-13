package id.nlp.depparser;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.ud.CoNLLUDocumentWriter;
import edu.stanford.nlp.trees.ud.ExtendedCoNLLUDocumentWriter;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;

import java.io.File;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import static edu.stanford.nlp.pipeline.Annotator.*;

public class DependencyParser {

    static final String TAGGER_MODEL = "tagger-id.universal.model";
    static final String NER_MODEL = "ner-id.model.ser.gz";
    static final String PARSER_MODEL = "parser-id.conllu.model.gz";
    static final int NUM_THREADS = 1;
    static final String OUTPUT_FORMAT = "conllu";

    AnnotatorPool annotatorPool;
    Properties props;
    StanfordCoreNLP pipeline;

    public DependencyParser() throws SQLException, IOException, ClassNotFoundException {
        this(TAGGER_MODEL, NER_MODEL, PARSER_MODEL, NUM_THREADS);
    }

    public DependencyParser(
            String taggerModel,
            String nerModel,
            String parserModel,
            int numThreads
    ) throws SQLException, IOException, ClassNotFoundException {

        // Create the Stanford CoreNLP pipeline
        this.props = PropertiesUtils.asProperties(
                "annotators", "tokenize,ssplit,pos,lemma,ner,depparse",
                "ssplit.eolonly", "true",
                "ner.model", nerModel,
                "ner.useSUTime", "false",
                "pos.model", taggerModel,
                "depparse.model", parserModel,
                "splitter.nomodel", "true",
                "ignore_affinity", "true",
                "outputFormat", OUTPUT_FORMAT,
                "threads", String.valueOf(numThreads)
        );

        // Create annotator pools
        this.annotatorPool = new AnnotatorPool();
        AnnotatorImplementations annotatorImplementations = new IndonesianAnnotatorImplementations();
        annotatorPool.register(STANFORD_TOKENIZE, AnnotatorFactories.tokenize(props, annotatorImplementations));
        annotatorPool.register(STANFORD_SSPLIT, AnnotatorFactories.sentenceSplit(props, annotatorImplementations));
        annotatorPool.register(STANFORD_POS, AnnotatorFactories.posTag(props, annotatorImplementations));
        annotatorPool.register(STANFORD_LEMMA, AnnotatorFactories.lemma(props, annotatorImplementations));
        annotatorPool.register(STANFORD_NER, AnnotatorFactories.nerTag(props, annotatorImplementations));
        annotatorPool.register(STANFORD_DEPENDENCIES, AnnotatorFactories.dependencies(props, annotatorImplementations));

        // Create pipeline
        this.pipeline = new IndonesianStanfordCoreNLP(this.props, annotatorPool);
    }

    /**
     * Parse text
     * @param text
     * @return
     */
    public String parse(String text) {
        StringBuilder result = new StringBuilder();
        Annotation doc = pipeline.process(text);
        List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);
        CoNLLUDocumentWriter conllUWriter = new ExtendedCoNLLUDocumentWriter();
        for (CoreMap sentence : sentences) {
            SemanticGraph sg = sentence.get(SemanticGraphCoreAnnotations.BasicDependenciesAnnotation.class);
            if (sg != null) {
                result.append(conllUWriter.printSemanticGraph(sg)).append("\n");
            }
        }
        return result.toString();
    }

    /**
     * Parse input file(s)
     * @param inputFiles
     * @param outputDir
     * @throws IOException
     */
    public void parse(List<File> inputFiles, String outputDir) throws IOException, SQLException, ClassNotFoundException {
        // override existing pipeline
        if (!props.containsKey("outputDirectory")) {
            props.setProperty("outputDirectory", outputDir);
            this.pipeline = new IndonesianStanfordCoreNLP(this.props, this.annotatorPool);
        }
        pipeline.processFiles(inputFiles);
    }

    public static void main(String args[]) {

        // parse arguments
        ArgumentParser parser = ArgumentParsers.newArgumentParser("DependencyParser").defaultHelp(true).description("Generate CONLL-U dependency tree from Indonesian text");
        parser.addArgument("-t", "--text").help("Text input to parse");
        parser.addArgument("-f", "--file").nargs("*").help("File input to parse");
        parser.addArgument("-o", "--outputDir").setDefault(".").help("Output directory");

        Namespace ns = null;
        try {
            ns = parser.parseArgs(args);
        } catch (ArgumentParserException e) {
            parser.handleError(e);
            System.exit(1);
        }

        String text = ns.getString("text");
        List<String> files = ns.<String> getList("file");
        String outputDir = ns.getString("outputDir");
        try {
            if (text != null) {
                text = text.trim();
                if (!text.endsWith(".")) {
                  text += ".";
                }
                System.out.println(new DependencyParser().parse(text));
            } else if (files != null) {
                List<File> fileList = new ArrayList<>();
                List<String> outputFiles = new ArrayList<>();
                String sep = System.getProperty("file.separator");
                for (String file:files) {
                    File fileObj = new File(file);
                    fileList.add(fileObj);
                    outputFiles.add(outputDir + sep + fileObj.getName() + "." + OUTPUT_FORMAT);
                }
                new DependencyParser().parse(fileList, outputDir);
                System.out.println("File(s) created:");
                for (String outputFile:outputFiles) {
                    System.out.println(outputFile);
                }
            } else {
                System.err.println("No input provided");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
