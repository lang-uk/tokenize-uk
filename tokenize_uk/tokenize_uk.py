import regex as re

SPLIT_CHARS: str = (
    "(!{2,3}|\\?{2,3}|\\.{3}|[!?][!?.]{1,2}" + "|[\u0020\u00A0\\n\\r\\t"
    ",.;!?\u2014:()\\[\\]{}<>/|\\\\…°$€₴=¿¡]"  # what about: №§
    + "|%(?![-\u2013][а-яіїєґ])"  # allow 5%-й
    + '|(?<!\uE109)["«»„”“]'
    + "|[\u2000-\u200F"  # quotes have special cases
    + "\u201A\u2020-\u202F\u2030\u2031\u2033-\u206F"
    + "\u2400-\u27FF"  # TODO: Verify Control Pictures
    # + String.valueOf(Character.toChars(0x1F000))
    + chr(0x1F000) + "-"
    # + String.valueOf(Character.toChars(0x1FFFF))  # TODO: Verify Emojis
    + chr(0x1FFFF) + "\uf000-\uffff" + "\uE110])(?!\uE120)"  # private unicode area: U+E000..U+F8FF
)


# As per https://perldoc.perl.org/perlrecharclass#Whitespace
VERTICAL_SPACE: str = "\u000a\u000b\u000c\u000d\u0085\u2028\u2029"
HORIZONTAL_SPACE: str = (
    "\u0009\u0020\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000"
)

SPLIT_CHARS_REGEX: re.Pattern = re.compile(SPLIT_CHARS)

DECIMAL_COMMA_SUBST: str = "\uE001"  # some unused character to hide comma in decimal number temporary for tokenizer run
NON_BREAKING_SPACE_SUBST: str = "\uE002"
NON_BREAKING_DOT_SUBST: str = "\uE003"  # some unused character to hide dot in date temporary for tokenizer run
NON_BREAKING_COLON_SUBST: str = "\uE004"
LEFT_BRACE_SUBST: str = "\uE005"
RIGHT_BRACE_SUBST: str = "\uE006"
NON_BREAKING_SLASH_SUBST: str = "\uE007"  # hide slash in с/г
LEFT_ANGLE_SUBST: str = "\uE008"
RIGHT_ANGLE_SUBST: str = "\uE009"
SLASH_SUBST: str = "\uE010"
NON_BREAKING_PLACEHOLDER: str = "\uE109"
BREAKING_PLACEHOLDER: str = "\uE110"
NON_BREAKING_PLACEHOLDER2: str = "\uE120"

NON_BREAKING_BREAKING_PLACEHOLDER: str = f"{NON_BREAKING_PLACEHOLDER2}{BREAKING_PLACEHOLDER}"


WEIRD_APOSTROPH_PATTERN: re.Pattern = re.compile('([бвджзклмнпрстфхш])(["\u201D\u201F`´])([єїюя])', re.I | re.U)

WORDS_WITH_BRACKETS_PATTERN: re.Pattern = re.compile("([а-яіїєґ])\\[([а-яіїєґ]+)\\]", re.I | re.U)

# decimal comma between digits
DECIMAL_COMMA_PATTERN: re.Pattern = re.compile("([\\d]),([\\d])", re.I | re.U)
DECIMAL_COMMA_REPL = rf"\1{DECIMAL_COMMA_SUBST}\2"

# space between digits
DECIMAL_SPACE_PATTERN: re.Pattern = re.compile(
    "(?<=^|["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "(])\\d{1,3}(["
    + HORIZONTAL_SPACE
    + "][\\d]{3})+(?=["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "(]|$)",
    re.I | re.U,
)

# numbers with n-dash
DASH_NUMBERS_PATTERN: re.Pattern = re.compile("([IVXІХ]+)([\u2013-])([IVXІХ]+)")
DASH_NUMBERS_REPL: str = rf"\1{BREAKING_PLACEHOLDER}\2{BREAKING_PLACEHOLDER}\3"
N_DASH_SPACE_PATTERN: re.Pattern = re.compile(
    "([а-яіїєґa-z0-9])(\u2013[" + HORIZONTAL_SPACE + "])(?!(та|чи|і|й)[" + HORIZONTAL_SPACE + VERTICAL_SPACE + "])",
    re.I | re.U,
)
N_DASH_SPACE_PATTERN2: re.Pattern = re.compile("([" + HORIZONTAL_SPACE + ".,;!?]\u2013)([а-яіїєґa-z])", re.I | re.U)
N_DASH_SPACE_REPL: str = rf"\1{BREAKING_PLACEHOLDER}\2"

