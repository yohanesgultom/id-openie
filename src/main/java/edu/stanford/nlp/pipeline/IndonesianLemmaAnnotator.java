package edu.stanford.nlp.pipeline;

import edu.stanford.nlp.ling.CoreAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.util.ArraySet;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.logging.Redwood;

import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class IndonesianLemmaAnnotator implements Annotator {

    private static final Redwood.RedwoodChannels log = Redwood.channels(IndonesianLemmaAnnotator.class);
    private boolean verbose = false;

    /* Statics */

    private static final String vowels = "aiueo";
    private static final String consonants = "bcdfghjklmnpqrstvwxyz";
    private static final String consonantsNoR = "bcdfghjklmnpqstvwxyz";
    private static final String consonantsNoLR = "bcdfghjkmnpqstvwxyz";
    private static final String syllable = "([" + consonants + "]|sy)?[" + vowels + "]([" + consonants + "]|ng)?";
    private static final String validWord = "\\w+-?\\w*";

    // regex patterns
    private static final Pattern digits = Pattern.compile("(\\d+)");
    private static final Pattern repetitiveWord = Pattern.compile("^([a-z]+)-([a-z]+)$");
    private static final Pattern compoundWord = Pattern.compile("^(?<first>aneka|(" + syllable + syllable + "))(?<second>" + syllable + syllable + "(" + syllable + ")*)$");
    private static final Pattern vowelsEnding = Pattern.compile("[" + vowels + "]$");
    private static final Pattern confixBeAnKanLah = Pattern.compile("^be(?<word>" + validWord + ")([^k]an|lah|kah)$");
    private static final Pattern confixMeDiPeTeI = Pattern.compile("^(me|di|pe|te)(?<word>" + validWord + ")(i)$");
    private static final Pattern confixKeSeIKan = Pattern.compile("^(k|s)e(?<word>" + validWord + ")(i|kan)$");
    // TODO only capturing (ah|ak|er|el). strange...
    private static final Pattern confixPenPemMenMemDitDimDipAn = Pattern.compile("^([pm]e[nm]|di[tmp])(?<word>ah|ak|er|el)an$");
    private static final Pattern disallowedConfix = Pattern.compile("^(be[^r]i|(k|s)e(i|kan)|(di|me|te)[^krwylp]an)$");
    private static final Pattern particleKahLahTahPun = Pattern.compile("([klt]ah|pun)$");
    private static final Pattern possessivePronoun = Pattern.compile("([km]u|nya)$");
    private static final Pattern derivationalSuffix = Pattern.compile("(i|k?an)$");
    private static final Pattern derivationalPrefixPlain = Pattern.compile("^(di|(k|s)e)");
    private static final Pattern derivationalPrefixComplex = Pattern.compile("^(b|m|p|t)e");

    private static final Pattern prefixBerVowel = Pattern.compile("^(ber)["+vowels+"]");
    private static final Pattern prefixBerConsonantsNoR = Pattern.compile("^(ber)["+consonantsNoR+"][a-z](?!er)");
    private static final Pattern prefixBerConsonantsNoRVowels = Pattern.compile("^(ber)["+consonantsNoR+ "][a-z]er["+vowels+"]");
    private static final Pattern prefixBelajar = Pattern.compile("^(bel)ajar");
    private static final Pattern prefixBeConsonantsNoLRConsonants = Pattern.compile("^(be)["+consonantsNoLR+"]er["+consonants+"]");
    private static final Pattern prefixTerVowels = Pattern.compile("^(ter)["+vowels+"]");
    private static final Pattern prefixTerConsonantsNoRVowels = Pattern.compile("^(ter)["+consonantsNoR+"]er["+vowels+"]");
    private static final Pattern prefixTerConsonants = Pattern.compile("^(ter)["+consonants+"](?!er)");
    private static final Pattern prefixTeConsonantsNoRConsonants = Pattern.compile("^(te)["+consonantsNoR+"]er["+consonants+"]");
    private static final Pattern prefixTerConsonantsNoRConsonants = Pattern.compile("^(ter)["+consonantsNoR+"]er["+consonants+"]");
    private static final Pattern prefixMelrwyVowels = Pattern.compile("^(me)[lrwy]["+vowels+"]");
    private static final Pattern prefixMembfv = Pattern.compile("^(mem)[bfv]");
    private static final Pattern prefixMempe = Pattern.compile("^(mem)pe");
    private static final Pattern prefixMemrVowels = Pattern.compile("^(mem)(r?)["+vowels+"]");
    private static final Pattern prefixMencdsjz = Pattern.compile("^(men)[cdsjz]");
    private static final Pattern prefixMenVowels = Pattern.compile("^(men)["+vowels+"]");
    private static final Pattern prefixMengghk = Pattern.compile("^(meng)[ghqk]");
    private static final Pattern prefixMengVowels = Pattern.compile("^(meng)["+vowels+"]");
    private static final Pattern prefixMenyVowels = Pattern.compile("^(meny)["+vowels+"]");
    private static final Pattern prefixMempNoE = Pattern.compile("^(mem)p[abcdfghijklmnopqrstuvwxyz]");
    private static final Pattern prefixPewyVowels = Pattern.compile("^(pe)[wy]["+vowels+"]");
    private static final Pattern prefixPerVowels = Pattern.compile("^(per)["+vowels+"]");
    private static final Pattern prefixPerConsonantsNoR = Pattern.compile("^(per)["+consonantsNoR+"][a-z](?!er)");
    private static final Pattern prefixPerConsonantsNoRVowels = Pattern.compile("^(per)["+consonantsNoR+"][a-z]er["+vowels+"]");
    private static final Pattern prefixPembfv = Pattern.compile("^(pem)[bfv]");
    private static final Pattern prefixPemrVowels = Pattern.compile("^(pem)(r?)["+vowels+"]");
    private static final Pattern prefixPencdsjz = Pattern.compile("^(pen)[cdsjz]");
    private static final Pattern prefixPenVowels = Pattern.compile("^(pen)["+vowels+"]");
    private static final Pattern prefixPengConsonants = Pattern.compile("^(peng)["+consonants+"]");
    private static final Pattern prefixPengVowels = Pattern.compile("^(peng)["+vowels+"]");
    private static final Pattern prefixPenyVowels = Pattern.compile("^(peny)["+vowels+"]");
    private static final Pattern prefixPelVowels = Pattern.compile("^(pel)["+vowels+"]");
    private static final Pattern prefixPeSomeConsonantsVowels = Pattern.compile("^(pe)[bcdfghjkpqstvxz]er["+vowels+"]");
    private static final Pattern prefixPeSomeConsonants = Pattern.compile("^(pe)[bcdfghjkpqstvxz](?!er)");
    private static final Pattern prefixPeSomeConsonantsConsonants = Pattern.compile("^(pe)[bcdfghjkpqstvxz]er["+consonants+"]");

    private static final String lookupSql = "select lemma from dictionary where lemma = ? order by pos desc";

    /* Instance variables and methods */

    private Connection databaseConnection;
    private PreparedStatement lookupStatement;

    public IndonesianLemmaAnnotator() throws SQLException, IOException, ClassNotFoundException {
        this(false);
    }

    public IndonesianLemmaAnnotator(boolean verbose) throws SQLException, IOException, ClassNotFoundException {
        this.databaseConnection = IndonesianStanfordCoreNLP.createDatabaseConnection();
        this.verbose = verbose;
    }

    boolean lookup(IndonesianWord obj) {
        if (obj.getText().length() < 3) return false;

        // basic search
        String searchLemma = obj.getText();
        obj.setLemma(this.lookupLemmaInDatabase(searchLemma));
        if (obj.getLemma() != null) return true;

        // handle plural word
        Matcher matcher = repetitiveWord.matcher(obj.getText());
        if (matcher.matches() && matcher.group(1).equalsIgnoreCase(matcher.group(2))) {
            searchLemma = matcher.group(1);
            obj.setLemma(this.lookupLemmaInDatabase(searchLemma));
            if (obj.getLemma() != null) return true;
        }

        // handle variation of compound word (with/without space. eg: anekamasakan & aneka masakan)
        if (obj.getText().length() > 6) {
            matcher = compoundWord.matcher(obj.getText());
            if (matcher.find()) {
                searchLemma = matcher.group("first") + " " + matcher.group("second");
                obj.setLemma(this.lookupLemmaInDatabase(searchLemma));
                if (obj.getLemma() != null) return true;
            }
        }

        // If the checked word is ended with a vowel and the removed derivational suffix is -kan, there is a likely chance of overstemming;
        // So check for both possibilities: with -k or without -k, sorted by its PART OF SPEECH (verb prioritized)
        matcher = vowelsEnding.matcher(obj.getText());
        if (matcher.find() && obj.getRemovedDerivationalSuffixes().contains("kan")) {
            searchLemma = obj.getText() + "k";
            obj.setLemma(this.lookupLemmaInDatabase(searchLemma));
            if (obj.getLemma() != null) return true;
        }

        return false;
    }

    private String lookupLemmaInDatabase(String searchLemma) {
        String lemma = null;
        try {
            lookupStatement = this.databaseConnection.prepareStatement(lookupSql);
            lookupStatement.setString(1, searchLemma);
            ResultSet resultSet = lookupStatement.executeQuery();
            if (resultSet.next()) {
                lemma = resultSet.getString("lemma");
            }
        } catch (SQLException e) {
            log.error(e.getMessage(), e);
        }
        return lemma;
    }

    /**
     *  Checks input word for rule precedence
     *  If the input word has a confix: be-lah, be-an, me-i, di-i, pe-i, te-i
     *  then derivational prefix removal will be performed first
     * @param obj
     * @return
     */
    boolean checkRulePrecedence(IndonesianWord obj) {
        ArrayList<Pattern> patterns = new ArrayList<>();
        patterns.add(confixMeDiPeTeI);
        patterns.add(confixKeSeIKan);
        patterns.add(confixBeAnKanLah);
        patterns.add(confixPenPemMenMemDitDimDipAn);

        for (Pattern p: patterns) {
            Matcher matcher = p.matcher(obj.getText().toLowerCase());
            if (matcher.matches() && !"ngalam".equalsIgnoreCase(matcher.group("word"))) {
                return true;
            }
        }
        return false;
    }

    /**
     * Checks whether the input word contains disallowed affix pairs/confixes
     * @param word
     * @return
     */
    boolean hasDisallowedPair(IndonesianWord word) {
        if (!word.getRemovedDerivationalPrefixes().isEmpty() && !word.getRemovedDerivationalSuffixes().isEmpty()) {
            String pair = word.getRemovedDerivationalPrefixes().get(0) + word.getRemovedDerivationalSuffixes().get(0);
            Matcher matcher = disallowedConfix.matcher(pair);
            return matcher.matches();
        }
        return false;
    }

    /**
     * Attempts to remove inflectional suffixes from input word:
     * (particles) -kah, -lah, -tah, -pun
     * (possessive pronoun) -ku, -mu, -nya
     * @param obj
     */
    void deleteInflectionalSuffix(IndonesianWord obj) {
        HashMap<String, Pattern> patterns = new HashMap<>();
        patterns.put(IndonesianWord.REMOVABLE.PARTICLE, particleKahLahTahPun);
        patterns.put(IndonesianWord.REMOVABLE.POSSESSIVE_PRONOUN, possessivePronoun);

        String result = obj.getText();
        for (Map.Entry<String, Pattern> p: patterns.entrySet()) {
            Matcher matcher = p.getValue().matcher(result);
            if (matcher.find()) {
                obj.getRemoved(p.getKey()).add(matcher.group());
                obj.setText(matcher.replaceAll(""));
                return;
            }
        }
    }


    /**
     * Attempts to remove derivational suffixes -i, -kan, -an from input word;
     * @param obj
     */
    void deleteDerivationalSuffix(IndonesianWord obj) {
        String result = obj.getText();
        Matcher matcher = derivationalSuffix.matcher(result);
        if (matcher.find()) {
            String suffix = matcher.group();
            obj.getRemovedDerivationalSuffixes().add(suffix);
            obj.setText(matcher.replaceAll(""));
        }
    }

    /**
     * Attempts to remove derivational prefixes: di-, ke-, se-, be-, pe-, me-, pe- from input word.
     * Generally, derivational prefix is divided to 2 different groups:
     * plain (di-, ke-, se-) and
     * complex (be-,me-,pe-,te-)
     * Complex prefixes need transformation rules for certain cases in order to
     * correctly lemmatize the input word.
     */
    void deleteDerivationalPrefix(IndonesianWord obj) {
        String result = obj.getText();
        if (result.length() < 4) return;

        // get type
        String type = null;
        Matcher matcher = derivationalPrefixPlain.matcher(result);
        if (!matcher.find()) {
            matcher = derivationalPrefixComplex.matcher(result);
            type = matcher.find() ? "complex" : null;
        } else {
            type = "plain";
        }

        // ignore other type
        if (type == null) return;

        String prefix = matcher.group();
        // prevent duplicate previx removal
        if (!obj.getRemovedDerivationalPrefixes().isEmpty() && obj.getRemovedDerivationalPrefixes().contains(prefix)) {
            return;
        }

        if ("plain".equalsIgnoreCase(type)) {
            // If the prefix belongs to the 'plain' group, then immediate removal is done
            String removedPrefix = "";
            if (!obj.getRemovedDerivationalPrefixes().isEmpty()) {
                removedPrefix = obj.getRemovedDerivationalPrefixes().get(0);
            }
            if ("ke".equalsIgnoreCase(prefix)
                    && !removedPrefix.isEmpty()
                    && "di".equalsIgnoreCase(removedPrefix)
                    && !"be".equalsIgnoreCase(removedPrefix)
                    && !result.contains("tahu")
                    && !result.contains("tawa")) {
                return;
            }
            // remove prefix
            result = result.replaceFirst(prefix, "");
            // TODO redundant keys on parent and child. Strange..
            // track prefix sequence
            obj.addComplexPrefix(prefix, prefix, "");

        } else if ("complex".equalsIgnoreCase(type)) {

            boolean found = false;
            LinkedHashMap<String, String> modification = new LinkedHashMap<>();
            List<Pattern> patterns = new ArrayList<>();

            // be- rules (5)
            if ("be".equalsIgnoreCase(prefix)) {

                // If a prefix has been removed before, these rules check for
                // combination, if it is an allowed type of combination or not.
                if (!obj.getRemovedDerivationalPrefixes().isEmpty()) {
                    String prevPrefix = obj.getFirstComplexPrefix();
                    if(!"mem".equalsIgnoreCase(prevPrefix)
                            && !"pem".equalsIgnoreCase(prevPrefix)
                            && !"di".equalsIgnoreCase(prevPrefix)
                            && !"ke".equalsIgnoreCase(prevPrefix)) {
                        return;
                    }

                }

                // TODO special
                // rule #1
                // input: berV...
                // output: ber - V... | be - rV...
                matcher = prefixBerVowel.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "");
                    result = result.replaceFirst(completePrefix, "");
                    obj.addRecoding(prefix, prefix, "");
                    found = true;
                }

                // rule #2
                // input: berCAP... where C!='r' and P!='er'
                // output: ber-CAP...

                // rule #3
                // input: berCAerV... where C!= 'r'
                // output: ber-CAerV

                // rule #4
                // input: belajar
                // output: bel - ajar

                // rule #5
                // input: beC1erC2... where C1!= 'r' or 'l'
                // output: be-C1erC2
                patterns = Arrays.asList(new Pattern[] {
                        prefixBerConsonantsNoR,
                        prefixBerConsonantsNoRVowels,
                        prefixBelajar,
                        prefixBeConsonantsNoLRConsonants
                });

            }

            // te- rules (5)
            else if ("te".equalsIgnoreCase(prefix)) {

                // If a prefix has been removed before, these rules check for
                // combination, if it is an allowed type of combination or not.
                if (!obj.getRemovedDerivationalPrefixes().isEmpty()) {
                    String prevPrefix = obj.getFirstComplexPrefix();

                    if(!"ke".equalsIgnoreCase(prevPrefix)
                            && ("me".equalsIgnoreCase(prevPrefix) || "men".equalsIgnoreCase(prevPrefix) || "pen".equalsIgnoreCase(prevPrefix))
                            && !result.contains("tawa")) {
                        return;
                    }

                }

                // TODO special
                // rule #6
                // input: terV...
                // output: ter-V... | te-rV...
                matcher = prefixTerVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "");
                    result = result.replaceFirst(completePrefix, "");
                    obj.addRecoding(prefix, prefix, "");
                    found = true;
                }

                // rule #7
                // input: terCerV...
                // output: ter-CerV... where C!='r'

                // rule #8
                // input: terCerV...
                // output: ter-CerV... where C!='r'

                // rule #9
                // input: teC1erC2...
                // output: te-C1erC2... where C1!='r'

                // rule #10
                // input: terC1erC2...
                // output: ter-C1erC2... where C1!='r'

                patterns = Arrays.asList(new Pattern[] {
                        prefixTerConsonantsNoRVowels,
                        prefixTerConsonants,
                        prefixTeConsonantsNoRConsonants,
                        prefixTerConsonantsNoRConsonants
                });
            }

            // me- rules (10)
            else if ("me".equalsIgnoreCase(prefix)) {

                // This prefix cannot be a second-level prefix. If there is
                // already a removed prefix, immediately return input word.
                if (!obj.getRemovedDerivationalPrefixes().isEmpty()) {
                    return;
                }

                // TODO special
                // rule #14
                // input: mem{rV|V}...
                // output:me-m{rV|V}... | me-p{rV|V}...
                matcher = prefixMemrVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(prefix + matcher.group(2), "");
                    result = result.replaceFirst(prefix, "");
                    obj.addRecoding(prefix, completePrefix, "p");
                    found = true;
                }

                // TODO special
                // rule #16
                // input: menV...
                // output:me-tV... | me-nV...
                matcher = prefixMenVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "t");
                    result = result.replaceFirst(completePrefix, "t");
                    obj.addRecoding(prefix, prefix, "");
                    found = true;
                }

                // TODO special
                // rule #18
                // input: mengV...
                // output: meng-V... | meng-kV... | mengV-... if V='e'
                matcher = prefixMengVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "");
                    result = result.replaceFirst(completePrefix, "");
                    obj.addRecoding(prefix, completePrefix + "1", "k");
                    obj.addRecoding(prefix, completePrefix + "e", "");
                    found = true;
                }

                // TODO special
                // rule #19
                // input: menyV...
                // output: meny-sV... | me-nyV...
                matcher = prefixMenyVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(prefix, "");
                    result = result.replaceFirst(prefix, "");
                    obj.addRecoding(prefix, completePrefix, "s");
                    found = true;
                }

                // rule #11
                // input: me{l|r|w|y}V...
                // output: me-{l|r|w|y}V...

                // rule #12
                // input: mem{b|f|v}...
                // output: mem-{b|f|v}...

                // rule #13
                // input: mempe...
                // output: mem-pe..

                // rule #15
                // input: men{c|d|j|s|z}...
                // output:men-{c|dj|s|z}...

                // rule #17
                // input: meng{g|h|q|k}...
                // output: meng-{g|h|q|k}...

                // rule #20
                // input: mempA...
                // output: mem-pA... where A!='e'

                patterns = Arrays.asList(new Pattern[] {
                        prefixMelrwyVowels,
                        prefixMembfv,
                        prefixMempe,
                        prefixMencdsjz,
                        prefixMengghk,
                        prefixMempNoE,
                });

            }

            // pe- rules (15)
            else if ("pe".equalsIgnoreCase(prefix)) {

                // If a prefix has been removed before, these rules check for
                // combination, if it is an allowed type of combination or not.
                if (!obj.getRemovedDerivationalPrefixes().isEmpty()) {
                    String prevPrefix = obj.getFirstComplexPrefix();
                    if(!"di".equalsIgnoreCase(prevPrefix)
                            && !"ber".equalsIgnoreCase(prevPrefix)
                            && !"mem".equalsIgnoreCase(prevPrefix)
                            && !"se".equalsIgnoreCase(prevPrefix)
                            && !"ke".equalsIgnoreCase(prevPrefix)) {
                        return;
                    }

                }

                // TODO special
                // rule #22
                // input: perV...
                // output: per-V... | pe-rV...
                matcher = prefixPerVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "");
                    result = result.replaceFirst(completePrefix, "");
                    obj.addRecoding(prefix, prefix, "");
                    found = true;
                }

                // TODO special
                // rule #26
                // input: pem{rV|V}...
                // output: pe-m{rV|V}... | pe-p{rV|V}...
                matcher = prefixPemrVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(prefix, "");
                    result = result.replaceFirst(prefix, "");
                    obj.addRecoding(prefix, completePrefix, "p");
                    found = true;
                }

                // TODO special
                // rule #28
                // input: penV...
                // output: pe-tV... | pe-nV...
                matcher = prefixPenVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "t");
                    result = result.replaceFirst(completePrefix, "t");
                    obj.addRecoding(prefix, prefix, "");
                    found = true;
                }

                // TODO special
                // rule #30
                // input: pengV...
                // output: peng-V | peng-kV... | pengV-... if V='e'
                matcher = prefixPengVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(completePrefix, "");
                    result = result.replaceFirst(completePrefix, "");
                    obj.addRecoding(prefix, completePrefix + "1", "k");
                    obj.addRecoding(prefix, completePrefix + "e", "");
                    found = true;
                }

                // TODO special
                // rule #31
                // input: penyV...
                // output: peny-sV... | pe-nyV...
                matcher = prefixPenyVowels.matcher(result);
                if (!found && matcher.find()) {
                    String completePrefix = matcher.group(1);
                    modification.put(prefix, "");
                    result = result.replaceFirst(prefix, "");
                    obj.addRecoding(prefix, completePrefix, "s");
                    found = true;
                }

                // TODO special
                // rule #32
                // input: pelV...
                // output: pe-lV... | pel-V if 'pelajar'
                matcher = prefixPelVowels.matcher(result);
                if (!found && matcher.find()) {
                    if ("pelajar".equalsIgnoreCase(result)) {
                        String completePrefix = matcher.group(1);
                        modification.put(completePrefix, "");
                        result = result.replaceFirst(completePrefix, "");
                    } else {
                        modification.put(prefix, "");
                        result = result.replaceFirst(prefix, "");
                    }
                    found = true;
                }

                // rule #21
                // input: pe{w|y}V...
                // output: pe-{w|y}V...

                // rule #23
                // input: perCAP...
                // output: per-CAP... where C!='r' and P!='er'

                // rule #24
                // input: perCAerV...
                // output: per-CAerV... where C!= 'r'

                // rule #25
                // input: pem{b|f|v}...
                // output: pem-{b|f|v}...

                // rule #27
                // input: pen{c|d|j|z}...
                // output: pen-{c|d|j|z}...

                // rule #29
                // input: pengC...
                // output: peng-C...

                // rule #33
                // input: peCerV...
                // output: per-CerV... where C!={r|w|y|l|m|n}

                // rule #34
                // input: peCP...
                // output: pe-CP... where C!={r|w|y|l|m|n} and P!='er'
                // rule #35
                // input: peC1erC2...
                // output: pe-C1erC2... where C1!={r|w|y|l|m|n}

                patterns = Arrays.asList(new Pattern[] {
                        prefixPewyVowels,
                        prefixPerConsonantsNoR,
                        prefixPerConsonantsNoRVowels,
                        prefixPembfv,
                        prefixPencdsjz,
                        prefixPengConsonants,
                        prefixPeSomeConsonantsVowels,
                        prefixPeSomeConsonants,
                        prefixPeSomeConsonantsConsonants,
                });
            }

            if (!found) {
                for (Pattern pattern : patterns) {
                    matcher = pattern.matcher(result);
                    if (matcher.find()) {
                        String completePrefix = matcher.group(1);
                        modification.put(completePrefix, "");
                        result = result.replaceFirst(completePrefix, "");
                        found = true;
                        break;
                    }
                }
            }

            // In this case, the rule is unsuccessful, therefore the
            // original input word will be returned. The previously
            // initialized recoding chars will also be unset
            if (!found) {
                obj.getRecodingTracker().remove(prefix);
            }

            // Moves the temporary saved modification to prefix tracker
            // attribute (provided it's not null); If there is no modification
            // detected, then the this process is terminated.
            if (!modification.isEmpty()) {
                obj.addComplexPrefix(prefix, modification);
            } else {
                return;
            }

        }

        // Adds the detected prefix type to the removed affix tracker.
        obj.getRemovedDerivationalPrefixes().add(prefix);
        obj.setText(result);
    }


    /**
     * Performs recoding on input word (provided there are recoding paths available)
     */
    void recode(IndonesianWord obj) {
        String beforeRecode = obj.getText();
        List<Map.Entry<String, LinkedHashMap<String, String>>> entries = new ArrayList<>(obj.getComplexPrefixTracker().entrySet());
        Collections.reverse(entries);
        for (Map.Entry<String, LinkedHashMap<String, String>> prefixEntry:entries) {
            LinkedHashMap<String, String> changes = prefixEntry.getValue();

            if (changes.isEmpty()) continue;

            // remove prefixAdded and prepend prefixRemoved
            Map.Entry<String, String> first = changes.entrySet().iterator().next();
            String prefixAdded = first.getValue();
            String prefixRemoved = first.getKey();
            if (!prefixAdded.isEmpty()) {
                obj.setText(obj.getText().replaceFirst(prefixAdded, prefixRemoved));
            } else {
                obj.setText(prefixRemoved + obj.getText());
            }

            // If a recoding path is available, then it will be checked whether
            // there are more than one path. For every path, the word is configured
            // with the recoding path, and checked against the database.

            String prefix = prefixEntry.getKey();
            if (!obj.getRecodingTracker().containsKey(prefix)) continue;

            LinkedHashMap<String, String> recode = obj.getRecodingTracker().get(prefix);
            if (!recode.isEmpty()) {
                for (Map.Entry<String, String> recodeEntry:recode.entrySet()) {

                    // There are some cases where the recoding path is more than
                    // one, and both have identical removed value; because this
                    // can cause duplicate array keys (which will lead to overwriting),
                    // some rules are appended with numbers. Before the removed value
                    // is stored, it removes any number appended in the value
                    String remove = recodeEntry.getKey();
                    Matcher matcher = digits.matcher(remove);
                    if (matcher.find()) {
                        remove = matcher.replaceAll("");
                    }

                    // replace removed with added
                    String add = recodeEntry.getValue();
                    obj.setText(obj.getText().replaceFirst(remove, add));

                    // lookup
                    if (this.lookup(obj)) {
                        obj.addComplexPrefix(prefix, remove, add);
                        return;
                    }

                    int before = obj.getComplexPrefixTracker().size();
                    int maxIter = 3;
                    for (int i = 0; i < maxIter; i++) {
                        String prev = obj.getText();
                        this.deleteDerivationalPrefix(obj);

                        // Checks for disallowed affix combination,
                        // Checks if the lemma is already found,
                        // Checks if the no prefix was removed, or the amount of prefixes removed are already 2.
                        if (this.lookup(obj)) {
                            return;
                        } else if ((i == 0 && this.hasDisallowedPair(obj))
                                || obj.getText().equalsIgnoreCase(prev)
                                || obj.getRemovedDerivationalPrefixes().size() > maxIter) {
                            break;
                        }
                    }

                    // TODO what??
                    // remove entries added by deleteDerivationalPrefix()
                    // in removed and complexPrefixTracker
                    int after = obj.getComplexPrefixTracker().size();
                    if (after > before) {
                        List<Map.Entry<String, LinkedHashMap<String, String>>> complexPrefixEntries = new ArrayList<>(obj.getComplexPrefixTracker().entrySet());
                        for (int i = before; i < after; i++) {
                            obj.getComplexPrefixTracker().remove(complexPrefixEntries.get(i).getKey());
			    if (obj.getRemovedDerivationalPrefixes().size() > i) {
			        obj.getRemovedDerivationalPrefixes().remove(i);
			    }
                        }
                    }
                }
            }
        }
        obj.setText(beforeRecode);
    }

    /**
     * Find the lemma of the word
     * @param word
     * @return
     */
    public String lemmatize(String word) {
        IndonesianWord obj = new IndonesianWord(word);
        this.lemmatize(obj, false);
        return obj.getLemma() != null ? obj.getLemma() : obj.getOriginal();
    }

    void lemmatize(IndonesianWord obj, boolean backtrackStep) {
        String backup = obj.getText();
        if (this.lookup(obj)) return;
        int[] steps;
        if (backtrackStep) {
            steps = new int[]{ 5, 6 };
        } else {
            // Checks the rule precedence; contains True if derivational prefix
            // is performed first and False for otherwise
            if (this.checkRulePrecedence(obj)) {
                steps = new int[]{ 5, 6, 3, 4, 7 };
            } else {
                steps = new int[]{ 3, 4, 5, 6, 7 };
            }
        }

        for (int step:steps) {
            switch (step) {

                case 3:
                    this.deleteInflectionalSuffix(obj);
                    this.lookup(obj);
                    break;

                case 4:
                    this.deleteDerivationalSuffix(obj);
                    this.lookup(obj);
                    break;

                case 5:
                    int maxIter = 3;
                    for (int i = 0; i < maxIter; i++) {
                        String prev = obj.getText();
                        this.deleteDerivationalPrefix(obj);
                        this.lookup(obj);

                        // Checks for disallowed affix combination,
                        // Checks if the lemma is already found,
                        // Checks if the no prefix was removed, or the amount of prefixes removed are already 2.
                        if ((i == 0 && this.hasDisallowedPair(obj))
                                || obj.getLemma() != null
                                || obj.getText().equalsIgnoreCase(prev)
                                || obj.getRemovedDerivationalPrefixes().size() > maxIter) {
                            break;
                        }
                    }
                    break;

                case 6:
                    this.recode(obj);
                    break;

                case 7:
                    List<Map.Entry<String, LinkedHashMap<String, String>>> entries = new ArrayList<>(obj.getComplexPrefixTracker().entrySet());
                    Collections.reverse(entries);
                    for (Map.Entry<String, LinkedHashMap<String, String>> prefixEntry:entries) {
                        LinkedHashMap<String, String> changes = prefixEntry.getValue();

                        if (changes.isEmpty()) continue;

                        // remove prefixAdded and prepend prefixRemoved
                        Map.Entry<String, String> first = changes.entrySet().iterator().next();
                        String prefixAdded = first.getValue();
                        String prefixRemoved = first.getKey();
                        if (!prefixAdded.isEmpty()) {
                            obj.setText(obj.getText().replaceFirst(prefixAdded, prefixRemoved));
                        } else {
                            obj.setText(prefixRemoved + obj.getText());
                        }
                    }
                    if (this.backtrack(obj)) break;

                    // return derivational suffix
                    if (!obj.getRemovedDerivationalSuffixes().isEmpty()) {
                        if (obj.getRemovedDerivationalSuffixes().contains("kan")) {
                            obj.setText(obj.getText() + "k");
                            if (this.backtrack(obj)) break;
                            obj.setText(obj.getText() + "an");
                        } else {
                            obj.setText(obj.getText() + obj.getRemovedDerivationalSuffixes().get(0));
                        }
                        if (this.backtrack(obj)) break;
                    }

                    // return possessive pronoun
                    if (!obj.getRemovedPossesivePronouns().isEmpty()) {
                        obj.setText(obj.getText() + obj.getRemovedPossesivePronouns().get(0));
                        if (this.backtrack(obj)) break;
                    }

                    // return particle
                    if (!obj.getRemovedParticles().isEmpty()) {
                        obj.setText(obj.getText() + obj.getRemovedParticles().get(0));
                        if (this.backtrack(obj)) break;
                    }
                    break;
            }

            if (obj.getLemma() != null) return;
        }
        log.debug("Out of steps. Reverting backup: " + backup);
        obj.setText(backup);
    }
    private boolean backtrack(IndonesianWord obj) {
        obj.clearRemovedDerivationalPrefixes();
        obj.clearComplexPrefixTracker();
        this.lemmatize(obj, true);
        return obj.getLemma() != null;
    }

    @Override
    public void annotate(Annotation annotation) {
        if (this.verbose) {
            log.info("Finding lemmas ...");
        }
        if (annotation.containsKey(CoreAnnotations.SentencesAnnotation.class)) {
            for (CoreMap sentence : annotation.get(CoreAnnotations.SentencesAnnotation.class)) {
                List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);
                for (CoreLabel token : tokens) {
                    String text = token.get(CoreAnnotations.TextAnnotation.class);
                    String posTag = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
                    String lemma = null;
                    if (!posTag.equalsIgnoreCase("NNP")) {
                        lemma = this.lemmatize(text);
                    }
                    token.set(CoreAnnotations.LemmaAnnotation.class, lemma);
                }
            }
        } else {
            throw new RuntimeException("Unable to find words/tokens in: " +
                    annotation);
        }
    }

    @Override
    public Set<Class<? extends CoreAnnotation>> requires() {
        return Collections.unmodifiableSet(new ArraySet<>(Arrays.asList(
                CoreAnnotations.TextAnnotation.class,
                CoreAnnotations.TokensAnnotation.class,
                CoreAnnotations.SentencesAnnotation.class,
                CoreAnnotations.PartOfSpeechAnnotation.class
        )));
    }

    @Override
    public Set<Class<? extends CoreAnnotation>> requirementsSatisfied() {
        return Collections.singleton(CoreAnnotations.LemmaAnnotation.class);
    }

}


