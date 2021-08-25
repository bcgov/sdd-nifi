#!/bin/bash
mkdir -p data #folder for the raw data, draft summary reports, and metadata
mkdir -p approved_for_yellow/processed #folder for approved summary reports and metadata (sent to yellow zone)
mkdir -p existing_redzone_data_input/processed #processed folder for the "onramp" for data that already exists in the red zone
mkdir -p existing_redzone_data_input/approved #folder NiFi monitors for the "onramp" for data that already exists in the red zone
mkdir -p awaitingapproval/approved/processed #folders for the manual red zone approval processing