# dots in numbers
DOTTED_NUMBERS_PATTERN: re.Pattern = re.compile(r"([\d])\.([\d])")
DOTTED_NUMBERS_PATTERN3: re.Pattern = re.compile(r"([\d])\.([\d]+)\.([\d])")

DOTTED_NUMBERS_REPL: str = rf"\1{NON_BREAKING_DOT_SUBST}\2"

# colon in numbers
COLON_NUMBERS_PATTERN: re.Pattern = re.compile(r"([\d]):([\d])")
COLON_NUMBERS_REPL: str = rf"\1{NON_BREAKING_COLON_SUBST}\2"

# dates
DATE_PATTERN: re.Pattern = re.compile(
    r"([\d]{2})\.([\d]{2})\.([\d]{4})|([\d]{4})\.([\d]{2})\.([\d]{2})|([\d]{4})-([\d]{2})-([\d]{2})",
    re.I | re.U,
)
DATE_PATTERN_REPL: str = rf"\1{NON_BREAKING_DOT_SUBST}\2{NON_BREAKING_DOT_SUBST}\3"

# braces in words
BRACE_IN_WORD_PATTERN: re.Pattern = re.compile("([а-яіїєґ])\\(([а-яіїєґ']+)\\)", re.I | re.U)

XML_TAG_PATTERN: re.Pattern = re.compile("<(/?[a-z_]+/?)>", re.I)

# abbreviation dot
ABBR_DOT_VO_PATTERN1: re.Pattern = re.compile("([вВу])\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*о)\\.")
ABBR_DOT_VO_PATTERN2: re.Pattern = re.compile("(к)\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*с)\\.")
ABBR_DOT_VO_PATTERN3: re.Pattern = re.compile("(ч|ст)\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*л)\\.")
# ABBR_DOT_VO_PATTERN4: re.Pattern = re.compile("(р)\\.([\\s\u00A0\u202F]*х)\\.")
ABBR_DOT_TYS_PATTERN1: re.Pattern = re.compile("([0-9IІ][" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]+)(тис|арт)\\.")
ABBR_DOT_TYS_PATTERN2: re.Pattern = re.compile("(тис|арт)\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]+[а-яіїєґ0-9])")
ABBR_DOT_ART_PATTERN: re.Pattern = re.compile("([Аа]рт|[Мм]ал|[Рр]ис)\\.([" + HORIZONTAL_SPACE + "]*[0-9])")
ABBR_DOT_MAN_PATTERN: re.Pattern = re.compile("(Ман)\\.([" + HORIZONTAL_SPACE + "]*(Сіті|[Юю]н))")
ABBR_DOT_LAT_PATTERN: re.Pattern = re.compile(
    "([^а-яіїєґА-ЯІЇЄҐ'\u0301-]лат)\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]+[a-zA-Z])"
)
ABBR_DOT_PROF_PATTERN: re.Pattern = re.compile(
    "(?<![а-яіїєґА-ЯІЇЄҐ'\u0301-])([Аа]кад|[Пп]роф|[Дд]оц|[Аа]сист|[Аа]рх|тов|вул|о|р|ім|упоряд|[Пп]реп|Ів|Дж)\\.(["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "]+[А-ЯІЇЄҐа-яіїєґ])"
)
ABBR_DOT_GUB_PATTERN: re.Pattern = re.compile(
    "(.[А-ЯІЇЄҐ][а-яіїєґ'-]+[" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]+губ)\\."
)
ABBR_DOT_DASH_PATTERN: re.Pattern = re.compile(r"\b([А-ЯІЇЄҐ]ж?)\.([-\u2013]([А-ЯІЇЄҐ][а-яіїєґ']{2}|[А-ЯІЇЄҐ]\.))")


# tokenize initials with dot before last name, e.g. "А.", "Ковальчук"
INITIALS_DOT_PATTERN_SP_2: re.Pattern = re.compile(
    r"([А-ЯІЇЄҐ])\.(["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + r"]{0,5}[А-ЯІЇЄҐ])\.(["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "]{0,5}[А-ЯІЇЄҐ][а-яіїєґ']+)"
)
INITIALS_DOT_PATTERN_SP_1: re.Pattern = re.compile(
    r"([А-ЯІЇЄҐ])\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]{0,5}[А-ЯІЇЄҐ][а-яіїєґ']+)"
)