class IndonesianWord {

    interface REMOVABLE {
        String PARTICLE = "particle";
        String POSSESSIVE_PRONOUN = "possessivePronoun";
        String DERIVATIONAL_PREFIX = "derivationalPrefix";
        String DERIVATIONAL_SUFFIX = "derivationalSuffix";
    }

    private final String original;
    private String text;
    private String lemma;
    private Map<String, List<String>> removed;
    private LinkedHashMap<String, LinkedHashMap<String, String>> recodingTracker;
    private LinkedHashMap<String, LinkedHashMap<String, String>> complexPrefixTracker;

    public IndonesianWord(String original) throws IllegalArgumentException {
        if (original == null || original.isEmpty()) throw new IllegalArgumentException("Null or empty string argument");
        this.original = original;
        this.text = original.toLowerCase();
        this.removed = new HashMap<>();
        this.removed.put(REMOVABLE.PARTICLE, new ArrayList<>());
        this.removed.put(REMOVABLE.POSSESSIVE_PRONOUN, new ArrayList<>());
        this.removed.put(REMOVABLE.DERIVATIONAL_PREFIX, new ArrayList<>());
        this.removed.put(REMOVABLE.DERIVATIONAL_SUFFIX, new ArrayList<>());
        this.recodingTracker = new LinkedHashMap<>();
        this.complexPrefixTracker = new LinkedHashMap<>();
        this.lemma = null;
    }

