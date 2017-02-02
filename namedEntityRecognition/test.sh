python ner.py train.txt test.txt word
python ner.py train.txt test.txt wordcap
python ner.py train.txt test.txt poscon
python ner.py train.txt test.txt lexcon
python ner.py train.txt test.txt bothcon
mv test.txt.* liblinear-1.93/
mv train.txt.* liblinear-1.93/
