const args = process.argv.slice(2)
const data_file_name = args[0];
const data_file_directory = args[1];
process.env['NODE_CONFIG_DIR'] = args[2];
const approver = args[3];
const approval_time = args[4];
const semanticinfer = require('semantic_infer');
const source = {"sources": [{
  "title": data_file_name,
  "path": data_file_directory,
  "approver": approver,
  "approval_time": approval_time
}]}

semanticinfer.datapackage_infer_filesystem.datapackage_infer_filesystem(source);