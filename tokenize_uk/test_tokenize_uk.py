import unittest
from tokenize_uk import UkrainianWordTokenizer


class TokenizeUkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tokenizer = UkrainianWordTokenizer()

    def test_tokenize_url(self):
        url: str = "http://youtube.com:80/herewego?start=11&quality=high%3F"
        self.assertEqual([url, " "], self.tokenizer.tokenize(url + " "))

        url = "http://example.org"
        self.assertEqual([" ", url], self.tokenizer.tokenize(" " + url))

        url = "www.example.org"
        self.assertEqual([url], self.tokenizer.tokenize(url))

        url = "elect@ombudsman.gov.ua"
        self.assertEqual([url], self.tokenizer.tokenize(url))

        parts: list[str] = ["https://www.foo.com/foo", " ", "https://youtube.com", " ", "Зе"]
        self.assertEqual(parts, self.tokenizer.tokenize("".join(parts)))

        parts = ["https://www.phpbb.com/downloads/", '"', ">", "сторінку"]
        self.assertEqual(parts, self.tokenizer.tokenize("".join(parts)))

    def test_tokenize_tags(self):
        self.assertEqual(["<sup>", "3", "</sup>"], self.tokenizer.tokenize("<sup>3</sup>"))

    def test_numbers(self):
        test_list = self.tokenizer.tokenize("300 грн на балансі")
        self.assertEqual(["300", " ", "грн", " ", "на", " ", "балансі"], test_list)

        test_list = self.tokenizer.tokenize("надійшло 2,2 мільйона")
        self.assertEqual(["надійшло", " ", "2,2", " ", "мільйона"], test_list)

        test_list = self.tokenizer.tokenize("надійшло 84,46 мільйона")
        self.assertEqual(["надійшло", " ", "84,46", " ", "мільйона"], test_list)

        # TODO:
        #    test_list = self.tokenizer.tokenize("в 1996,1997,1998")
        #    self.assertEqual(["в", " ", "1996,1997,1998"], test_list)

        test_list = self.tokenizer.tokenize("2 000 тон з 12 000 відер")
        self.assertEqual(["2 000", " ", "тон", " ", "з", " ", "12 000", " ", "відер"], test_list)

        test_list = self.tokenizer.tokenize("надійшло 12 000 000 тон")
        self.assertEqual(["надійшло", " ", "12 000 000", " ", "тон"], test_list)

        test_list = self.tokenizer.tokenize("надійшло 12\u202F000\u202F000 тон")
        self.assertEqual(["надійшло", " ", "12 000 000", " ", "тон"], test_list)

        test_list = self.tokenizer.tokenize("до 01.01.42 400 000 шт.")
        self.assertEqual(["до", " ", "01.01.42", " ", "400 000", " ", "шт."], test_list)

        # should not merge these numbers
        test_list = self.tokenizer.tokenize("2 15 мільярдів")
        self.assertEqual(["2", " ", "15", " ", "мільярдів"], test_list)

        test_list = self.tokenizer.tokenize("у 2004 200 мільярдів")
        self.assertEqual(["у", " ", "2004", " ", "200", " ", "мільярдів"], test_list)

        test_list = self.tokenizer.tokenize("в бюджеті-2004 200 мільярдів")
        self.assertEqual(["в", " ", "бюджеті-2004", " ", "200", " ", "мільярдів"], test_list)

        test_list = self.tokenizer.tokenize("з 12 0001 відер")
        self.assertEqual(["з", " ", "12", " ", "0001", " ", "відер"], test_list)

        test_list = self.tokenizer.tokenize("сталося 14.07.2001 вночі")
        self.assertEqual(["сталося", " ", "14.07.2001", " ", "вночі"], test_list)

        test_list = self.tokenizer.tokenize("вчора о 7.30 ранку")
        self.assertEqual(["вчора", " ", "о", " ", "7.30", " ", "ранку"], test_list)

        test_list = self.tokenizer.tokenize("вчора о 7:30 ранку")
        self.assertEqual(["вчора", " ", "о", " ", "7:30", " ", "ранку"], test_list)

        test_list = self.tokenizer.tokenize("3,5-5,6% 7° 7,4°С")
        self.assertEqual(["3,5-5,6", "%", " ", "7", "°", " ", "7,4", "°", "С"], test_list)

        test_list = self.tokenizer.tokenize("відбулася 17.8.1245")
        self.assertEqual(["відбулася", " ", "17.8.1245"], test_list)

    def test_numbersmissingspace(self):
        test_list: list[str] = self.tokenizer.tokenize("від 12 до14 років")
        self.assertEqual(["від", " ", "12", " ", "до", "14", " ", "років"], test_list)

        test_list = self.tokenizer.tokenize("до14-15")
        self.assertEqual(["до", "14-15"], test_list)

        test_list = self.tokenizer.tokenize("Т.Шевченка53")
        self.assertEqual(["Т.", "Шевченка", "53"], test_list)

        #    test_list = self.tokenizer.tokenize("«Тен»103.")
        #    self.assertEqual(["«", "Тен", "»", "103", "."], test_list)

        test_list = self.tokenizer.tokenize("«Мак2»")
        self.assertEqual(["«", "Мак2", "»"], test_list)

        test_list = self.tokenizer.tokenize("км2")
        self.assertEqual(["км2"], test_list)

        test_list = self.tokenizer.tokenize("000ххх000")
        self.assertEqual(["000ххх000"], test_list)

    def test_plus(self):
        test_list: list[str] = self.tokenizer.tokenize("+20")
        self.assertEqual(["+20"], test_list)

        test_list = self.tokenizer.tokenize("прислівник+займенник")
        self.assertEqual(["прислівник", "+", "займенник"], test_list)

        test_list = self.tokenizer.tokenize("+займенник")
        self.assertEqual(["+", "займенник"], test_list)

        test_list = self.tokenizer.tokenize("Роттердам+ ")
        self.assertEqual(["Роттердам+", " "], test_list)

    def test_tokenize(self):
        test_list: list[str] = self.tokenizer.tokenize("Вони прийшли додому.")
        self.assertEqual(["Вони", " ", "прийшли", " ", "додому", "."], test_list)

        test_list = self.tokenizer.tokenize("Вони прийшли пʼятими зів’ялими.")
        self.assertEqual(["Вони", " ", "прийшли", " ", "п'ятими", " ", "зів'ялими", "."], test_list)

        #    test_list = self.tokenizer.tokenize("Вони\u0301 при\u00ADйшли пʼя\u0301тими зів’я\u00ADлими.")
        #    self.assertEqual(["Вони", " ", "прийшли", " ", "п'ятими", " ", "зів'ялими", "."], test_list)

        test_list = self.tokenizer.tokenize("я українець(сміється")
        self.assertEqual(["я", " ", "українець", "(", "сміється"], test_list)

        test_list = self.tokenizer.tokenize("ОУН(б) та КП(б)У")
        self.assertEqual(["ОУН(б)", " ", "та", " ", "КП(б)У"], test_list)

        test_list = self.tokenizer.tokenize("Негода є... заступником")
        self.assertEqual(["Негода", " ", "є", "...", " ", "заступником"], test_list)

        test_list = self.tokenizer.tokenize("Запагубили!.. також")
        self.assertEqual(["Запагубили", "!..", " ", "також"], test_list)

        test_list = self.tokenizer.tokenize("Цей графин.")
        self.assertEqual(["Цей", " ", "графин", "."], test_list)

        test_list = self.tokenizer.tokenize("— Гм.")
        self.assertEqual(["—", " ", "Гм", "."], test_list)

        test_list = self.tokenizer.tokenize("стін\u00ADку")
        self.assertEqual(["стін\u00ADку"], test_list)

        test_list = self.tokenizer.tokenize("стін\u00AD\nку")
        self.assertEqual(["стін\u00AD\nку"], test_list)

        # TODO: re-enable
        test_list = self.tokenizer.tokenize('п"яний')
        self.assertEqual(['п"яний'], test_list)

        test_list = self.tokenizer.tokenize("Веретениця**")
        self.assertEqual(["Веретениця", "**"], test_list)

        test_list = self.tokenizer.tokenize("мові***,")
        self.assertEqual(["мові", "***", ","], test_list)

        test_list = self.tokenizer.tokenize("*Оренбург")
        self.assertEqual(["*", "Оренбург"], test_list)

        test_list = self.tokenizer.tokenize("▶Трансформація")
        self.assertEqual(["▶", "Трансформація"], test_list)

        test_list = self.tokenizer.tokenize("усмішку😁")
        self.assertEqual(["усмішку", "😁"], test_list)

        test_list = self.tokenizer.tokenize("з*ясував")
        self.assertEqual(["з*ясував"], test_list)

    def test_initials(self):
        test_list: list[str] = self.tokenizer.tokenize("Засідав І.Єрмолюк.")
        self.assertEqual(["Засідав", " ", "І.", "Єрмолюк", "."], test_list)

        test_list = self.tokenizer.tokenize("Засідав І.   Єрмолюк.")
        self.assertEqual(["Засідав", " ", "І.", " ", " ", " ", "Єрмолюк", "."], test_list)

        test_list = self.tokenizer.tokenize("Засідав І. П. Єрмолюк.")
        self.assertEqual(["Засідав", " ", "І.", " ", "П.", " ", "Єрмолюк", "."], test_list)

        test_list = self.tokenizer.tokenize("Засідав І.П.Єрмолюк.")
        self.assertEqual(["Засідав", " ", "І.", "П.", "Єрмолюк", "."], test_list)

        test_list = self.tokenizer.tokenize("І.\u00A0Єрмолюк.")
        self.assertEqual(["І.", "\u00A0", "Єрмолюк", "."], test_list)

        test_list = self.tokenizer.tokenize("Засідав Єрмолюк І.")
        self.assertEqual(["Засідав", " ", "Єрмолюк", " ", "І."], test_list)

        test_list = self.tokenizer.tokenize("Засідав Єрмолюк І. П.")
        self.assertEqual(["Засідав", " ", "Єрмолюк", " ", "І.", " ", "П."], test_list)

        test_list = self.tokenizer.tokenize("Засідав Єрмолюк І. та інші")
        self.assertEqual(["Засідав", " ", "Єрмолюк", " ", "І.", " ", "та", " ", "інші"], test_list)

    def test_abbreviations(self):
        # скорочення
        test_list: list[str] = self.tokenizer.tokenize("140 тис. працівників")
        self.assertEqual(["140", " ", "тис.", " ", "працівників"], test_list)

        test_list = self.tokenizer.tokenize("450 тис. 297 грн")
        self.assertEqual(["450", " ", "тис.", " ", "297", " ", "грн"], test_list)

        test_list = self.tokenizer.tokenize("297 грн...")
        self.assertEqual(["297", " ", "грн", "..."], test_list)

        test_list = self.tokenizer.tokenize("297 грн.")
        self.assertEqual(["297", " ", "грн", "."], test_list)

        #    test_list = self.tokenizer.tokenize("297 грн.!!!")
        #    self.assertEqual(["297", " ", "грн.", "!!!"], test_list)

        #    test_list = self.tokenizer.tokenize("297 грн.??")
        #    self.assertEqual(["297", " ", "грн.", "??"], test_list)

        test_list = self.tokenizer.tokenize("450 тис.")
        self.assertEqual(["450", " ", "тис."], test_list)

        test_list = self.tokenizer.tokenize("450 тис.\n")
        self.assertEqual(["450", " ", "тис.", "\n"], test_list)

        test_list = self.tokenizer.tokenize("354\u202Fтис.")
        self.assertEqual(["354", "\u202F", "тис."], test_list)

        test_list = self.tokenizer.tokenize("911 тис.грн. з бюджету")
        self.assertEqual(["911", " ", "тис.", "грн", ".", " ", "з", " ", "бюджету"], test_list)

        # TODO: re-enable
        test_list = self.tokenizer.tokenize("за $400\n  тис., здавалося б")
        self.assertEqual(["за", " ", "$", "400", "\n", " ", " ", "тис.", ",", " ", "здавалося", " ", "б"], test_list)

        test_list = self.tokenizer.tokenize("найважчого жанру— оповідання")
        self.assertEqual(["найважчого", " ", "жанру", "—", " ", "оповідання"], test_list)

        test_list = self.tokenizer.tokenize("проф. Артюхов")
        self.assertEqual(["проф.", " ", "Артюхов"], test_list)

        test_list = self.tokenizer.tokenize("проф.\u00A0Артюхов")
        self.assertEqual(["проф.", "\u00A0", "Артюхов"], test_list)

        test_list = self.tokenizer.tokenize("Ів. Франко")
        self.assertEqual(["Ів.", " ", "Франко"], test_list)

        test_list = self.tokenizer.tokenize("кутю\u00A0— щедру")
        self.assertEqual(["кутю", "\u00A0", "—", " ", "щедру"], test_list)

        test_list = self.tokenizer.tokenize("також зав. відділом")
        self.assertEqual(["також", " ", "зав.", " ", "відділом"], test_list)

        test_list = self.tokenizer.tokenize("до н. е.")
        self.assertEqual(["до", " ", "н.", " ", "е."], test_list)

        test_list = self.tokenizer.tokenize("до н.е.")
        self.assertEqual(["до", " ", "н.", "е."], test_list)

        test_list = self.tokenizer.tokenize("в. о. начальника")
        self.assertEqual(["в.", " ", "о.", " ", "начальника"], test_list)

        test_list = self.tokenizer.tokenize("в.о. начальника")
        self.assertEqual(["в.", "о.", " ", "начальника"], test_list)

        test_list = self.tokenizer.tokenize("100 к.с.")
        self.assertEqual(["100", " ", "к.", "с."], test_list)

        test_list = self.tokenizer.tokenize("1998 р.н.")
        self.assertEqual(["1998", " ", "р.", "н."], test_list)

        test_list = self.tokenizer.tokenize("22 коп.")
        self.assertEqual(["22", " ", "коп."], test_list)

        test_list = self.tokenizer.tokenize("800 гр. м'яса")
        self.assertEqual(["800", " ", "гр.", " ", "м'яса"], test_list)

        test_list = self.tokenizer.tokenize("18-19 ст.ст. були")
        self.assertEqual(["18-19", " ", "ст.", "ст.", " ", "були"], test_list)

        test_list = self.tokenizer.tokenize("І ст. 11")
        self.assertEqual(["І", " ", "ст.", " ", "11"], test_list)

        test_list = self.tokenizer.tokenize("куб. м")
        self.assertEqual(["куб.", " ", "м"], test_list)

        test_list = self.tokenizer.tokenize("куб.м")
        self.assertEqual(["куб.", "м"], test_list)

        test_list = self.tokenizer.tokenize("У с. Вижва")
        self.assertEqual(["У", " ", "с.", " ", "Вижва"], test_list)

        test_list = self.tokenizer.tokenize("Довжиною 30 см. з гаком.")
        self.assertEqual(["Довжиною", " ", "30", " ", "см", ".", " ", "з", " ", "гаком", "."], test_list)

        test_list = self.tokenizer.tokenize("Довжиною 30 см. Поїхали.")
        self.assertEqual(["Довжиною", " ", "30", " ", "см", ".", " ", "Поїхали", "."], test_list)

        test_list = self.tokenizer.tokenize("100 м. дороги.")
        self.assertEqual(["100", " ", "м", ".", " ", "дороги", "."], test_list)

        test_list = self.tokenizer.tokenize("в м.Київ")
        self.assertEqual(["в", " ", "м.", "Київ"], test_list)

        test_list = self.tokenizer.tokenize("На висоті 4000 м...")
        self.assertEqual(["На", " ", "висоті", " ", "4000", " ", "м", "..."], test_list)

        test_list = self.tokenizer.tokenize("№47 (м. Слов'янськ)")
        self.assertEqual(["№47", " ", "(", "м.", " ", "Слов'янськ", ")"], test_list)

        test_list = self.tokenizer.tokenize("с.-г.")
        self.assertEqual(["с.-г."], test_list)

        test_list = self.tokenizer.tokenize("100 грн. в банк")
        self.assertEqual(["100", " ", "грн", ".", " ", "в", " ", "банк"], test_list)

        test_list = self.tokenizer.tokenize("таке та ін.")
        self.assertEqual(["таке", " ", "та", " ", "ін."], test_list)

        test_list = self.tokenizer.tokenize("і т. ін.")
        self.assertEqual(["і", " ", "т.", " ", "ін."], test_list)

        test_list = self.tokenizer.tokenize("і т.д.")
        self.assertEqual(["і", " ", "т.", "д."], test_list)

        test_list = self.tokenizer.tokenize("в т. ч.")
        self.assertEqual(["в", " ", "т.", " ", "ч."], test_list)

        test_list = self.tokenizer.tokenize("до т. зв. сальону")
        self.assertEqual(["до", " ", "т.", " ", "зв.", " ", "сальону"], test_list)

        test_list = self.tokenizer.tokenize(" і под.")
        self.assertEqual([" ", "і", " ", "под."], test_list)

        test_list = self.tokenizer.tokenize("Інститут ім. акад. Вернадського.")
        self.assertEqual(["Інститут", " ", "ім.", " ", "акад.", " ", "Вернадського", "."], test_list)

        test_list = self.tokenizer.tokenize("Палац ім. гетьмана Скоропадського.")
        self.assertEqual(["Палац", " ", "ім.", " ", "гетьмана", " ", "Скоропадського", "."], test_list)

        test_list = self.tokenizer.tokenize("від лат. momento")
        self.assertEqual(["від", " ", "лат.", " ", "momento"], test_list)

        test_list = self.tokenizer.tokenize("на 1-кімн. кв. в центрі")
        self.assertEqual(["на", " ", "1-кімн.", " ", "кв.", " ", "в", " ", "центрі"], test_list)

        test_list = self.tokenizer.tokenize("1 кв. км.")
        self.assertEqual(["1", " ", "кв.", " ", "км", "."], test_list)

        test_list = self.tokenizer.tokenize("Валерій (міліціонер-пародист.\n–  Авт.) стане пародистом.")
        self.assertEqual(
            [
                "Валерій",
                " ",
                "(",
                "міліціонер-пародист",
                ".",
                "\n",
                "–",
                " ",
                " ",
                "Авт.",
                ")",
                " ",
                "стане",
                " ",
                "пародистом",
                ".",
            ],
            test_list,
        )

        test_list = self.tokenizer.tokenize("Сьогодні (у четвер.  — Ред.), вранці.")
        self.assertEqual(
            ["Сьогодні", " ", "(", "у", " ", "четвер", ".", " ", " ", "—", " ", "Ред.", ")", ",", " ", "вранці", "."],
            test_list,
        )

        test_list = self.tokenizer.tokenize(
            "Fair trade [«Справедлива торгівля». –    Авт.], який стежить за тим, щоб у країнах"
        )
        self.assertTrue("Авт." in test_list)

        test_list = self.tokenizer.tokenize("диво з див.")
        self.assertEqual(["диво", " ", "з", " ", "див", "."], test_list)

        test_list = self.tokenizer.tokenize("диво з див...")
        self.assertEqual(["диво", " ", "з", " ", "див", "..."], test_list)

        test_list = self.tokenizer.tokenize("тел.: 044-425-20-63")
        self.assertEqual(["тел.", ":", " ", "044-425-20-63"], test_list)

        test_list = self.tokenizer.tokenize("с/г")
        self.assertEqual(["с/г"], test_list)

        test_list = self.tokenizer.tokenize("ім.Василя")
        self.assertEqual(["ім.", "Василя"], test_list)

        test_list = self.tokenizer.tokenize("ст.231")
        self.assertEqual(["ст.", "231"], test_list)

        test_list = self.tokenizer.tokenize("2016-2017рр.")
        self.assertEqual(["2016-2017", "рр."], test_list)

        test_list = self.tokenizer.tokenize("30.04.2010р.")
        self.assertEqual(["30.04.2010", "р."], test_list)

        test_list = self.tokenizer.tokenize("ні могили 6в. ")
        self.assertEqual(["ні", " ", "могили", " ", "6в", ".", " "], test_list)

        test_list = self.tokenizer.tokenize("в... одягненому")
        self.assertEqual(["в", "...", " ", "одягненому"], test_list)

        # invaild but happens
        test_list = self.tokenizer.tokenize("10 млн. чоловік")
        self.assertEqual(["10", " ", "млн.", " ", "чоловік"], test_list)

        test_list = self.tokenizer.tokenize("від Таврійської губ.5")
        self.assertEqual(["від", " ", "Таврійської", " ", "губ.", "5"], test_list)

        test_list = self.tokenizer.tokenize("від червоних губ.")
        self.assertEqual(["від", " ", "червоних", " ", "губ", "."], test_list)

        test_list = self.tokenizer.tokenize("К.-Святошинський")
        self.assertEqual(["К.-Святошинський"], test_list)

        test_list = self.tokenizer.tokenize("К.-Г. Руффман")
        self.assertEqual(["К.-Г.", " ", "Руффман"], test_list)

        test_list = self.tokenizer.tokenize("Рис. 10")
        self.assertEqual(["Рис.", " ", "10"], test_list)

        test_list = self.tokenizer.tokenize("худ. фільм")
        self.assertEqual(["худ.", " ", "фільм"], test_list)

        # not too frequent

    #    test_list = self.tokenizer.tokenize("30.04.10р.")
    #    self.assertEqual(["30.04.10", "р."], test_list)

    def test_brackets(self):
        # скорочення
        test_list: list[str] = self.tokenizer.tokenize("д[окто]р[ом]")
        self.assertEqual(["д[окто]р[ом]"], test_list)

    def test_apostrophe(self):
        test_list: list[str] = self.tokenizer.tokenize("’продукти харчування’")
        self.assertEqual(["'", "продукти", " ", "харчування", "'"], test_list)

        test_list = self.tokenizer.tokenize("схема 'гроші'")
        self.assertEqual(["схема", " ", "'", "гроші", "'"], test_list)

        test_list = self.tokenizer.tokenize("(‘дзеркало’)")
        self.assertEqual(["(", "'", "дзеркало", "'", ")"], test_list)

        test_list = self.tokenizer.tokenize("все 'дно піду")
        self.assertEqual(["все", " ", "'дно", " ", "піду"], test_list)

        test_list = self.tokenizer.tokenize("трохи 'дно 'дному сказано")
        self.assertEqual(["трохи", " ", "'дно", " ", "'дному", " ", "сказано"], test_list)

        test_list = self.tokenizer.tokenize("а мо',")
        self.assertEqual(["а", " ", "мо'", ","], test_list)

        test_list = self.tokenizer.tokenize("підемо'")
        self.assertEqual(["підемо", "'"], test_list)

        test_list = self.tokenizer.tokenize("ЗДОРОВ’Я.")
        self.assertEqual(["ЗДОРОВ'Я", "."], test_list)

        test_list = self.tokenizer.tokenize("''український''")
        self.assertEqual(["''", "український", "''"], test_list)

        # 'тсе, 'ддати  'го

        test_list = self.tokenizer.tokenize("'є")
        self.assertEqual(["'", "є"], test_list)

        test_list = self.tokenizer.tokenize("'(є)")
        self.assertEqual(["'", "(", "є", ")"], test_list)

    def test_dash(self):
        test_list: list[str] = self.tokenizer.tokenize("Кан’-Ка Но Рей")
        self.assertEqual(["Кан'-Ка", " ", "Но", " ", "Рей"], test_list)

        test_list = self.tokenizer.tokenize("і екс-«депутат» вибув")
        self.assertEqual(["і", " ", "екс-«депутат»", " ", "вибув"], test_list)

        test_list = self.tokenizer.tokenize('тих "200"-х багато')
        self.assertEqual(["тих", " ", '"200"-х', " ", "багато"], test_list)

        test_list = self.tokenizer.tokenize("«діди»-українці")
        self.assertEqual(["«діди»-українці"], test_list)

        #    test_list = self.tokenizer.tokenize("«краб»-переросток")
        #    self.assertEqual(["«", "краб", "»", "-", "переросток"], test_list)

        test_list = self.tokenizer.tokenize("вересні--жовтні")
        self.assertEqual(["вересні", "--", "жовтні"], test_list)

        test_list = self.tokenizer.tokenize("—У певному")
        self.assertEqual(["—", "У", " ", "певному"], test_list)

        test_list = self.tokenizer.tokenize("-У певному")
        self.assertEqual(["-", "У", " ", "певному"], test_list)

        test_list = self.tokenizer.tokenize("праця—голова")
        self.assertEqual(["праця", "—", "голова"], test_list)

        test_list = self.tokenizer.tokenize("Людина—")
        self.assertEqual(["Людина", "—"], test_list)

        test_list = self.tokenizer.tokenize("Х–ХІ")
        self.assertEqual(["Х", "–", "ХІ"], test_list)

        test_list = self.tokenizer.tokenize("VII-VIII")
        self.assertEqual(["VII", "-", "VIII"], test_list)

        test_list = self.tokenizer.tokenize("Стрий– ")
        self.assertEqual(["Стрий", "–", " "], test_list)

        test_list = self.tokenizer.tokenize("фіто– та термотерапії")
        self.assertEqual(["фіто–", " ", "та", " ", "термотерапії"], test_list)

        test_list = self.tokenizer.tokenize(" –Виділено")
        self.assertEqual([" ", "–", "Виділено"], test_list)

        test_list = self.tokenizer.tokenize("так,\u2013так")
        self.assertEqual(["так", ",", "\u2013", "так"], test_list)

    # def test_specialchars(self):
    #     text:str = "РЕАЛІЗАЦІЇ \u00AD\n" + "СІЛЬСЬКОГОСПОДАРСЬКОЇ"

    #     test_list: list[str] = self.tokenizer.tokenize(text).stream()
    #         .map(s -> s.replace("\n", "\\n").replace("\u00AD", "\\xAD"))
    #         .collect(Collectors.toList())
    #     self.assertEqual(["РЕАЛІЗАЦІЇ", " ", "\\xAD", "\\n", "СІЛЬСЬКОГОСПОДАРСЬКОЇ"], test_list)

    #     test_list = self.tokenizer.tokenize("а%його")
    #     self.assertEqual(["а", "%", "його"], test_list)

    #     test_list = self.tokenizer.tokenize("5%-го")
    #     self.assertEqual(["5%-го"], test_list)
