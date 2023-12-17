RELEASE_NAME=flipperzero-goodies_keys_release`[ ! -z ${RELEASE} ] && echo _${RELEASE} || echo ''`

check-keys:
	python3 ./scripts/key-utils/check-duplicates.py

clear-keys-release:
	rm -rf ./release/ ./flipperzero-goodies_keys_release*

build-keys-release: clear-keys-release
	mkdir -p ./release/ibutton/
	mkdir ./release/ibutton_fuzzer/
	mkdir ./release/lfrfid/
	mkdir ./release/lfrfid_fuzzer/
	mkdir ./release/nfc/
	mkdir ./release/mifare_fuzzer/
	cp ./intercom-keys/*/keys/ibutton/* ./release/ibutton/ 2>/dev/null
	cp ./intercom-keys/*/keys/nfc/* ./release/nfc/ 2>/dev/null
	cp ./intercom-keys/*/keys/lfrfid/* ./release/lfrfid/ 2>/dev/null
	for file in $$(ls ./release/ibutton/*.ibtn); do \
	  	data=`cat $${file} | grep 'Data:' | cut -d ':' -f2- | tr -d ' '`; \
	  	data_length=`echo $${data} | tr -d ' \n' | wc -c | tr -d ' \t'`; \
	  	if [[ $${data_length} == 4 ]]; then \
	  		echo $${data} >> ./release/ibutton_fuzzer/wetox_uids_cyfral.txt; \
	  	fi; \
	  	if [[ $${data_length} == 8 ]]; then \
	  	  echo $${data} >> ./release/ibutton_fuzzer/wetox_uids_metakom.txt; \
	  	fi; \
	  	if [[ $${data_length} == 16 ]]; then \
	  		echo $${data} >> ./release/ibutton_fuzzer/wetox_uids_ds1990.txt; \
	    fi; \
	done;
	for file in $$(ls ./release/lfrfid/*.rfid); do \
	  	data=`cat $${file} | grep 'Data:' | cut -d ':' -f2- | tr -d ' '`; \
	  	data_length=`echo $${data} | tr -d ' \n' | wc -c | tr -d ' \t'`; \
	  	if [[ $${data_length} == 6 ]]; then \
	  		echo $${data} >> ./release/lfrfid_fuzzer/wetox_uids_h10301.txt; \
	  	fi; \
	  	if [[ $${data_length} == 8 ]]; then \
	  	  echo $${data} >> ./release/lfrfid_fuzzer/wetox_uids_pac.txt; \
	  	fi; \
	  	if [[ $${data_length} == 10 ]]; then \
	  		echo $${data} >> ./release/lfrfid_fuzzer/wetox_uids_em4100.txt; \
	    fi; \
	  	if [[ $${data_length} == 12 ]]; then \
	  		echo $${data} >> ./release/lfrfid_fuzzer/wetox_uids_hidprox.txt; \
	    fi; \
	done;
	for file in $$(ls ./release/nfc/*.nfc); do \
	  	data=`cat $${file} | grep 'UID:' | cut -d ':' -f2- | tr -d ' '`; \
	  	data_length=`echo $${data} | tr -d ' \n' | wc -c | tr -d ' \t'`; \
	  	if [[ $${data_length} == 8 ]]; then \
	  		echo $${data} >> ./release/mifare_fuzzer/wetox_uids_04.txt; \
	  	fi; \
	  	if [[ $${data_length} == 14 ]]; then \
	  	  echo $${data} >> ./release/mifare_fuzzer/wetox_uids_07.txt; \
	  	fi; \
	done;
	cp ./LICENSE ./AUTHORS.md ./release/
	echo 'Source repo: https://github.com/wetox-team/flipperzero-goodies\n\n' >> ./release/README.md
	echo '```\ncp -r '${RELEASE_NAME}'/ibutton/ /path/to/flipper_sd_card/' >> ./release/README.md
	echo 'cp -r '${RELEASE_NAME}'/nfc/ /path/to/flipper_sd_card/' >> ./release/README.md
	echo 'cp -r '${RELEASE_NAME}'/lfrfid/ /path/to/flipper_sd_card/' >> ./release/README.md
	echo 'cp -r '${RELEASE_NAME}'/ibutton_fuzzer/ /path/to/flipper_sd_card/  # https://github.com/DarkFlippers/Multi_Fuzzer' >> ./release/README.md
	echo 'cp -r '${RELEASE_NAME}'/lfrfid_fuzzer/ /path/to/flipper_sd_card/  # https://github.com/DarkFlippers/Multi_Fuzzer' >> ./release/README.md
	echo 'cp -r '${RELEASE_NAME}'/mifare_fuzzer/ /path/to/flipper_sd_card/  # https://github.com/spheeere98/mifare_fuzzer \n```' >> ./release/README.md
	echo "\nNFC - `find release -type f -name '*.nfc' | wc -l` items\n" >> ./release/README.md
	echo "RFID - `find release -type f -name '*.rfid' | wc -l` items\n" >> ./release/README.md
	echo "IButton - `find release -type f -name '*.ibtn' | wc -l` items" >> ./release/README.md
	mv release ${RELEASE_NAME}
	zip -r ${RELEASE_NAME}.zip ${RELEASE_NAME}