# tokenize initials with dot after last name, e.g.  "Ковальчук", "А."
INITIALS_DOT_PATTERN_RSP_2: re.Pattern = re.compile(
    "([А-ЯІЇЄҐ][а-яіїєґ']+)(["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + r"]?[А-ЯІЇЄҐ])\.(["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + r"]?[А-ЯІЇЄҐ])\."
)
INITIALS_DOT_PATTERN_RSP_1: re.Pattern = re.compile(
    "([А-ЯІЇЄҐ][а-яіїєґ']+)([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]?[А-ЯІЇЄҐ])\."
)

INITIALS_DOT_REPL_SP_2: str = (
    rf"\1{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\2{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\3"
)
INITIALS_DOT_REPL_SP_1: str = rf"\1{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\2"
INITIALS_DOT_REPL_RSP_2: str = rf"\1{BREAKING_PLACEHOLDER}\2{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\3{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}"
INITIALS_DOT_REPL_RSP_1: str = rf"\1{BREAKING_PLACEHOLDER}\2{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}"

# село, місто, річка (якщо з цифрою: секунди, метри, роки) - з роками складно
ABBR_DOT_INVALID_DOT_PATTERN: re.Pattern = re.compile("((?:[0-9]|кв\\.|куб\\.)[\\s\u00A0\u202F]+(?:[смкд]|мк)?м)\\.(.)")
ABBR_DOT_KUB_SM_PATTERN: re.Pattern = re.compile(
    "(кв|куб)\\.([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*(?:[смкд]|мк)?м)"
)
ABBR_DOT_S_G_PATTERN: re.Pattern = re.compile(r"(с)\.(-г)\.")
ABBR_DOT_PN_ZAH_PATTERN: re.Pattern = re.compile(r"(пн|пд)\.(-(зах|сх))\.")
ABBR_DOT_2_SMALL_LETTERS_PATTERN: re.Pattern = re.compile(r"([^а-яіїєґА-ЯІЇЄҐ'\u0301-][векнпрстцч]{1,2})\.([" + HORIZONTAL_SPACE +r"]*(?![смкд]?м\.)[екмнпрстч]{1,2})\.")
ABBR_DOT_2_SMALL_LETTERS_REPL: str = (
    rf"\1{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\2{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}"
)
INVALID_MLN_DOT_PATTERN: re.Pattern = re.compile(r"(млн|млрд)\.( [а-яіїєґ])")

ONE_DOT_TWO_REPL: str = rf"\1{NON_BREAKING_DOT_SUBST}{BREAKING_PLACEHOLDER}\2"

# скорочення що не можуть бути в кінці речення
ABBR_DOT_NON_ENDING_PATTERN: re.Pattern = re.compile(
      r"(?<![а-яіїєґА-ЯІЇЄҐ'\u0301-])(абз|австрал|амер|англ|акад(ем)?|арк|ауд|бл(?:изьк)?|буд|в(?!\.+)|вип|вірм|грец(?:ьк)"
    + r"|держ|див|діал|дод|дол|досл|доц|доп|екон|ел|жін|зав|заст|зах|зб|зв|зневажл?|зовн|ім|івр|ісп|іст|італ"
    + r"|к|каб|каф|канд|кв|[1-9]-кімн|кімн|кл|кн|коеф|латин|мал|моб|н|[Нн]апр|нац|образн|оп|оф|п|пен|перекл|перен|пл|пол|пов|пор|поч|пп|прибл|прикм|прим|присл|пров|пром|просп"
    + r"|[Рр]ед|[Рр]еж|розд|розм|рт|рум|с|[Сс]вв?|скор|соц|співавт|[сС]т|стор|сх|табл|тт|[тТ]ел|техн|укр|філол|фр|франц|худ|ч|чайн|част|ц|яп)\.(?!" + NON_BREAKING_PLACEHOLDER2 + r"|\.+["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "]*$)"
)

  # private static final Pattern ABBR_DOT_NON_ENDING_PATTERN = Pattern.compile(
  #       "(?<![а-яіїєґА-ЯІЇЄҐ'\u0301-])(абз|австрал|амер|англ|акад(ем)?|арк|ауд|бл(?:изьк)?|буд|в(?!\\.+)|вип|вірм|грец(?:ьк)"
  #     + "|держ|див|діал|дод|дол|досл|доц|доп|екон|ел|жін|зав|заст|зах|зб|зв|зневажл?|зовн|ім|івр|ісп|іст|італ"
  #     + "|к|каб|каф|канд|кв|[1-9]-кімн|кімн|кл|кн|коеф|латин|мал|моб|н|[Нн]апр|нац|образн|оп|оф|п|пен|перекл|перен|пл|пол|пов|пор|поч|пп|прибл|прикм|прим|присл|пров|пром|просп"
  #     + "|[Рр]ед|[Рр]еж|розд|розм|рт|рум|с|[Сс]вв?|скор|соц|співавт|[сС]т|стор|сх|табл|тт|[тТ]ел|техн|укр|філол|фр|франц|худ|ч|чайн|част|ц|яп)\\.(?!\uE120|\\.+[\\h\\v]*$)");


