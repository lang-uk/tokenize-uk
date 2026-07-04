package org.languagetool.tokenizers;
import java.util.List;
public interface Tokenizer {
  List<String> tokenize(String text);
}
