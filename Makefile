SRC_DIR=$(shell pwd)
BUILD_DIR=$(SRC_DIR)/build
STAGING_DIRECTORY_STAMP=$(BUILD_DIR)/staging-directory-stamp
STAGING_DIRECTORY=$(BUILD_DIR)/staging
STAGING_REQUIREMENTS_STAMP=$(BUILD_DIR)/staging_requirements_stamp
OUTPUT_ZIP=$(BUILD_DIR)/lambda.zip

all: $(OUTPUT_ZIP)

clean:
	rm -f $(STAGING_DIRECTORY_STAMP)
	rm -f $(STAGING_REQUIREMENTS_STAMP)
	rm -rf $(STAGING_DIRECTORY)
	rm -f $(OUTPUT_ZIP)

$(STAGING_DIRECTORY_STAMP): $(SRC_DIR)/lambda_function.py
	mkdir -p $(STAGING_DIRECTORY)
	cp $(SRC_DIR)/lambda_function.py $(STAGING_DIRECTORY)/
	touch $@

$(OUTPUT_ZIP): $(STAGING_REQUIREMENTS_STAMP) $(STAGING_DIRECTORY_STAMP)
	rm -f $(OUTPUT_ZIP)
	cd $(STAGING_DIRECTORY) && zip -q -9 -r $(OUTPUT_ZIP) *

$(STAGING_REQUIREMENTS_STAMP): $(SRC_DIR)/requirements.txt
	mkdir -p $(STAGING_DIRECTORY)
	pip install -r requirements.txt -t $(STAGING_DIRECTORY)
	touch $@


UPLOAD_CODE_STAMP=$(BUILD_DIR)/upload-stamp

$(UPLOAD_CODE_STAMP): $(OUTPUT_ZIP)
	aws lambda update-function-code --function-name iot-find-iphone --zip-file fileb://build/lambda.zip
	touch $@

upload: $(UPLOAD_CODE_STAMP)

.PHONY: all clean upload

