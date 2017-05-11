package edu.stanford.nlp.pipeline;

import edu.stanford.nlp.io.IOUtils;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations;
import edu.stanford.nlp.trees.ud.ExtendedCoNLLUDocumentWriter;
import edu.stanford.nlp.util.CoreMap;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.List;

public class ExtendedCoNLLUOutputter extends CoNLLUOutputter {

    private static final ExtendedCoNLLUDocumentWriter conllUWriter = new ExtendedCoNLLUDocumentWriter();

    public ExtendedCoNLLUOutputter() {}

    @Override
    public void print(Annotation doc, OutputStream target, Options options) throws IOException {
        PrintWriter writer = new PrintWriter(IOUtils.encodedOutputStreamWriter(target, options.encoding));

        List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);
        for (CoreMap sentence : sentences) {
            SemanticGraph sg = sentence.get(SemanticGraphCoreAnnotations.BasicDependenciesAnnotation.class);
            if (sg != null) {
                writer.print(conllUWriter.printSemanticGraph(sg));
            }
        }
        writer.flush();
    }


    public static void conllUPrint(Annotation annotation, OutputStream os) throws IOException {
        new CoNLLUOutputter().print(annotation, os);
    }

    public static void conllUPrint(Annotation annotation, OutputStream os, StanfordCoreNLP pipeline) throws IOException {
        new CoNLLUOutputter().print(annotation, os, pipeline);
    }

    public static void conllUPrint(Annotation annotation, OutputStream os, Options options) throws IOException {
        new CoNLLUOutputter().print(annotation, os, options);
    }

}
