#!/bin/bash

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Damegender; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

# First, we save the current config and create the config for the tests

cp config.cfg config.cfg.backup

echo "
[DEFAULT]
genderapi = no
genderize = no
nameapi = no
namsor = no
customsearch = no

[FILES]
genderapi = files/apikeys/genderapipass.txt
genderize = files/apikeys/genderizepass.txt
genderguesser = files/apikeys/genderguesserpass.txt
namsor = files/apikeys/namsorpass.txt
nameapi = files/apikeys/nameapipass.txt
" > config.cfg

python3.5m main.py David > files/tests/maindavid-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/maindavid.txt files/tests/maindavid-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "maindavid test is failing"
else
    echo "maindavid test is ok"
fi

python3.5m main.py Jesús > files/tests/mainjesus-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainjesus.txt files/tests/mainjesus-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "mainjesus test is failing"
else
    echo "mainjesus test is ok"
fi

python3.5m main.py Inés > files/tests/mainines-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainines.txt files/tests/mainines-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainines test is failing"
else
	echo "mainines test is ok"
fi

python3.5m main.py Alex > files/tests/mainalex-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainalex.txt files/tests/mainalex-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainalex test is failing"
else
	echo "mainalex test is ok"
fi

python3.5m main.py Andrea > files/tests/mainandrea-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainandrea.txt files/tests/mainandrea-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainandrea test is failing"
else
	echo "mainandrea test is ok"
fi

python3.5m main.py "Jesús María" > files/tests/mainjesusmaria-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainjesusmaria.txt files/tests/mainjesusmaria-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainjesusmaria test is failing"
else
	echo "mainjesusmaria test is ok"
fi

python3.5m main.py "José María" > files/tests/mainjosemaria-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainjosemaria.txt files/tests/mainjosemaria-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "mainjosemaria test is failing"
else
	echo "mainjosemaria test is ok"
fi

python3.5m main.py Mesa --ml=nltk > files/tests/mainmesa-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainmesa.txt files/tests/mainmesa-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "mainmesa test is failing"
else
    echo "mainmesa test is ok"
fi

python3.5m main.py silla --ml=forest > files/tests/mainsilla-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/mainsilla.txt files/tests/mainsilla-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "mainsilla test is failing"
else
    echo "mainsilla test is ok"
fi



python3.5m nameincountries.py David > files/tests/nameincountriesdavid-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/nameincountriesdavid.txt files/tests/nameincountriesdavid-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "nameincountries david test is failing"
else
	echo "nameincountries david test is ok"
fi

python3.5m nameincountries.py david > files/tests/nameincountriesdavid2-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/nameincountriesdavid2.txt files/tests/nameincountriesdavid2-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "nameincountries david donwcase test is failing"
else
	echo "nameincountries david donwcase test is ok"
fi


python3.5m nameincountries.py Jesús > files/tests/nameincountriesjesus-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/nameincountriesjesus.txt files/tests/nameincountriesjesus-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "nameincountries jesus test is failing"
else
	echo "nameincountries jesus test is ok"
fi


# python3.5m infofeatures.py > files/tests/infofeatures-$(date "+%Y-%m-%d-%H").txt

# if ! cmp files/tests/infofeatures.txt files/tests/infofeatures-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
# then
# 	echo "infofeatures test is failing"
# else
# 	echo "infofeatures test is ok"
# fi

python3.5m csv2gender.py files/names/all.csv > files/tests/csv2genderall-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/csv2genderall.txt files/tests/csv2genderall-$(date "+%Y-%m-%d-%H").txt
then
	echo "csv2genderall test is failing"
else
	echo "csv2genderall test is ok"
fi

python3.5m csv2gender.py files/names/partial.csv > files/tests/csv2genderpartial-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/csv2genderpartial.txt files/tests/csv2genderpartial-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "csv2genderpartial test is failing"
else
	echo "csv2genderpartial test is ok"
fi

