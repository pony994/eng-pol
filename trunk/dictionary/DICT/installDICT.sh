#przed instalacja nalezy zainstalowac dict i dictd
#skrypt nalezy uruchamiac jako superuser

cp eng-pol.dict.dz /usr/share/dictd
cp eng-pol.dict /usr/share/dictd
cp eng-pol.index /usr/share/dictd
dictdconfig -w && (killall dictd; dictd)
