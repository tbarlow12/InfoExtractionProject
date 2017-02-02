./train -s 0 train.txt.word model.word
./train -s 0 train.txt.wordcap model.wordcap
./train -s 0 train.txt.poscon model.poscon
./train -s 0 train.txt.lexcon model.lexcon
./train -s 0 train.txt.bothcon model.bothcon
./predict test.txt.word model.word? predictions.txt > accuracyWord.txt
./predict test.txt.wordcap model.wordcap? predictions.txt > accuracyWordCap.txt
./predict test.txt.poscon model.poscon? predictions.txt > accuracyPoscon.txt
./predict test.txt.lexcon model.lexcon? predictions.txt > accuracyLexcon.txt
./predict test.txt.bothcon model.bothcon? predictions.txt > accuracyBothcon.txt
cat accuracyWord.txt
cat accuracyWordCap.txt
cat accuracyPoscon.txt
cat accuracyLexcon.txt
cat accuracyBothcon.txt