ABBR_DOT_NON_ENDING_PATTERN_2: re.Pattern = re.compile(
    r"([^а-яіїєґА-ЯІЇЄҐ'-]м\.)([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*[А-ЯІЇЄҐ])"
)

# скорочення що можуть бути в кінці речення
ABBR_DOT_ENDING_PATTERN: re.Pattern = re.compile(
    rf"([^а-яіїєґА-ЯІЇЄҐ'\u0301-]((та|й|і) (інш?|под)|атм|відс|гр|коп|обл|р|рр|РР|руб|ст|стол|стор|чол|шт))\.(?!{NON_BREAKING_PLACEHOLDER2})"
)
ABBR_DOT_I_T_P_PATTERN: re.Pattern = re.compile(
    "([ій][" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]+т\.)([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]*(д|п|ін)\.)"
)

ABBR_DOT_I_T_CH_PATTERN: re.Pattern = re.compile("([ву][" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]+т\.)([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]*ч\.)")

ABBR_DOT_T_ZV_PATTERN: re.Pattern = re.compile(
    "([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]+т\.)([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]*зв\.)"
)

ABBR_AT_THE_END: re.Pattern = re.compile(
    r"(?<![а-яіїєґА-ЯІЇЄҐ'\u0301])(тис|губ|[А-ЯІЇЄҐ])\.[" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*$"
)

APOSTROPHE_BEGIN_PATTERN: re.Pattern = re.compile(
    "(^|[" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"(„«\"'])'(?!дно)(\p{L})"
)
APOSTROPHE_END_PATTER: re.Pattern = re.compile(
    r"(\p{L})(?<!\b(?:мо|тре|тра|чо|нічо|бо|зара|пра))'([^\p{L}-]|$)", re.I | re.U
)

YEAR_WITH_R: re.Pattern = re.compile(r"((?:[12][0-9]{3}[—–-])?[12][0-9]{3})(рр?\.)")

COMPOUND_WITH_QUOTES1: re.Pattern = re.compile('([а-яіїє]-)([«"„])([а-яіїєґ\'-]+)([»"“])', re.I | re.U)
COMPOUND_WITH_QUOTES2: re.Pattern = re.compile(r'([«"„])([а-яіїєґ0-9\'-]+)([»\"“])(-[а-яіїє])', re.I | re.U)

# Сьогодні (у четвер. - Ред.), вранці.
ABBR_DOT_PATTERN8: re.Pattern = re.compile(r"([\s\u00A0\u202F]+[–—-][\s\u00A0\u202F]+(?:[Рр]ед|[Аа]вт))\.([\)\]])")
ABBR_DOT_RED_AVT_PATTERN: re.Pattern = re.compile(
    "([" + HORIZONTAL_SPACE + VERTICAL_SPACE + r"]+(?:[Рр]ед|[Аа]вт))\.([\)\]])"
)

SOFT_HYPHEN_WRAP: str = "\u00AD\n"
SOFT_HYPHEN_WRAP_SUBST: str = "\uE103"

