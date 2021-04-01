/*
As part of the Nifi flow that processes of new data files in the secure area, we want to infer metadata (frictionless data package json)
and as part of it add in who approved the data to be brought into the secure area and when.
*/
const args = process.argv.slice(2)
const data_file_name = args[0];
const data_file_directory = args[1];
process.env['NODE_CONFIG_DIR'] = args[2];
const approver = args[3];
const approval_time = args[4];
const semanticinfer = require('semantic_infer');

// add the "source" below to inferred frictionless data package json
const source = {"sources": [{
  "title": data_file_name,
  "path": data_file_directory,
  "approver": approver,
  "approval_time": approval_time
}]}

semanticinfer.datapackage_infer_filesystem.datapackage_infer_filesystem(source);