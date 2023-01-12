RELEASE_NAME=flipperzero-goodies_keys_release`[ ! -z ${RELEASE} ] && echo _${RELEASE} || echo ''`

check-keys:
	python3 ./scripts/key-utils/check-duplicates.py

clear-keys-release:
	rm -rf ./release/ ./flipperzero-goodies_keys_release*

build-keys-release: clear-keys-release
	mkdir -p ./release/ibutton/
	mkdir ./release/nfc/
	mkdir ./release/lfrfid/
	cp ./intercom-keys/*/keys/ibutton/* ./release/ibutton/ 2>/dev/null
	cp ./intercom-keys/*/keys/nfc/* ./release/nfc/ 2>/dev/null
	cp ./intercom-keys/*/keys/lfrfid/* ./release/lfrfid/ 2>/dev/null
	cp ./LICENSE ./AUTHORS.md ./release/
	echo 'Source repo: https://github.com/wetox-team/flipperzero-goodies\n\n' >> ./release/README.md
	echo '```\ncp '${RELEASE_NAME}'/ibutton/* /path/to/flipper_sd_card/ibutton/' >> ./release/README.md
	echo 'cp '${RELEASE_NAME}'/nfc/* /path/to/flipper_sd_card/nfc/' >> ./release/README.md
	echo 'cp '${RELEASE_NAME}'/lfrfid/* /path/to/flipper_sd_card/lfrfid/\n```' >> ./release/README.md
	echo "\nNFC - `find release -type f -name '*.nfc' | wc -l` items" >> ./release/README.md
	echo "RFID - `find release -type f -name '*.rfid' | wc -l` items" >> ./release/README.md
	echo "IButton - `find release -type f -name '*.ibtn' | wc -l` items" >> ./release/README.md
	mv release ${RELEASE_NAME}
	zip -r ${RELEASE_NAME}.zip ${RELEASE_NAME}
