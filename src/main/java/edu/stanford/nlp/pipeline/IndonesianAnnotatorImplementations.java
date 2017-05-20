package edu.stanford.nlp.pipeline;

import edu.stanford.nlp.util.logging.Redwood;

import java.util.Properties;

public class IndonesianAnnotatorImplementations extends AnnotatorImplementations {

    private static final Redwood.RedwoodChannels log = Redwood.channels(IndonesianAnnotatorImplementations.class);

    @Override
    public Annotator morpha(Properties properties, boolean verbose) {
        Annotator annotator = null;
        try {
            annotator = new IndonesianLemmaAnnotator(verbose);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
        }
        return annotator;
    }

}
