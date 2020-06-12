const semanticinfer = require('semantic_infer');
const args = process.argv.slice(2)
const data_file_name = args[0];
const data_file_directory = args[1];
const source = {"sources": [{
  "title": data_file_name,
  "path": data_file_directory
}]}
semanticinfer.datapackage_infer_filesystem.datapackage_infer_filesystem(source);