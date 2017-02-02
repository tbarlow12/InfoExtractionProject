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

echo word
cat accuracyWord.txt
echo wordcap
cat accuracyWordCap.txt
echo poscon
cat accuracyPoscon.txt
echo lexcon
cat accuracyLexcon.txt
echo bothcon
cat accuracyBothcon.txt