# url
URL_PATTERN: re.Pattern = re.compile(
    "((https?|ftp)://|www\\.)[^"
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "/$.?#),]+\\.[^"
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + '),">]*|(mailto:)?[\\p{L}\\d._-]+@[\\p{L}\\d_-]+(\\.[\\p{L}\\d_-]+)+',
    re.I,
)
URL_START_REPLACE_CHAR: int = 0xE300
LEADING_DASH_PATTERN: re.Pattern = re.compile("^([\u2014\u2013])([а-яіїєґА-ЯІЇЄҐA-Z])")
LEADING_DASH_PATTERN_2: re.Pattern = re.compile("^(-)([А-ЯІЇЄҐA-Z])")

NUMBER_MISSING_SPACE: re.Pattern = re.compile(
    "((?:["
    + HORIZONTAL_SPACE
    + VERTICAL_SPACE
    + "\uE110]|^)(?!(?:[кдсмн]|мк)?м[23])[а-яїієґА-ЯІЇЄҐ'-]*[а-яїієґ]'?[а-яїієґ])([0-9]+(?![а-яіїєґА-ЯІЇЄҐa-zA-Z»\"“]))"
)


class UkrainianWordTokenizer:
    def tokenize(self, text: str) -> list[str]:
        urls: dict[str, str] = {}
        if text.strip():
            text, urls = self.adjust_text_for_tokenizing(text)

        token_list: list[str] = []

        tokens: list[str] = self.split_with_delimiters(text, SPLIT_CHARS_REGEX)

        for token in tokens:
            if token == BREAKING_PLACEHOLDER:
                continue

            token = token.replace(DECIMAL_COMMA_SUBST, ",")

            token = token.replace(NON_BREAKING_SLASH_SUBST, "/")
            token = token.replace(NON_BREAKING_COLON_SUBST, ":")
            token = token.replace(NON_BREAKING_SPACE_SUBST, " ")

            token = token.replace(LEFT_BRACE_SUBST, "(")
            token = token.replace(RIGHT_BRACE_SUBST, ")")

            token = token.replace(LEFT_ANGLE_SUBST, "<")
            token = token.replace(RIGHT_ANGLE_SUBST, ">")
            token = token.replace(SLASH_SUBST, "/")

            # outside of if as we also replace back sentence-ending abbreviations
            token = token.replace(NON_BREAKING_DOT_SUBST, ".")

            token = token.replace(SOFT_HYPHEN_WRAP_SUBST, SOFT_HYPHEN_WRAP)

            token = token.replace(NON_BREAKING_PLACEHOLDER, "")
            token = token.replace(NON_BREAKING_PLACEHOLDER2, "")

            for k, v in urls.items():
                token = token.replace(k, v)

            token_list.append(token)

        return token_list

    def adjust_text_for_tokenizing(self, text: str) -> tuple[str, dict[str, str]]:
        urls: dict[str, str] = {}
        text = self.cleanup(text)

        if text[0] in "\u2014\u2013-":
            if LEADING_DASH_PATTERN.search(text):
                text = LEADING_DASH_PATTERN.sub(rf"\1{BREAKING_PLACEHOLDER}\2", text, count=1)
            else:
                if LEADING_DASH_PATTERN_2.search(text):
                    text = LEADING_DASH_PATTERN_2.sub(rf"\1{BREAKING_PLACEHOLDER}\2", text, count=1)

        if "," in text:
            text = DECIMAL_COMMA_PATTERN.sub(DECIMAL_COMMA_REPL, text)

        # check for urls
        if "http" in text or "www" in text or "@" in text or "ftp" in text:  # https?|ftp
            # Matcher matcher = URL_PATTERN.matcher(text)
            url_replace_char: int = URL_START_REPLACE_CHAR
            match = URL_PATTERN.search(text)

            # TODO: barely efficient, rewrite with re.sub callback?
            while match:
                replace_char: str = chr(url_replace_char)
                urls[replace_char] = match.group()
                text = URL_PATTERN.sub(replace_char, text, count=1)
                url_replace_char += 1
                match = URL_PATTERN.search(text)

        if "\u2014" in text:
            text = re.sub(
                "\u2014([" + HORIZONTAL_SPACE + VERTICAL_SPACE + "])", f"{BREAKING_PLACEHOLDER}\u2014\\1", text
            )

        ndash_present: bool = "\u2013" in text
        if "-" in text or ndash_present:
            text = DASH_NUMBERS_PATTERN.sub(DASH_NUMBERS_REPL, text)
            if ndash_present:
                text = N_DASH_SPACE_PATTERN.sub(N_DASH_SPACE_REPL, text)
                text = N_DASH_SPACE_PATTERN2.sub(N_DASH_SPACE_REPL, text)

        if "с/г" in text:
            text = text.replace("с/г", f"с{NON_BREAKING_SLASH_SUBST}г")

        if "Л/ДНР" in text:
            text = text.replace("Л/ДНР", f"Л{NON_BREAKING_SLASH_SUBST}ДНР")

        if "р." in text:
            text = YEAR_WITH_R.sub(rf"\1{BREAKING_PLACEHOLDER}\2", text)

        # leave only potential hashtags together
        # TODO: difference between replace and replaceAll.
        text = text.replace("#", BREAKING_PLACEHOLDER + "#")

        # leave numbers with following % together
        if "%" in text:
            text = re.sub(r"%([^-])", rf"%{BREAKING_PLACEHOLDER}\1", text)

        text = COMPOUND_WITH_QUOTES1.sub(rf"\1\2{NON_BREAKING_PLACEHOLDER2}\3{NON_BREAKING_PLACEHOLDER2}\4{NON_BREAKING_PLACEHOLDER2}", text)
        text = COMPOUND_WITH_QUOTES2.sub(rf"\1{NON_BREAKING_PLACEHOLDER2}\2{NON_BREAKING_PLACEHOLDER2}\3{NON_BREAKING_PLACEHOLDER2}\4", text)
        if "[" in text:
            text = WORDS_WITH_BRACKETS_PATTERN.sub(rf"\1[{NON_BREAKING_PLACEHOLDER2}\2]{NON_BREAKING_PLACEHOLDER2}", text)

        # if period is not the last character in the sentence
        try:
            dot_index: int = text.index(".")
        except ValueError:
            dot_index = -1

        text_rtrimmed: str = re.sub("[" + HORIZONTAL_SPACE + VERTICAL_SPACE + "]*$", "", text)
        dot_inside_sentence: bool = dot_index >= 0 and dot_index < len(text_rtrimmed) - 1

        if (
            dot_inside_sentence or dot_index == len(text_rtrimmed) - 1 and ABBR_AT_THE_END.search(text)
        ):  # ugly - special case for тис. та ініціалів
            text = DATE_PATTERN.sub(DATE_PATTERN_REPL, text)

            text = DOTTED_NUMBERS_PATTERN3.sub(rf"\1.{NON_BREAKING_PLACEHOLDER2}\2.{NON_BREAKING_PLACEHOLDER2}\3", text)
            text = DOTTED_NUMBERS_PATTERN.sub(rf"\1.{NON_BREAKING_PLACEHOLDER2}\2", text)

            text = ABBR_DOT_2_SMALL_LETTERS_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}\2.{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_VO_PATTERN1.sub(ABBR_DOT_2_SMALL_LETTERS_REPL, text)
            text = ABBR_DOT_VO_PATTERN2.sub(ABBR_DOT_2_SMALL_LETTERS_REPL, text)
            text = ABBR_DOT_VO_PATTERN3.sub(ABBR_DOT_2_SMALL_LETTERS_REPL, text)
            text = ABBR_DOT_ART_PATTERN.sub(ONE_DOT_TWO_REPL, text)
            text = ABBR_DOT_MAN_PATTERN.sub(ONE_DOT_TWO_REPL, text)
            text = ABBR_DOT_TYS_PATTERN1.sub("\\1\\2" + NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER, text)
            text = ABBR_DOT_TYS_PATTERN2.sub(ONE_DOT_TWO_REPL, text)
            text = ABBR_DOT_LAT_PATTERN.sub(ONE_DOT_TWO_REPL, text)
            text = ABBR_DOT_PROF_PATTERN.sub(ONE_DOT_TWO_REPL, text)
            text = ABBR_DOT_GUB_PATTERN.sub("\\1" + NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER, text)
            text = ABBR_DOT_DASH_PATTERN.sub("\\1" + NON_BREAKING_DOT_SUBST + "\\2", text)

            text = INITIALS_DOT_PATTERN_SP_2.sub(INITIALS_DOT_REPL_SP_2, text)
            text = INITIALS_DOT_PATTERN_SP_1.sub(INITIALS_DOT_REPL_SP_1, text)
            text = INITIALS_DOT_PATTERN_RSP_2.sub(INITIALS_DOT_REPL_RSP_2, text)
            text = INITIALS_DOT_PATTERN_RSP_1.sub(INITIALS_DOT_REPL_RSP_1, text)

            text = ABBR_DOT_KUB_SM_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}\2", text)
            text = ABBR_DOT_S_G_PATTERN.sub(
                "\\1" + NON_BREAKING_DOT_SUBST + "\\2" + NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER, text
            )
            text = ABBR_DOT_PN_ZAH_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}\2.{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_I_T_P_PATTERN.sub(rf"\1{NON_BREAKING_BREAKING_PLACEHOLDER}\2{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_I_T_CH_PATTERN.sub(rf"\1{NON_BREAKING_BREAKING_PLACEHOLDER}\2{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_T_ZV_PATTERN.sub(rf"\1{NON_BREAKING_BREAKING_PLACEHOLDER}\2{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_RED_AVT_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}\2", text)
            text = ABBR_DOT_NON_ENDING_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}", text)
            text = ABBR_DOT_NON_ENDING_PATTERN_2.sub(rf"\1{NON_BREAKING_BREAKING_PLACEHOLDER}\2", text)
            text = INVALID_MLN_DOT_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}\2", text)

        # preserve * inside words (sometimes used instead of apostrophe or to mask profane words)
        # but split if it's the beginning or end of the word (often used for mark-up and footnotes)
        if "*" in text:
            text = re.sub("((?:^|[^а-яіїєґА-ЯІЇЄҐ])\\*+)([а-яіїєґА-ЯІЇЄҐ])", "\\1" + BREAKING_PLACEHOLDER + "\\2", text)
            text = re.sub("([а-яіїєґА-ЯІЇЄҐ])(\\*+(?:[^а-яіїєґА-ЯІЇЄҐ]|$))", "\\1" + BREAKING_PLACEHOLDER + "\\2", text)

        text = ABBR_DOT_ENDING_PATTERN.sub(rf"\1.{NON_BREAKING_BREAKING_PLACEHOLDER}", text)

        # 2 000 000
        text = DECIMAL_SPACE_PATTERN.sub(
            lambda m: m.group(0)
            .replace(" ", NON_BREAKING_SPACE_SUBST)
            .replace("\u00A0", NON_BREAKING_SPACE_SUBST)
            .replace("\u202F", NON_BREAKING_SPACE_SUBST),
            text,
        )

        # Matcher spacedDecimalMatcher = DECIMAL_SPACE_PATTERN.matcher(text);
        # if( spacedDecimalMatcher.find() ) {
        #     StringBuffer sb = new StringBuffer();
        #     do {
        #         String splitNumber = spacedDecimalMatcher.group(0);
        #         String splitNumberAdjusted = splitNumber.replace(' ', NON_BREAKING_SPACE_SUBST);
        #         splitNumberAdjusted = splitNumberAdjusted.replace('\u00A0', NON_BREAKING_SPACE_SUBST);
        #         splitNumberAdjusted = splitNumberAdjusted.replace('\u202F', NON_BREAKING_SPACE_SUBST);
        #         spacedDecimalMatcher.appendReplacement(sb, splitNumberAdjusted);
        #     } while( spacedDecimalMatcher.find() );

        #     spacedDecimalMatcher.appendTail(sb);
        #     text = sb.toString();
        # }

        # 12:25
        if ":" in text:
            text = COLON_NUMBERS_PATTERN.sub(COLON_NUMBERS_REPL, text)

        # ВКПБ(о)
        if "(" in text:
            text = BRACE_IN_WORD_PATTERN.sub("\\1" + LEFT_BRACE_SUBST + "\\2" + RIGHT_BRACE_SUBST, text)

        if "<" in text:
            text = XML_TAG_PATTERN.sub(
                BREAKING_PLACEHOLDER + LEFT_ANGLE_SUBST + "\\1" + RIGHT_ANGLE_SUBST + BREAKING_PLACEHOLDER, text
            )
            text = text.replace(LEFT_ANGLE_SUBST + "/", "" + LEFT_ANGLE_SUBST + SLASH_SUBST)
            text = text.replace("/" + RIGHT_ANGLE_SUBST, "" + SLASH_SUBST + RIGHT_ANGLE_SUBST)

        if "-" in text:
            text = re.sub('([а-яіїєґА-ЯІЇЄҐ])([»"-]+-)', "\\1" + BREAKING_PLACEHOLDER + "\\2", text)
            text = re.sub('([»"-]+-)([а-яіїєґА-ЯІЇЄҐ])', "\\1" + BREAKING_PLACEHOLDER + "\\2", text)

        if SOFT_HYPHEN_WRAP in text:
            text = re.sub("(?<!\\s)" + SOFT_HYPHEN_WRAP, SOFT_HYPHEN_WRAP_SUBST, text)

        if "'" in text:
            text = APOSTROPHE_BEGIN_PATTERN.sub("\\1'" + BREAKING_PLACEHOLDER + "\\2", text)
            text = APOSTROPHE_END_PATTER.sub("\\1" + BREAKING_PLACEHOLDER + "'\\2", text)

        if "+" in text:
            text = re.sub("\\+(?=[а-яіїєґА-ЯІЇЄҐ])", BREAKING_PLACEHOLDER + "+" + BREAKING_PLACEHOLDER, text)

        text = NUMBER_MISSING_SPACE.sub("\\1" + BREAKING_PLACEHOLDER + "\\2", text)

        return text, urls

    def cleanup(self, text: str) -> str:
        text = (
            text.replace("\u2019", "'")
            .replace("\u02BC", "'")
            .replace("\u2018", "'")
            # .replace("`", "'")
            # .replace("´", "'")
            .replace("\u201A", ",")  # SINGLE LOW-9 QUOTATION MARK sometimes used as a comma
            .replace("\u2011", "-")  # we handle \u2013 in tagger so we can base our rule on it
        )

        text = WEIRD_APOSTROPH_PATTERN.sub(rf"\1{NON_BREAKING_PLACEHOLDER2}\2{NON_BREAKING_PLACEHOLDER2}\3", text)

        return text

    def split_with_delimiters(self, text: str, delim_pattern: re.Pattern) -> list[str]:
        parts: list[str] = []
        last_end: int = 0

        for matcher in delim_pattern.finditer(text):
            start: int = matcher.start()

            if last_end != start:
                non_delim: str = text[last_end:start]
                parts.append(non_delim)

            delim: str = matcher.group()
            parts.append(delim)

            last_end = matcher.end()

        if last_end != len(text):
            non_delim = text[last_end:]
            parts.append(non_delim)

        return parts

def tokenize_text(string: str) -> list[list[list[str]]]:
    """
    Tokenize input text to paragraphs, sentences and words.

    Tokenization to paragraphs is done using simple Newline algorithm
    For sentences and words tokenizers above are used

    :param string: Text to tokenize
    :type string: str or unicode
    :return: text, tokenized into paragraphs, sentences and words
    :rtype: list of list of list of words
    """
    tokenizer = UkrainianWordTokenizer()
    tokens = tokenizer.tokenize(text=string)
    paragraphs = []
    sentences : list[list[str]] = []
    current_sentence: list[str] = []
    for w in tokens:
        if w == " ":
            continue
        if w == ".":
            current_sentence.append(w)
            sentences.append(current_sentence)
            current_sentence = []
        elif w == "\n":
            paragraphs.append(sentences)
            sentences = []
        else:
            current_sentence.append(w)

    if len(current_sentence) > 0:
        sentences.append(current_sentence)
    if len(sentences) > 0:
        paragraphs.append(sentences)
    return paragraphs

def tokenize_words(string):
    """
    Tokenize input text to words.

    :param string: Text to tokenize
    :type string: str or unicode
    :return: words
    :rtype: list of strings
    """
    tokenizer = UkrainianWordTokenizer()
    tokens = tokenizer.tokenize(text=string)
    words = [w for w in tokens if w != ' ']
    return words

def tokenize_sents(string):
    """
    Tokenize input text to sentences.

    :param string: Text to tokenize
    :type string: str or unicode
    :return: sentences
    :rtype: list of strings
    """
    tokenizer = UkrainianWordTokenizer()
    tokens = tokenizer.tokenize(text=string)
    sentences = []
    current_sentence = ""
    for w in tokens:
        if w != ".":
            current_sentence += w
        else:
            sentences.append(current_sentence)
            current_sentence = ""
    if current_sentence != "":
        sentences.append(current_sentence)
    return sentences

__all__ = [
    "tokenize_words", "tokenize_text", "tokenize_sents", "UkrainianWordTokenizer"]