    public String getOriginal() {
        return original;
    }

    public String getLemma() {
        return lemma;
    }

    public Map<String, List<String>> getRemoved() {
        return removed;
    }

    public LinkedHashMap<String, LinkedHashMap<String, String>> getRecodingTracker() {
        return recodingTracker;
    }

    public LinkedHashMap<String, LinkedHashMap<String, String>> getComplexPrefixTracker() {
        return complexPrefixTracker;
    }

    public void setLemma(String lemma) {
        if (lemma != null) {
            if ("".equalsIgnoreCase(lemma.trim())) throw new IllegalArgumentException("Should not be empty string");
        }
        this.lemma = lemma;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public List<String> getRemovedDerivationalPrefixes() {
        return this.getRemoved(REMOVABLE.DERIVATIONAL_PREFIX);
    }

    public List<String> getRemovedDerivationalSuffixes() {
        return this.getRemoved(REMOVABLE.DERIVATIONAL_SUFFIX);
    }

    public List<String> getRemovedParticles() {
        return this.getRemoved(REMOVABLE.PARTICLE);
    }

    public List<String> getRemovedPossesivePronouns() {
        return this.getRemoved(REMOVABLE.POSSESSIVE_PRONOUN);
    }

    public List<String> getRemoved(String key) {
        List<String> list = null;
        if (this.removed.containsKey(key)) {
            list = this.removed.get(key);
        }
        return list;
    }

    public void clearRemovedDerivationalPrefixes() {
        this.removed.put(REMOVABLE.DERIVATIONAL_PREFIX, new ArrayList<>());
    }

    public void clearComplexPrefixTracker() {
        this.complexPrefixTracker = new LinkedHashMap<>();
    }

    public String getFirstComplexPrefix() {
        String prevPrefix = null;
        if (!complexPrefixTracker.isEmpty()) {
            LinkedHashMap<String, String> tracker = complexPrefixTracker.values().iterator().next();
            if (!tracker.isEmpty()) {
                prevPrefix = tracker.keySet().iterator().next();
            }
        }
        return prevPrefix;
    }

    public void addComplexPrefix(String head, String key, String value) {
        if (!this.complexPrefixTracker.containsKey(head)) {
            LinkedHashMap<String, String> prefixTracker = new LinkedHashMap<>();
            prefixTracker.put(key, value);
            this.complexPrefixTracker.put(head, prefixTracker);
        } else {
            this.complexPrefixTracker.get(head).put(key, value);
        }
    }

    public void addComplexPrefix(String head, LinkedHashMap<String, String> prefixTracker) {
        this.complexPrefixTracker.put(head, prefixTracker);
    }

    public void addRecoding(String head, String key, String value) {
        if (!this.recodingTracker.containsKey(head)) {
            LinkedHashMap<String, String> recoding = new LinkedHashMap<>();
            recoding.put(key, value);
            this.recodingTracker.put(head, recoding);
        } else {
            this.recodingTracker.get(head).put(key, value);
        }
    }

}