if [ -a files/images/pca_components_files_features_list.csv.png ]; then
    rm files/images/pca_components_files_features_list.csv.png
fi

python3.5m pca-components.py --csv='files/features_list.csv' --no-show
if [ -a files/images/pca_components_files_features_list.csv.png ]; then
	echo "pca-components test is ok"
else
	echo "pca-components test is failing"
fi

python3.5m pca-features.py --categorical="both" --components=7 > files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/pca-features-nocategorical.txt files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "pca-features-both test is failing"
else
	echo "pca-features-both test is ok"
fi

if [ -a files/images/pca_components_files_features_list_no_cat.csv.png ]; then
    rm files/images/pca_components_files_features_list_no_cat.csv.png
fi

python3.5m pca-components.py --csv='files/features_list_no_cat.csv' --no-show
if [ -a files/images/pca_components_files_features_list_no_cat.csv.png ]; then
	echo "pca-components-nocategorical test is ok"
else
	echo "pca-components-nocategorical test is failing"
fi

python3.5m pca-features.py --categorical="nocategorical" --components=7 > files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/pca-features-nocategorical.txt files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "pca-features-nocategorical test is failing"
else
	echo "pca-features-nocategorical test is ok"
fi

if [ -a files/images/pca_components_files_features_list_cat.csv.png ]; then
    rm files/images/pca_components_files_features_list_cat.csv.png
fi

python3.5m pca-components.py --csv='files/features_list_cat.csv' --no-show
if [ -a files/images/pca_components_files_features_list_cat.csv.png ]; then
	echo "pca-components-categorical test is ok"
else
	echo "pca-components-categorical test is failing"
fi

python3.5m pca-features.py --categorical="noletters" --components=3 > files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/pca-features-nocategorical.txt files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "pca-features-nocategorical test is failing"
else
	echo "pca-features-nocategorical test is ok"
fi

if [ -a files/images/pca_components_files_features_list_no_undefined.csv.png ]; then
    rm files/images/pca_components_files_features_list_no_undefined.csv.png
fi

python3.5m pca-components.py --csv='files/features_list_no_undefined.csv' --no-show
if [ -a files/images/pca_components_files_features_list_no_undefined.csv.png ]; then
	echo "pca-components-no-undefined test is ok"
else
	echo "pca-components-no-undefined test is failing"
fi

python3.5m pca-features.py --categorical="both" --components=3 > files/tests/pca-features-both-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/pca-features-both.txt files/tests/pca-features-both-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "pca-features-both test is failing"
else
	echo "pca-features-both test is ok"
fi


python3.5m pca-features.py --categorical="noletters" --components=3 > files/tests/pca-features-categorical-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/pca-features-nocategorical.txt files/tests/pca-features-nocategorical-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "pca-features-nocategorical test is failing"
else
	echo "pca-features-nocategorical test is ok"
fi


python3.5m confusion.py --csv="files/names/min.csv" --api=damegender > files/tests/confusion-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/confusion.txt files/tests/confusion-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusion test is failing"
else
	echo "confusion test is ok"
fi

python3.5m confusion.py --csv="files/names/min.csv" --ml="nltk" --api=damegender > files/tests/confusionnltk-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/confusionnltk.txt files/tests/confusionnltk-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusion nltk test is failing"
else
	echo "confusion nltk test is ok"
fi

python3.5m confusion.py --csv="files/names/min.csv" --api=genderapi --jsondownloaded="files/names/genderapifiles_names_min.csv.json" > files/tests/confusiongenderapijsondownloaded-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/confusiongenderapijsondownloaded.txt files/tests/confusiongenderapijsondownloaded-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusion genderapi jsondonwloaded test is failing"
else
	echo "confusion genderapi jsondonwloaded test is ok"
fi


