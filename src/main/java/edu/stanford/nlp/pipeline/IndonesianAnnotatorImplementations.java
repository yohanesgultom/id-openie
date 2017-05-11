package edu.stanford.nlp.pipeline;

import edu.stanford.nlp.naturalli.IndonesianOpenIE;
import edu.stanford.nlp.util.PropertiesUtils;
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

    @Override
    public Annotator openie(Properties properties) {
        Properties relevantProperties = PropertiesUtils.extractPrefixedProperties(properties,
                Annotator.STANFORD_OPENIE + '.');
        return new IndonesianOpenIE(relevantProperties);
    }

}
