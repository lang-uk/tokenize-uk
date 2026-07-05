import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.languagetool.tokenizers.uk.UkrainianWordTokenizer;

public class Driver {
  public static void main(String[] args) throws Exception {
    UkrainianWordTokenizer tokenizer = new UkrainianWordTokenizer();
    String sep = String.valueOf((char) 1);
    BufferedReader reader = new BufferedReader(
        new InputStreamReader(System.in, StandardCharsets.UTF_8));
    PrintStream out = new PrintStream(System.out, false, "UTF-8");
    String line;
    while ((line = reader.readLine()) != null) {
      List<String> tokens = tokenizer.tokenize(line);
      out.println(String.join(sep, tokens));
    }
    out.flush();
  }
}