python3.5m confusion.py --csv=files/names/partialnoundefined.csv --api=genderize --jsondownloaded=files/names/genderizefiles_names_partialnoundefined.csv.json > files/tests/confusion-genderize-partialnoun-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusion-genderize-partialnoun.txt files/tests/confusion-genderize-partialnoun-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusion genderize jsondonwloaded test is failing"
else
	echo "confusion genderize jsondonwloaded test is ok"
fi


python3.5m confusion.py --csv="files/names/partial.csv" --api=nameapi --jsondownloaded="files/names/nameapifiles_names_partial.csv.json" > files/tests/confusionnameapijsondownloaded-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/confusionnameapijsondownloaded.txt files/tests/confusionnameapijsondownloaded-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "confusion nameapi jsondonwloaded test is failing"
else
	echo "confusion nameapi jsondonwloaded test is ok"
fi

python3.5m accuracy.py --csv="files/names/min.csv" --api=genderapi --jsondownloaded="files/names/genderapifiles_names_min.csv.json" > files/tests/accuracygenderapijsondownloaded-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracygenderapijsondownloaded.txt files/tests/accuracygenderapijsondownloaded-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracy genderapi jsondonwloaded test is failing"
else
	echo "accuracy genderapi jsondonwloaded test is ok"
fi

python3.5m accuracy.py --csv=files/names/partial.csv --api=nameapi --json="files/names/nameapifiles_names_partial.csv.json" > files/tests/accuracypartialjsonnameapi-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracypartialjsonnameapi.txt files/tests/accuracypartialjsonnameapi-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo "accuracy nameapi jsondonwloaded test is failing"
else
	echo "accuracy nameapi jsondonwloaded test is ok"
fi

python3.5m accuracy.py --jsondownloaded=files/names/genderizefiles_names_partialnoundefined.csv.json --measure=f1score --api=genderize --csv=files/names/partialnoundefined.csv > files/tests/accuracygenderizepartialjsonf1score-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracygenderizepartialjsonf1score.txt files/tests/accuracygenderizepartialjsonf1score-$(date "+%Y-%m-%d-%H").txt
then
	echo "accuracy genderize f1score jsondonwloaded test is failing"
else
	echo "accuracy genderize f1score jsondonwloaded test is ok"
fi

python3.5m accuracy.py --jsondownloaded=files/names/genderizefiles_names_partialnoundefined.csv.json --measure=precision --api=genderize --csv=files/names/partialnoundefined.csv > files/tests/accuracygenderizepartialjsonprecision-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracygenderizepartialjsonprecision.txt files/tests/accuracygenderizepartialjsonprecision-$(date "+%Y-%m-%d-%H").txt
then
	echo "accuracy genderize precision jsondonwloaded test is failing"
else
	echo "accuracy genderize precision jsondonwloaded test is ok"
fi

python3.5m accuracy.py --jsondownloaded=files/names/genderizefiles_names_partialnoundefined.csv.json --measure=recall --api=genderize --csv=files/names/partialnoundefined.csv > files/tests/accuracygenderizepartialjsonrecall-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracygenderizepartialjsonrecall.txt files/tests/accuracygenderizepartialjsonrecall-$(date "+%Y-%m-%d-%H").txt
then
	echo "accuracy genderize recall jsondonwloaded test is failing"
else
	echo "accuracy genderize recall jsondonwloaded test is ok"
fi


python3.5m accuracy.py --jsondownloaded=files/names/genderizefiles_names_partialnoundefined.csv.json --measure=accuracy --api=genderize --csv=files/names/partialnoundefined.csv > files/tests/accuracygenderizepartialjsonaccuracy-$(date "+%Y-%m-%d-%H").txt
if ! cmp files/tests/accuracygenderizepartialjsonaccuracy.txt files/tests/accuracygenderizepartialjsonaccuracy-$(date "+%Y-%m-%d-%H").txt
then
	echo "accuracy genderize accuracy jsondonwloaded test is failing"
else
	echo "accuracy genderize accuracy jsondonwloaded test is ok"
fi


echo "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt

echo "restoring the config"
cp config.cfg.backup config.cfg
rm config.cfg.backup
