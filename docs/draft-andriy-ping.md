# Draft issue for brown-uk/nlp_uk (post as yourself)

Title: FYI: байт-ідентичні Python-порти токенізації LanguageTool (choppa-srx, tokenize-uk 2.0)

Привіт, @arysin!

Хотів поділитися новиною, яка може бути цікава користувачам nlp_uk, що працюють у Python-стеку.

Ми нарешті довели до пуття Python-порти української токенізації LanguageTool:

- **[choppa-srx](https://pypi.org/project/choppa-srx/)** — порт java-бібліотеки segment (алгоритм ultimate) з правилами `segment.srx` з LanguageTool. Вихід **байт-ідентичний** Java-оригіналу: перевірено на ~136 тис. сегментів реальних текстів (новини, художня література, uk+en) плюс усі 848 тестів з 24 мовних тест-сьютів LT. Працює у ~5 разів швидше за Java CLI.
- **[tokenize-uk 2.0](https://github.com/lang-uk/tokenize-uk/pull/13)** — порт Вашого `UkrainianWordTokenizer` (синхронізований з master станом на `0761ec3e`). Теж **байт-ідентичний**: 3 871 085 токенів на чотирьох корпусах, нуль розбіжностей, швидше за Java. Іде в парі з choppa для речень — тобто повний пайплайн абзаци→речення→слова з якістю LT.

В обох репозиторіях тепер є щотижневий watchdog, який відкриває issue, щойно Ваші правила чи токенізатор змінюються в LT master — тож порти більше не відставатимуть роками, а виправлення підтягуватимуться швидко.

Величезна подяка за роки роботи над українською в LanguageTool — ці порти повністю стоять на Ваших правилах. Якщо помітите розбіжності з очікуваною поведінкою — issue у [lang-uk/choppa](https://github.com/lang-uk/choppa) чи [lang-uk/tokenize-uk](https://github.com/lang-uk/tokenize-uk) дуже вітаються.
