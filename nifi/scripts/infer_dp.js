/*
As part of the Nifi flow that processes of new data files in the secure area, we want to infer metadata (frictionless data package json)
and as part of it add in additional information about the origin of the data.
*/
const args = process.argv.slice(2)
const data_file_name = args[0];
const data_file_directory = args[1];
process.env['NODE_CONFIG_DIR'] = args[2];
const upload_info = args[3];
const semanticinfer = require('semantic_infer');

// add the "source" below to inferred frictionless data package json
const source = {"sources": [{
  "title": data_file_name,
  "path": data_file_directory,
  "upload_info": upload_info
}]}

semanticinfer.datapackage_infer_filesystem.datapackage_infer_filesystem(source);